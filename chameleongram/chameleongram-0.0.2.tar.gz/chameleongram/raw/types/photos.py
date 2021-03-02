from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class Photos(TL):
    ID = 0x8dca6aa5

    def __init__(cls, photos: List[TL], users: List[TL]):
        cls.photos = photos
        cls.users = users

    @staticmethod
    def read(data) -> "Photos":
        photos = data.getobj()
        users = data.getobj()
        return Photos(photos=photos, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.photos))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class PhotosSlice(TL):
    ID = 0x15051f54

    def __init__(cls, count: int, photos: List[TL], users: List[TL]):
        cls.count = count
        cls.photos = photos
        cls.users = users

    @staticmethod
    def read(data) -> "PhotosSlice":
        count = Int.read(data)
        photos = data.getobj()
        users = data.getobj()
        return PhotosSlice(count=count, photos=photos, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.count))
        data.write(Vector().getvalue(cls.photos))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class Photo(TL):
    ID = 0x20212ca8

    def __init__(cls, photo: TL, users: List[TL]):
        cls.photo = photo
        cls.users = users

    @staticmethod
    def read(data) -> "Photo":
        photo = data.getobj()
        users = data.getobj()
        return Photo(photo=photo, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.photo.getvalue())
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()
