from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class GetConfig(TL):
    ID = 0xc4f9186b

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetConfig":
        
        return GetConfig()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetNearestDc(TL):
    ID = 0x1fb33026

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetNearestDc":
        
        return GetNearestDc()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetAppUpdate(TL):
    ID = 0x522d5a7d

    def __init__(cls, source: str):
        cls.source = source

    @staticmethod
    def read(data) -> "GetAppUpdate":
        source = String.read(data)
        return GetAppUpdate(source=source)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.source))
        return data.getvalue()


class GetInviteText(TL):
    ID = 0x4d392343

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetInviteText":
        
        return GetInviteText()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetSupport(TL):
    ID = 0x9cdf08cd

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetSupport":
        
        return GetSupport()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetAppChangelog(TL):
    ID = 0x9010ef6f

    def __init__(cls, prev_app_version: str):
        cls.prev_app_version = prev_app_version

    @staticmethod
    def read(data) -> "GetAppChangelog":
        prev_app_version = String.read(data)
        return GetAppChangelog(prev_app_version=prev_app_version)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.prev_app_version))
        return data.getvalue()


class SetBotUpdatesStatus(TL):
    ID = 0xec22cfcd

    def __init__(cls, pending_updates_count: int, message: str):
        cls.pending_updates_count = pending_updates_count
        cls.message = message

    @staticmethod
    def read(data) -> "SetBotUpdatesStatus":
        pending_updates_count = Int.read(data)
        message = String.read(data)
        return SetBotUpdatesStatus(pending_updates_count=pending_updates_count, message=message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.pending_updates_count))
        data.write(String.getvalue(cls.message))
        return data.getvalue()


class GetCdnConfig(TL):
    ID = 0x52029342

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetCdnConfig":
        
        return GetCdnConfig()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetRecentMeUrls(TL):
    ID = 0x3dc0f114

    def __init__(cls, referer: str):
        cls.referer = referer

    @staticmethod
    def read(data) -> "GetRecentMeUrls":
        referer = String.read(data)
        return GetRecentMeUrls(referer=referer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.referer))
        return data.getvalue()


class GetTermsOfServiceUpdate(TL):
    ID = 0x2ca51fd1

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetTermsOfServiceUpdate":
        
        return GetTermsOfServiceUpdate()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class AcceptTermsOfService(TL):
    ID = 0xee72f79a

    def __init__(cls, id: TL):
        cls.id = id

    @staticmethod
    def read(data) -> "AcceptTermsOfService":
        id = data.getobj()
        return AcceptTermsOfService(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.id.getvalue())
        return data.getvalue()


class GetDeepLinkInfo(TL):
    ID = 0x3fedc75f

    def __init__(cls, path: str):
        cls.path = path

    @staticmethod
    def read(data) -> "GetDeepLinkInfo":
        path = String.read(data)
        return GetDeepLinkInfo(path=path)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.path))
        return data.getvalue()


class GetAppConfig(TL):
    ID = 0x98914110

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetAppConfig":
        
        return GetAppConfig()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SaveAppLog(TL):
    ID = 0x6f02f748

    def __init__(cls, events: List[TL]):
        cls.events = events

    @staticmethod
    def read(data) -> "SaveAppLog":
        events = data.getobj()
        return SaveAppLog(events=events)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.events))
        return data.getvalue()


class GetPassportConfig(TL):
    ID = 0xc661ad08

    def __init__(cls, hash: int):
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetPassportConfig":
        hash = Int.read(data)
        return GetPassportConfig(hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class GetSupportName(TL):
    ID = 0xd360e72c

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetSupportName":
        
        return GetSupportName()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetUserInfo(TL):
    ID = 0x38a08d3

    def __init__(cls, user_id: TL):
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "GetUserInfo":
        user_id = data.getobj()
        return GetUserInfo(user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.user_id.getvalue())
        return data.getvalue()


class EditUserInfo(TL):
    ID = 0x66b91b70

    def __init__(cls, user_id: TL, message: str, entities: List[TL]):
        cls.user_id = user_id
        cls.message = message
        cls.entities = entities

    @staticmethod
    def read(data) -> "EditUserInfo":
        user_id = data.getobj()
        message = String.read(data)
        entities = data.getobj()
        return EditUserInfo(user_id=user_id, message=message, entities=entities)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.user_id.getvalue())
        data.write(String.getvalue(cls.message))
        data.write(Vector().getvalue(cls.entities))
        return data.getvalue()


class GetPromoData(TL):
    ID = 0xc0977421

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetPromoData":
        
        return GetPromoData()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class HidePromoData(TL):
    ID = 0x1e251c95

    def __init__(cls, peer: TL):
        cls.peer = peer

    @staticmethod
    def read(data) -> "HidePromoData":
        peer = data.getobj()
        return HidePromoData(peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class DismissSuggestion(TL):
    ID = 0xf50dbaa1

    def __init__(cls, peer: TL, suggestion: str):
        cls.peer = peer
        cls.suggestion = suggestion

    @staticmethod
    def read(data) -> "DismissSuggestion":
        peer = data.getobj()
        suggestion = String.read(data)
        return DismissSuggestion(peer=peer, suggestion=suggestion)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(String.getvalue(cls.suggestion))
        return data.getvalue()


class GetCountriesList(TL):
    ID = 0x735787a8

    def __init__(cls, lang_code: str, hash: int):
        cls.lang_code = lang_code
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetCountriesList":
        lang_code = String.read(data)
        hash = Int.read(data)
        return GetCountriesList(lang_code=lang_code, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.lang_code))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()
