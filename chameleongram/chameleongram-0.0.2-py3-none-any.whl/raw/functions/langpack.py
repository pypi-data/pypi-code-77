from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class GetLangPack(TL):
    ID = 0xf2f2330a

    def __init__(cls, lang_pack: str, lang_code: str):
        cls.lang_pack = lang_pack
        cls.lang_code = lang_code

    @staticmethod
    def read(data) -> "GetLangPack":
        lang_pack = String.read(data)
        lang_code = String.read(data)
        return GetLangPack(lang_pack=lang_pack, lang_code=lang_code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.lang_pack))
        data.write(String.getvalue(cls.lang_code))
        return data.getvalue()


class GetStrings(TL):
    ID = 0xefea3803

    def __init__(cls, lang_pack: str, lang_code: str, keys: List[str]):
        cls.lang_pack = lang_pack
        cls.lang_code = lang_code
        cls.keys = keys

    @staticmethod
    def read(data) -> "GetStrings":
        lang_pack = String.read(data)
        lang_code = String.read(data)
        keys = data.getobj(String)
        return GetStrings(lang_pack=lang_pack, lang_code=lang_code, keys=keys)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.lang_pack))
        data.write(String.getvalue(cls.lang_code))
        data.write(Vector().getvalue(cls.keys, String))
        return data.getvalue()


class GetDifference(TL):
    ID = 0xcd984aa5

    def __init__(cls, lang_pack: str, lang_code: str, from_version: int):
        cls.lang_pack = lang_pack
        cls.lang_code = lang_code
        cls.from_version = from_version

    @staticmethod
    def read(data) -> "GetDifference":
        lang_pack = String.read(data)
        lang_code = String.read(data)
        from_version = Int.read(data)
        return GetDifference(lang_pack=lang_pack, lang_code=lang_code, from_version=from_version)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.lang_pack))
        data.write(String.getvalue(cls.lang_code))
        data.write(Int.getvalue(cls.from_version))
        return data.getvalue()


class GetLanguages(TL):
    ID = 0x42c6978f

    def __init__(cls, lang_pack: str):
        cls.lang_pack = lang_pack

    @staticmethod
    def read(data) -> "GetLanguages":
        lang_pack = String.read(data)
        return GetLanguages(lang_pack=lang_pack)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.lang_pack))
        return data.getvalue()


class GetLanguage(TL):
    ID = 0x6a596502

    def __init__(cls, lang_pack: str, lang_code: str):
        cls.lang_pack = lang_pack
        cls.lang_code = lang_code

    @staticmethod
    def read(data) -> "GetLanguage":
        lang_pack = String.read(data)
        lang_code = String.read(data)
        return GetLanguage(lang_pack=lang_pack, lang_code=lang_code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.lang_pack))
        data.write(String.getvalue(cls.lang_code))
        return data.getvalue()
