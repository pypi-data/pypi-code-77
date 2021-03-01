# This file is a part of pyctr.
#
# Copyright (c) 2017-2021 Ian Burgwin
# This file is licensed under The MIT License (MIT).
# You can find the full license text in LICENSE in the root of this project.

from enum import IntEnum
from hashlib import sha1, sha256
from os import PathLike
from threading import Lock
from typing import NamedTuple, TYPE_CHECKING

from common import PyCTRError
from crypto import CryptoEngine, Keyslot
from fileio import SubsectionIO
from util import readbe, readle
from type.base.typereader import TypeReaderCryptoBase
from type.exefs import EXEFS_HEADER_SIZE, ExeFSReader, InvalidExeFSError, ExeFSFileNotFoundError

if TYPE_CHECKING:
    from typing import BinaryIO, Dict, List, Optional, Tuple, Union

    from crypto import CTRFileIO

NAND_MEDIA_UNIT = 0x200

# ncsd image doesn't have the actual size
nand_size = {0x200000: 0x3AF00000, 0x280000: 0x4D800000}


class NANDError(PyCTRError):
    """Generic error for NAND operations."""


class InvalidNANDError(NANDError):
    """Invalid NAND header exception."""


class MissingOTPError(NANDError):
    """OTP wasn't loaded."""


class PartitionFSType(IntEnum):
    """Type of filesystem in the partition."""

    Nothing = 0  # this would be "None" but that's a reserved keyword
    """No partition here."""

    Normal = 1
    """Used for TWL and CTR parts."""

    FIRM = 3
    """Used for FIRM partitions."""

    AGBFIRMSave = 4
    """Used for the AGB_FIRM save partition."""


class PartitionEncryptionType(IntEnum):
    """
    Type of encryption on the partition. In practice this is only really used to determine what keyslot to use for
    CTRNAND which changes between Old 3DS and New 3DS. It's not really known what happens if any of the other partitions
    have the crypt type changed.
    """

    TWL = 1
    """Used for the TWL partitions."""

    CTR = 2
    """Used for FIRM, CTR on Old 3DS, and AGB_FIRM save partitions."""

    New3DSCTR = 3
    """Used for the CTR partitions on New 3DS."""


class NCSDPartitionInfo(NamedTuple):
    fs_type: 'Union[PartitionFSType, int]'
    encryption_type: 'Union[PartitionEncryptionType, int]'
    offset: int
    size: int
    base_file: 'Optional[str]'


class NAND(TypeReaderCryptoBase):

    def __init__(self, file: 'Union[PathLike, str, bytes, BinaryIO]', mode: str = 'rb', *, closefd: bool = True,
                 crypto: CryptoEngine = None, dev: bool = False, otp: bytes = None,
                 otp_file: 'Union[PathLike, str, bytes]' = None, cid: bytes = None,
                 cid_file: 'Union[PathLike, str, bytes]' = None):
        super().__init__(file=file, mode=mode, closefd=closefd, crypto=crypto, dev=dev)

        self._lock = Lock()

        # set up otp if it was provided
        # otherwise it has to be in essential.exefs or set up manually with a custom CryptoEngine object
        if otp:
            self._crypto.setup_keys_from_otp(otp)
        elif otp_file:
            self._crypto.setup_keys_from_otp_file(otp_file)

        # ignore the signature, we don't need it
        self._file.seek(0x100, 1)
        header = self._file.read(0x100)
        if header[0:4] != b'NCSD':
            raise InvalidNANDError('NCSD magic not found')

        # make sure the Media ID is all zeros, since anything else makes it a CCI
        media_id = header[0x8:0x10]
        if media_id != b'\0' * 8:
            raise InvalidNANDError('Not a NAND, this is a CCI')

        # check for essential.exefs
        try:
            self.essential = ExeFSReader(self._file, closefd=False)
        except InvalidExeFSError:
            self.essential = None

        self._file.seek(0, 2)
        raw_nand_size = self._file.tell() - self._start
        self._subfile = SubsectionIO(self._file, self._start, raw_nand_size)

        partition_fs_types = header[0x10:0x18]
        partition_crypt_types = header[0x18:0x20]
        partition_range_table_raw = header[0x20:0x60]
        partition_range_table = [partition_range_table_raw[x:x + 8] for x in range(0, 0x40, 0x8)]

        self.ncsd_partition_info: Dict[int, NCSDPartitionInfo] = {}
        self.partition_files: Dict[int, BinaryIO] = {}

        for idx in range(8):
            if not partition_fs_types[idx]:  # if there is no partition
                continue

            # This is largely based on assumptions that should work in every case, unless the partitions have been
            #   manually tweaked. If you're bored and want to figure out how the system actually works, mess with the
            #   partition table and let me know what you find!

            fs_type = partition_fs_types[idx]
            encryption_type = partition_crypt_types[idx]
            offset = readle(partition_range_table[idx][0:4]) * NAND_MEDIA_UNIT
            size = readle(partition_range_table[idx][4:8]) * NAND_MEDIA_UNIT

            if fs_type == PartitionFSType.Normal:
                if encryption_type == PartitionEncryptionType.TWL:
                    base_file = 'twl'
                elif encryption_type == PartitionEncryptionType.CTR:
                    base_file = 'ctr_old'
                elif encryption_type == PartitionEncryptionType.New3DSCTR:
                    base_file = 'ctr_new'
                else:
                    base_file = None
            elif fs_type == PartitionFSType.FIRM:
                base_file = 'firm'
            elif fs_type == PartitionFSType.AGBFIRMSave:
                base_file = 'agb'
            else:
                base_file = None

            info = NCSDPartitionInfo(fs_type=partition_fs_types[idx],
                                     encryption_type=partition_crypt_types[idx],
                                     offset=offset,
                                     size=size,
                                     base_file=base_file)

            self.ncsd_partition_info[idx] = info

        if not self._crypto.otp_keys_set:
            if self.essential:
                try:
                    with self.essential.open('otp') as f:
                        otp = f.read(0x100)
                    self._crypto.setup_keys_from_otp(otp)
                except ExeFSFileNotFoundError:
                    raise MissingOTPError('OTP was not provided in the otp or otp_file arguments, '
                                          'and otp is not in essential.exefs')
            else:
                raise MissingOTPError('OTP was not provided in the otp or otp_file arguments, '
                                      'and essential.exefs is missing')

        # cid should take precedence over the file
        if cid_file and not cid:
            with open(cid_file, 'rb') as f:
                cid = f.read(0x10)

        # if cid is still not provided, try to get it from essential.exefs
        if not cid:
            if self.essential:
                try:
                    with self.essential.open('nand_cid') as f:
                        cid = f.read(0x10)
                except ExeFSFileNotFoundError:
                    pass  # an attempt to generate the counter from known data later

        # generate the counter from the cid if it's available now
        if cid:
            self.counter = readbe(sha256(cid).digest()[0:0x10])
            self.counter_twl = readle(sha1(cid).digest()[0:0x10])
        else:
            # try to generate the counter from a known block of data that should not change normally
            raise NotImplementedError('Counter generation is not implemented yet')

        self._base_files = {
            'twl': self._crypto.create_ctr_io(Keyslot.TWLNAND, self._subfile, self.counter_twl),
            'ctr_old': self._crypto.create_ctr_io(Keyslot.CTRNANDOld, self._subfile, self.counter),
            'ctr_new': self._crypto.create_ctr_io(Keyslot.CTRNANDNew, self._subfile, self.counter),
            'firm': self._crypto.create_ctr_io(Keyslot.FIRM, self._subfile, self.counter),
            'agb': self._crypto.create_ctr_io(Keyslot.AGB, self._subfile, self.counter),
        }

    def open_ncsd_partition(self, partition_index: int):
        info = self.ncsd_partition_info[partition_index]
        return SubsectionIO(self._base_files[info.base_file], info.offset, info.size)
