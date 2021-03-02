from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class SaveFilePart(TL):
    ID = 0xb304a621

    def __init__(cls, file_id: int, file_part: int, bytes: bytes):
        cls.file_id = file_id
        cls.file_part = file_part
        cls.bytes = bytes

    @staticmethod
    def read(data) -> "SaveFilePart":
        file_id = Long.read(data)
        file_part = Int.read(data)
        bytes = Bytes.read(data)
        return SaveFilePart(file_id=file_id, file_part=file_part, bytes=bytes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.file_id))
        data.write(Int.getvalue(cls.file_part))
        data.write(Bytes.getvalue(cls.bytes))
        return data.getvalue()


class GetFile(TL):
    ID = 0xb15a9afc

    def __init__(cls, location: TL, offset: int, limit: int, precise: bool = None, cdn_supported: bool = None):
        cls.precise = precise
        cls.cdn_supported = cdn_supported
        cls.location = location
        cls.offset = offset
        cls.limit = limit

    @staticmethod
    def read(data) -> "GetFile":
        flags = Int.read(data)
        precise = True if flags & 1 else False
        cdn_supported = True if flags & 2 else False
        location = data.getobj()
        offset = Int.read(data)
        limit = Int.read(data)
        return GetFile(precise=precise, cdn_supported=cdn_supported, location=location, offset=offset, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.precise is not None else 0
        flags |= 2 if cls.cdn_supported is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.location.getvalue())
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()


class SaveBigFilePart(TL):
    ID = 0xde7b673d

    def __init__(cls, file_id: int, file_part: int, file_total_parts: int, bytes: bytes):
        cls.file_id = file_id
        cls.file_part = file_part
        cls.file_total_parts = file_total_parts
        cls.bytes = bytes

    @staticmethod
    def read(data) -> "SaveBigFilePart":
        file_id = Long.read(data)
        file_part = Int.read(data)
        file_total_parts = Int.read(data)
        bytes = Bytes.read(data)
        return SaveBigFilePart(file_id=file_id, file_part=file_part, file_total_parts=file_total_parts, bytes=bytes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.file_id))
        data.write(Int.getvalue(cls.file_part))
        data.write(Int.getvalue(cls.file_total_parts))
        data.write(Bytes.getvalue(cls.bytes))
        return data.getvalue()


class GetWebFile(TL):
    ID = 0x24e6818d

    def __init__(cls, location: TL, offset: int, limit: int):
        cls.location = location
        cls.offset = offset
        cls.limit = limit

    @staticmethod
    def read(data) -> "GetWebFile":
        location = data.getobj()
        offset = Int.read(data)
        limit = Int.read(data)
        return GetWebFile(location=location, offset=offset, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.location.getvalue())
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()


class GetCdnFile(TL):
    ID = 0x2000bcc3

    def __init__(cls, file_token: bytes, offset: int, limit: int):
        cls.file_token = file_token
        cls.offset = offset
        cls.limit = limit

    @staticmethod
    def read(data) -> "GetCdnFile":
        file_token = Bytes.read(data)
        offset = Int.read(data)
        limit = Int.read(data)
        return GetCdnFile(file_token=file_token, offset=offset, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.file_token))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()


class ReuploadCdnFile(TL):
    ID = 0x9b2754a8

    def __init__(cls, file_token: bytes, request_token: bytes):
        cls.file_token = file_token
        cls.request_token = request_token

    @staticmethod
    def read(data) -> "ReuploadCdnFile":
        file_token = Bytes.read(data)
        request_token = Bytes.read(data)
        return ReuploadCdnFile(file_token=file_token, request_token=request_token)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.file_token))
        data.write(Bytes.getvalue(cls.request_token))
        return data.getvalue()


class GetCdnFileHashes(TL):
    ID = 0x4da54231

    def __init__(cls, file_token: bytes, offset: int):
        cls.file_token = file_token
        cls.offset = offset

    @staticmethod
    def read(data) -> "GetCdnFileHashes":
        file_token = Bytes.read(data)
        offset = Int.read(data)
        return GetCdnFileHashes(file_token=file_token, offset=offset)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.file_token))
        data.write(Int.getvalue(cls.offset))
        return data.getvalue()


class GetFileHashes(TL):
    ID = 0xc7025931

    def __init__(cls, location: TL, offset: int):
        cls.location = location
        cls.offset = offset

    @staticmethod
    def read(data) -> "GetFileHashes":
        location = data.getobj()
        offset = Int.read(data)
        return GetFileHashes(location=location, offset=offset)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.location.getvalue())
        data.write(Int.getvalue(cls.offset))
        return data.getvalue()
