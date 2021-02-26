
import os
import sys
import uuid
import secrets
from hashlib import sha256
import binascii
from enum import Enum

import ecdsa
import cbor

import mtsmultitool.bsdiff as bsdiff

from .device_types import DeviceProperties

DIFF_MAGIC = 'MTS/BSDIFF/LZ4'
COMPR_MAGIC = 'MTS/LZ4'
BLOCK_SIZE = 512


class FirmwareUpgrade:
    class Type(Enum):
        PLAIN = 0
        PATCH = 1
        COMPRESSED = 2

    def __init__(self, image: bytes, size: int, digest: bytes, type: Type):
        self.image = image
        self.size = size
        self.digest = digest
        self.type = type


def export_key_pair(sk: ecdsa.SigningKey, name: str, out_dir: str = None) -> [str, str]:
    """
    Write keys to files.  Writes the private/signing key to <name>.prv and public/verifying key to <name>.pub

    :param sk: Private/signing key
    :param name: Name of key
    :param out_dir: Optional destination directory
    :return: Private and public key file names
    """
    if out_dir is None:
        out_dir = os.getcwd()
    full_path = os.path.join(out_dir, name)

    with open(full_path + '.prv', 'wb') as fd:
        fd.write(sk.to_pem())

    vk = pub_key_from_private(sk)
    with open(full_path + '.pub', 'wb') as fd:
        fd.write(vk)

    return full_path + '.prv', full_path + '.pub'


def import_key_pem(file: str) -> ecdsa.SigningKey:
    """
    Import keys from a private key PEM file.

    :param file: Path to private key file.
    :return: ECDSA signing key
    """
    with open(file, 'rb') as fd:
        sk, vk = load_keys_from_private_pem(fd.read())
        return sk


def gen_key_pair() -> [ecdsa.SigningKey, ecdsa.VerifyingKey]:
    """
    Generate a ECDSA key pair using NIST256 curve.

    :return: ECDSA signing key and verifying key
    """
    def entropy_source(size):
        return bytes([secrets.choice(range(0xFF)) for i in range(size)])
    # Generate a key pair using NIST256
    sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p, hashfunc=sha256, entropy=entropy_source)
    return sk, sk.verifying_key


def pub_key_from_private(sk: ecdsa.SigningKey) -> bytes:
    """
    Get the public/verifying key from a private/signing key.

    :param sk: Signing key
    :return: Verifying key in uncompressed format
    """
    # Get public key in uncompressed format
    return sk.verifying_key.to_string(encoding="uncompressed")


def load_keys_from_private_pem(sk_str: bytes) -> [ecdsa.SigningKey, ecdsa.VerifyingKey]:
    """
    Create key objects from a PEM formatted byte string.

    :param sk_str: PEM formatted private key
    :return: ECDSA signing key and verifying key
    """
    sk = ecdsa.SigningKey.from_pem(sk_str, hashfunc=sha256)
    vk = pub_key_from_private(sk)
    return sk, vk


def sign_manifest(sk: ecdsa.SigningKey, suit: dict) -> dict:
    """
    Add a COSE authentication wrapper to a SUIT manifest.

    :param sk: ECDSA signing key
    :param suit: SUIT manifest
    :return: SUIT manifest with COSE authentication wrapper
    """
    # Encode manifest as CBOR and compute SHA256 digest
    suit_enc = cbor.dumps({3: suit[3]})[1:]
    suit_digest = sha256(suit_enc).digest()

    # Sign the digest and encode in DER format
    suit_sig = sk.sign_digest(suit_digest, sigencode=ecdsa.util.sigencode_der)
    cose = {
        2: [  # authentication-wrapper
            {1: -7},  # protected alg: ES256
            {},  # unprotected
            [  # payload
                2,  # algorithm-id sha256
                suit_digest  # payload-digest
            ],
            suit_sig  # signature
        ],
        3: suit[3],     # suit-manifest
        13: suit[13]    # suit-text
    }

    return cose


def generate_manifest(fw_upgrade: FirmwareUpgrade, version: list, device_properties: DeviceProperties,
                      description: str or None = None, required_version: list or None = None,
                      vendor_name: str = None, model: str = None, vendor_dns: str = None) -> dict:
    """
    Generate a SUIT manifest for a firmware upgrade image.

    :param fw_upgrade: Firmware upgrade
    :param required_version: Version of firmware to be patched
    :param version: Version of update as a list of four integers
    :param device_properties: Device properties based on the series
    :param description: Description of the upgrade
    :param required_version: Version of firmware that must be present on the device (used for patches)
    :param vendor_name: Name of the vendor, defaults to 'Multi-Tech System Inc.' if `None`
    :param model: Target model, defaults to device_properties.name if `None`
    :param vendor_dns: Optional vendor DNS used to generate vendor_id using UUID5, if None will use 'multitech.com'
    :return: SUIT manifest
    """
    if fw_upgrade.type == FirmwareUpgrade.Type.PATCH and required_version is None:
        raise ValueError("Required version must be specified for delta upgrades")

    if version is None:
        raise ValueError("Version must be specified")

    if vendor_name is None:
        vendor_name = 'Multi-Tech System Inc.'

    install_directives = {21: "file:///fw_upgrade.bin"}
    if fw_upgrade.type == FirmwareUpgrade.Type.PATCH:
        install_directives[20] = 1
    elif fw_upgrade.type == FirmwareUpgrade.Type.COMPRESSED:
        install_directives[19] = 4

    if model is None:
        model = device_properties.series

    if vendor_dns is None:
        vendor_dns = 'multitech.com'

    vendor_id = uuid.uuid5(uuid.NAMESPACE_DNS, vendor_dns)
    class_id = uuid.uuid3(vendor_id, model)

    common_directives = {
        1: vendor_id.bytes,
        2: class_id.bytes,
        3: [
            2,
            fw_upgrade.digest
        ],
        14: fw_upgrade.size
    }

    common_sequence = [
        20,     # directive-override-parameters
        common_directives,
        1, 0xf6,    # condition-vendor-identifier
        2, 0xf6     # condition-class-identifier
    ]

    if required_version is not None:
        common_directives[28] = [   # version
            3,  # comparison-type equal
            required_version
        ]
        common_sequence.extend([28, 0xf6])  # condition-version

    # Convert version list to string
    version_str = ''
    for i in range(len(version)):
        if version[i] == -1:
            version_str = version_str.rstrip('.') + '-rc'
        elif version[i] == -2:
            version_str = version_str.rstrip('.') + '-beta'
        elif version[i] == -3:
            version_str = version_str.rstrip('.') + '-alpha'
        else:
            version_str += str(version[i])
            if i < (len(version) - 1):
                version_str += '.'

    if len(version) == 1:
        version_str += '.0'


    # suit-text
    text = {
        13: {
            1: vendor_name,                 # suit-text-vendor-name
            2: device_properties.series,    # suit-text-model-name
            3: vendor_dns,                  # suit-text-vendor-domain
            4: model,                       # suit-text-model-info
            5: description,                 # suit-text-component-description
            6: version_str,                 # suit-text-component-version
        }

    }

    # Encode text as CBOR and compute SHA256 digest
    text_enc = cbor.dumps(text)[1:]
    text_digest = sha256(text_enc).digest()

    suit = {
        3: {  # manifest
            1: 1,  # manifest-version
            2: 1,  # manifest-sequence-number
            3: {  # common
                2: [[b'\0']],  # components
                4: common_sequence
            },
            9: [  # install
                19, install_directives,  # directive-set-parameters
                23, 0xf6  # directive-copy
            ],
            10: [  # validate
                3, 0xf6  # condition-image-match
            ],
            12: [  # run
                23, 0xf6  # directive-run
            ],
            13: [
                2,          # algorithm-id "sha256"
                text_digest
            ]
        },
        13: text[13]    # suit-text
    }

    return suit


def encode_manifest(manifest: dict) -> bytes:
    """
    Encode a manifest as CBOR.

    :param manifest: SUIT manifest
    :return: CBOR encoded manifest
    """
    return cbor.dumps(manifest)


def combine(file: str, manifest: dict, upgrade_image: bytes, append_crc: bool, app_offset: int):
    """
    Combine manifest and image and write to file, optionally add a CRC32 to the end.

    :param file: Path to output file
    :param manifest: SUIT manifest
    :param upgrade_image: Firmware upgrade image
    :param append_crc: Set to true to append a CRC32 to the end of output
    :param app_offset: Offset into image to start
    :return: None
    """
    if app_offset is None:
        app_offset = 0
    with open(file, 'wb') as f:
        crc = 0
        if manifest is not None:
            mf_enc = encode_manifest(manifest)
            f.write(mf_enc)
            crc = binascii.crc32(mf_enc)
        image_mv = memoryview(upgrade_image)
        f.write(image_mv[app_offset:])
        crc = binascii.crc32(image_mv[app_offset:], crc) & 0xffffffff
        if append_crc:
            f.write(crc.to_bytes(4, byteorder='little'))


def calculate_crc(image: bytes) -> bytes:
    """
    Calculate CRC32 of image.

    :param image: Target image
    :return: CRC32 as little-endian formatted bytes
    """
    crc = binascii.crc32(image) & 0xffffffff
    return crc.to_bytes(4, byteorder='little')


def digest(image: bytes, app_offset: int) -> [int, bytes]:
    """
    Compute the SHA256 digest of an image.

    :param image: Target image
    :param app_offset: Offset into image to start
    :return: The image size from the offset and the computed digest
    """
    image_mv = memoryview(image)
    image_size = len(image_mv[app_offset:])
    image_digest = sha256(image_mv[app_offset:]).digest()
    return image_size, image_digest


def create_patch(origin: bytes, upgrade: bytes, app_offset: int) -> FirmwareUpgrade:
    """
    Generate a patch using BSDIFF.

    :param origin: Firmware image being upgraded
    :param upgrade: Destination firmware image
    :param app_offset: Offset into firmware images to start
    :return: Firmware upgrade with the patch image, size of upgrade firmware, and SHA256 digest of upgrade firmware
    """
    if app_offset is None:
        app_offset = 0
    origin_mv = memoryview(origin)
    upgrade_mv = memoryview(upgrade)

    image_size = len(upgrade_mv[app_offset:])
    image_digest = sha256(upgrade_mv[app_offset:]).digest()

    patch_image = bsdiff.diff(origin_mv[app_offset:].tobytes(), upgrade_mv[app_offset:].tobytes(), BLOCK_SIZE, DIFF_MAGIC)

    return FirmwareUpgrade(patch_image, image_size, image_digest, FirmwareUpgrade.Type.PATCH)


def compress(upgrade: bytes, app_offset: int) -> FirmwareUpgrade:
    """
    Compress a firmware image using LZ4 algorithm.

    :param upgrade: Firmware image to compress
    :param app_offset: Offset into image to start
    :return: Firmware upgrade with the compress image, size of upgrade firmware, and SHA256 digest of upgrade firmware
    """
    if app_offset is None:
        app_offset = 0
    upgrade_mv = memoryview(upgrade)

    image_size = len(upgrade_mv[app_offset:])
    image_digest = sha256(upgrade_mv[app_offset:]).digest()

    compr_image = bsdiff.compress(upgrade_mv[app_offset:].tobytes(), BLOCK_SIZE, COMPR_MAGIC)

    return FirmwareUpgrade(compr_image, image_size, image_digest, FirmwareUpgrade.Type.COMPRESSED)


def plain(upgrade: bytes, app_offset: int) -> FirmwareUpgrade:
    """
    Create a firmware upgrade from an image.

    :param upgrade: Firmware image
    :param app_offset: Offset into image to start
    :return: Firmware upgrade with the image, size of upgrade firmware, and SHA256 digest of upgrade firmware
    """
    if app_offset is None:
        app_offset = 0
    upgrade_mv = memoryview(upgrade)

    image_size = len(upgrade_mv[app_offset:])
    image_digest = sha256(upgrade_mv[app_offset:]).digest()

    return FirmwareUpgrade(bytes(upgrade_mv[app_offset:]), image_size, image_digest, FirmwareUpgrade.Type.PLAIN)


def verify_manifest(image: bytes, pub_key: bytes or ecdsa.VerifyingKey) -> [bool, bool]:
    """
    Verify signed manifest of image.

    :param image: Image with COSE signed manifest
    :param pub_key: Public key
    :return: Results of signature verification and manifest digest comparison
    """
    mf = cbor.loads(image)
    if type(mf) is not dict:
        raise Exception('Image does not have a manifest to verify.')
    if 2 in mf:
        if type(pub_key) == ecdsa.VerifyingKey:
            vk = pub_key
        else:
            vk = ecdsa.VerifyingKey.from_string(pub_key, curve=ecdsa.NIST256p, hashfunc=sha256)
        signed_digest = mf[2][2][1]     # Get signed digest from COSE
        signature = mf[2][3]            # Get signature of digest
        act_digest = sha256(cbor.dumps({3: mf[3]})[1:]).digest()
        digest_match = act_digest == signed_digest
        try:
            vk.verify_digest(signature, signed_digest, sigdecode=ecdsa.util.sigdecode_der)
            sig_verified = True
        except (ecdsa.keys.BadSignatureError, ecdsa.keys.BadDigestError):
            sig_verified = False

        return sig_verified, digest_match
    else:
        raise Exception('Image manifest does not contain COSE authentication wrapper.')
