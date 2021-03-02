import gzip
import struct
import time
from io import BytesIO
from typing import List

from .tl_base import TL
from ..utils import get_json


# TODO: Fix things here


class Int(TL):
    SIZE = 4

    @classmethod
    def read(cls, data: "chameleongram.raw.reader.Reader", signed: bool = True) -> int:
        return int.from_bytes(data.read(cls.SIZE), "little", signed=signed)

    @classmethod
    def getvalue(cls, value: int, signed: bool = True) -> bytes:
        return value.to_bytes(cls.SIZE, "little", signed=signed)


class Long(Int):
    SIZE = 8


class Int128(Int):
    SIZE = 16


class Int256(Int):
    SIZE = 32


class BoolFalse(TL):
    ID = 0xBC799737

    def getvalue(self):
        return Int.getvalue(self.ID, False)


class BoolTrue(TL):
    ID = 0x997275B5

    def getvalue(self):
        return Int.getvalue(self.ID, False)


class Bool(TL):
    @staticmethod
    def read(data: "chameleongram.raw.reader.Reader"):
        return True if Int.read(data) == BoolTrue.ID else False

    @staticmethod
    def getvalue(value: bool):
        return BoolTrue().getvalue() if value else BoolFalse().getvalue()


class Bytes(TL):
    @staticmethod
    def read(data: "chameleongram.raw.reader.Reader") -> bytes:
        length = int.from_bytes(data.read(1), "little")

        if length <= 253:
            result = data.read(length)
            data.read(-(length + 1) % 4)
        else:
            length = int.from_bytes(data.read(3), "little")
            result = data.read(length)
            data.read(-length % 4)
        return result

    @staticmethod
    def getvalue(value: bytes) -> bytes:
        length = len(value)
        data = BytesIO()

        if length <= 253:
            data.write(length.to_bytes(1, "little"))
            data.write(value)
            data.write(bytes(-(length + 1) % 4))
        else:
            data.write((254).to_bytes(1, "little"))
            data.write(length.to_bytes(3, "little"))
            data.write(value)
            data.write(bytes(-length % 4))
        return data.getvalue()


class String(TL):
    @staticmethod
    def read(data: "chameleongram.raw.reader.Reader") -> str:
        return Bytes.read(data).decode("utf-8", errors="replace")

    @staticmethod
    def getvalue(value: str) -> bytes:
        return Bytes.getvalue(value.encode("utf-8"))


class Double(TL):
    @staticmethod
    def read(data: "chameleongram.raw.reader.Reader") -> float:
        return struct.unpack("<d", data.read(8))[0]

    @staticmethod
    def getvalue(value: float) -> bytes:
        return struct.pack("<d", value)


class Vector(TL):
    ID = 0x1CB5C415

    @staticmethod
    def read(data: "chameleongram.raw.reader.Reader", tl_object: TL = None) -> List[TL]:
        return [
            tl_object.read(data) if tl_object else data.readtg()
            for _ in range(Int.read(data))
        ]

    def getvalue(self, values: List[TL], tl_object: TL = None) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(self.ID, False))
        data.write(Int.getvalue(len(values)))

        for value in values:
            if tl_object:
                data.write(tl_object.getvalue(value))
            else:
                data.write(value.getvalue())
        return data.getvalue()


class MessageID(TL):
    max_id = 0

    @classmethod
    def getvalue(cls) -> int:
        message_id = int(time.time()) * 2 ** 32
        assert (
                message_id % 4 == 0
        ), f"The message_id ({message_id}) is not divisible by 4, consider syncing your time"

        if message_id <= cls.max_id:
            message_id = cls.max_id + 4
        cls.max_id = message_id
        return message_id


class SeqNo(TL):
    seq_no = 1

    @classmethod
    def getvalue(cls, is_content_related: bool = False) -> int:
        cls.seq_no += abs(2 * ~is_content_related)
        return cls.seq_no


class GzipPacked(TL):
    ID = 0x3072CFA1

    def __init__(self, packed_data: bytes):
        self.packed_data = packed_data

    @staticmethod
    def read(data: "chameleongram.raw.reader.Reader") -> TL:
        data.__init__(gzip.decompress(Bytes.read(data)))
        return data.readtg()

    def getvalue(self) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(self.ID, False))
        data.write(Bytes.getvalue(gzip.compress(self.packed_data.write())))
        return data.getvalue()


class CoreMessage(TL):
    ID = 0x5BB8E511

    def __init__(self, msg_id: int, seqno: int, length: int, body: TL):
        self.msg_id = msg_id
        self.seqno = seqno
        self.length = length
        self.body = body

    @staticmethod
    def read(data: "chameleongram.raw.reader.Reader") -> "CoreMessage":
        msg_id = Long.read(data)
        seqno = Int.read(data)
        length = Int.read(data)
        tmp = data.__class__(data.read(length))
        body = tmp.readtg()
        return CoreMessage(msg_id=msg_id, seqno=seqno, length=length, body=body)

    def getvalue(self) -> bytes:
        data = BytesIO()
        data.write(Long.getvalue(self.msg_id))
        data.write(Int.getvalue(self.seqno))
        data.write(Int.getvalue(self.length))
        data.write(self.body.getvalue())
        return data.getvalue()

    def __str__(self):
        return get_json(self, as_string=True)

    def __repr__(self):
        return get_json(self, as_string=True)


class MsgContainer(TL):
    ID = 0x73F1F8DC

    def __init__(self, messages: List[CoreMessage]):
        self.messages = messages

    @staticmethod
    def read(data: "chameleongram.raw.reader.Reader") -> List[CoreMessage]:
        values = []

        for _ in range(Int.read(data)):
            values.append(CoreMessage.read(data))
        return MsgContainer(values)

    def getvalue(self, values: List[CoreMessage]) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(self.ID, False))
        data.write(Int.getvalue(len(values)))

        for value in values:
            data.write(value.getvalue())
        return data.getvalue()

    def __str__(self):
        return get_json(self, as_string=True)

    def __repr__(self):
        return get_json(self, as_string=True)


class FutureSalt(TL):
    ID = 0x0949D9DC

    def __init__(self, valid_since: int, valid_until: int, salt: int):
        self.valid_since = valid_since
        self.valid_until = valid_until
        self.salt = salt

    @staticmethod
    def read(data: "chameleongram.raw.reader.Reader") -> "FutureSalt":
        valid_since = Int.read(data)
        valid_until = Int.read(data)
        salt = Long.read(data)
        return FutureSalt(valid_since=valid_since, valid_until=valid_until, salt=salt)

    def __str__(self):
        return get_json(self, as_string=True)

    def __repr__(self):
        return get_json(self, as_string=True)


class FutureSalts(TL):
    ID = 0xAE500895

    def __init__(self, req_msg_id: int, now: int, salts: TL):
        self.req_msg_id = req_msg_id
        self.now = now
        self.salts = salts

    @staticmethod
    def read(data: "chameleongram.raw.reader.Reader") -> "FutureSalts":
        req_msg_id = Long.read(data)
        now = Int.read(data)
        salts = [FutureSalt.read(data) for _ in range(Int.read(data))]
        return FutureSalts(req_msg_id=req_msg_id, now=now, salts=salts)

    def __str__(self):
        return get_json(self, as_string=True)

    def __repr__(self):
        return get_json(self, as_string=True)
