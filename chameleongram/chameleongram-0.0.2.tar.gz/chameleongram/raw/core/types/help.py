from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class ConfigSimple(TL):
    ID = 0x5a592a6c

    def __init__(cls, date: int, expires: int, rules: List[TL]):
        cls.date = date
        cls.expires = expires
        cls.rules = rules

    @staticmethod
    def read(data) -> "ConfigSimple":
        date = Int.read(data)
        expires = Int.read(data)
        rules = data.getobj()
        return ConfigSimple(date=date, expires=expires, rules=rules)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.expires))
        data.write(Vector().getvalue(cls.rules))
        return data.getvalue()
