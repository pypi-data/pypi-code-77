from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class File(TL):
    ID = 0x96a18d5

    def __init__(cls, type: TL, mtime: int, bytes: bytes):
        cls.type = type
        cls.mtime = mtime
        cls.bytes = bytes

    @staticmethod
    def read(data) -> "File":
        type = data.getobj()
        mtime = Int.read(data)
        bytes = Bytes.read(data)
        return File(type=type, mtime=mtime, bytes=bytes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.type.getvalue())
        data.write(Int.getvalue(cls.mtime))
        data.write(Bytes.getvalue(cls.bytes))
        return data.getvalue()


class FileCdnRedirect(TL):
    ID = 0xf18cda44

    def __init__(cls, dc_id: int, file_token: bytes, encryption_key: bytes, encryption_iv: bytes, file_hashes: List[TL]):
        cls.dc_id = dc_id
        cls.file_token = file_token
        cls.encryption_key = encryption_key
        cls.encryption_iv = encryption_iv
        cls.file_hashes = file_hashes

    @staticmethod
    def read(data) -> "FileCdnRedirect":
        dc_id = Int.read(data)
        file_token = Bytes.read(data)
        encryption_key = Bytes.read(data)
        encryption_iv = Bytes.read(data)
        file_hashes = data.getobj()
        return FileCdnRedirect(dc_id=dc_id, file_token=file_token, encryption_key=encryption_key, encryption_iv=encryption_iv, file_hashes=file_hashes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.dc_id))
        data.write(Bytes.getvalue(cls.file_token))
        data.write(Bytes.getvalue(cls.encryption_key))
        data.write(Bytes.getvalue(cls.encryption_iv))
        data.write(Vector().getvalue(cls.file_hashes))
        return data.getvalue()


class WebFile(TL):
    ID = 0x21e753bc

    def __init__(cls, size: int, mime_type: str, file_type: TL, mtime: int, bytes: bytes):
        cls.size = size
        cls.mime_type = mime_type
        cls.file_type = file_type
        cls.mtime = mtime
        cls.bytes = bytes

    @staticmethod
    def read(data) -> "WebFile":
        size = Int.read(data)
        mime_type = String.read(data)
        file_type = data.getobj()
        mtime = Int.read(data)
        bytes = Bytes.read(data)
        return WebFile(size=size, mime_type=mime_type, file_type=file_type, mtime=mtime, bytes=bytes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.size))
        data.write(String.getvalue(cls.mime_type))
        data.write(cls.file_type.getvalue())
        data.write(Int.getvalue(cls.mtime))
        data.write(Bytes.getvalue(cls.bytes))
        return data.getvalue()


class CdnFileReuploadNeeded(TL):
    ID = 0xeea8e46e

    def __init__(cls, request_token: bytes):
        cls.request_token = request_token

    @staticmethod
    def read(data) -> "CdnFileReuploadNeeded":
        request_token = Bytes.read(data)
        return CdnFileReuploadNeeded(request_token=request_token)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.request_token))
        return data.getvalue()


class CdnFile(TL):
    ID = 0xa99fca4f

    def __init__(cls, bytes: bytes):
        cls.bytes = bytes

    @staticmethod
    def read(data) -> "CdnFile":
        bytes = Bytes.read(data)
        return CdnFile(bytes=bytes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.bytes))
        return data.getvalue()
