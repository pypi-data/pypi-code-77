from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class GetUsers(TL):
    ID = 0xd91a548

    def __init__(cls, id: List[TL]):
        cls.id = id

    @staticmethod
    def read(data) -> "GetUsers":
        id = data.getobj()
        return GetUsers(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.id))
        return data.getvalue()


class GetFullUser(TL):
    ID = 0xca30a5b1

    def __init__(cls, id: TL):
        cls.id = id

    @staticmethod
    def read(data) -> "GetFullUser":
        id = data.getobj()
        return GetFullUser(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.id.getvalue())
        return data.getvalue()


class SetSecureValueErrors(TL):
    ID = 0x90c894b5

    def __init__(cls, id: TL, errors: List[TL]):
        cls.id = id
        cls.errors = errors

    @staticmethod
    def read(data) -> "SetSecureValueErrors":
        id = data.getobj()
        errors = data.getobj()
        return SetSecureValueErrors(id=id, errors=errors)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.id.getvalue())
        data.write(Vector().getvalue(cls.errors))
        return data.getvalue()
