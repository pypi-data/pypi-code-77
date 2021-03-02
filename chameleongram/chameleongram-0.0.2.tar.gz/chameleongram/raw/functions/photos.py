from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class UpdateProfilePhoto(TL):
    ID = 0x72d4742c

    def __init__(cls, id: TL):
        cls.id = id

    @staticmethod
    def read(data) -> "UpdateProfilePhoto":
        id = data.getobj()
        return UpdateProfilePhoto(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.id.getvalue())
        return data.getvalue()


class UploadProfilePhoto(TL):
    ID = 0x89f30f69

    def __init__(cls, file: TL = None, video: TL = None, video_start_ts: float = None):
        cls.file = file
        cls.video = video
        cls.video_start_ts = video_start_ts

    @staticmethod
    def read(data) -> "UploadProfilePhoto":
        flags = Int.read(data)
        file = data.getobj() if flags & 1 else None
        video = data.getobj() if flags & 2 else None
        video_start_ts = Double.read(data) if flags & 4 else None
        return UploadProfilePhoto(file=file, video=video, video_start_ts=video_start_ts)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.file is not None else 0
        flags |= 2 if cls.video is not None else 0
        flags |= 4 if cls.video_start_ts is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.file is not None:
            data.write(cls.file.getvalue())
        
        if cls.video is not None:
            data.write(cls.video.getvalue())
        
        if cls.video_start_ts is not None:
            data.write(Double.getvalue(cls.video_start_ts))
        return data.getvalue()


class DeletePhotos(TL):
    ID = 0x87cf7f2f

    def __init__(cls, id: List[TL]):
        cls.id = id

    @staticmethod
    def read(data) -> "DeletePhotos":
        id = data.getobj()
        return DeletePhotos(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.id))
        return data.getvalue()


class GetUserPhotos(TL):
    ID = 0x91cd32a8

    def __init__(cls, user_id: TL, offset: int, max_id: int, limit: int):
        cls.user_id = user_id
        cls.offset = offset
        cls.max_id = max_id
        cls.limit = limit

    @staticmethod
    def read(data) -> "GetUserPhotos":
        user_id = data.getobj()
        offset = Int.read(data)
        max_id = Long.read(data)
        limit = Int.read(data)
        return GetUserPhotos(user_id=user_id, offset=offset, max_id=max_id, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.user_id.getvalue())
        data.write(Int.getvalue(cls.offset))
        data.write(Long.getvalue(cls.max_id))
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()
