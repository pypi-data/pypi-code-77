from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class AppUpdate(TL):
    ID = 0x1da7158f

    def __init__(cls, id: int, version: str, text: str, entities: List[TL], can_not_skip: bool = None, document: TL = None, url: str = None):
        cls.can_not_skip = can_not_skip
        cls.id = id
        cls.version = version
        cls.text = text
        cls.entities = entities
        cls.document = document
        cls.url = url

    @staticmethod
    def read(data) -> "AppUpdate":
        flags = Int.read(data)
        can_not_skip = True if flags & 1 else False
        id = Int.read(data)
        version = String.read(data)
        text = String.read(data)
        entities = data.getobj()
        document = data.getobj() if flags & 2 else None
        url = String.read(data) if flags & 4 else None
        return AppUpdate(can_not_skip=can_not_skip, id=id, version=version, text=text, entities=entities, document=document, url=url)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.can_not_skip is not None else 0
        flags |= 2 if cls.document is not None else 0
        flags |= 4 if cls.url is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        data.write(String.getvalue(cls.version))
        data.write(String.getvalue(cls.text))
        data.write(Vector().getvalue(cls.entities))
        
        if cls.document is not None:
            data.write(cls.document.getvalue())
        
        if cls.url is not None:
            data.write(String.getvalue(cls.url))
        return data.getvalue()


class NoAppUpdate(TL):
    ID = 0xc45a6536

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "NoAppUpdate":
        
        return NoAppUpdate()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InviteText(TL):
    ID = 0x18cb9f78

    def __init__(cls, message: str):
        cls.message = message

    @staticmethod
    def read(data) -> "InviteText":
        message = String.read(data)
        return InviteText(message=message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.message))
        return data.getvalue()


class Support(TL):
    ID = 0x17c6b5f6

    def __init__(cls, phone_number: str, user: TL):
        cls.phone_number = phone_number
        cls.user = user

    @staticmethod
    def read(data) -> "Support":
        phone_number = String.read(data)
        user = data.getobj()
        return Support(phone_number=phone_number, user=user)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone_number))
        data.write(cls.user.getvalue())
        return data.getvalue()


class TermsOfService(TL):
    ID = 0x780a0310

    def __init__(cls, id: TL, text: str, entities: List[TL], popup: bool = None, min_age_confirm: int = None):
        cls.popup = popup
        cls.id = id
        cls.text = text
        cls.entities = entities
        cls.min_age_confirm = min_age_confirm

    @staticmethod
    def read(data) -> "TermsOfService":
        flags = Int.read(data)
        popup = True if flags & 1 else False
        id = data.getobj()
        text = String.read(data)
        entities = data.getobj()
        min_age_confirm = Int.read(data) if flags & 2 else None
        return TermsOfService(popup=popup, id=id, text=text, entities=entities, min_age_confirm=min_age_confirm)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.popup is not None else 0
        flags |= 2 if cls.min_age_confirm is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.id.getvalue())
        data.write(String.getvalue(cls.text))
        data.write(Vector().getvalue(cls.entities))
        
        if cls.min_age_confirm is not None:
            data.write(Int.getvalue(cls.min_age_confirm))
        return data.getvalue()


class RecentMeUrls(TL):
    ID = 0xe0310d7

    def __init__(cls, urls: List[TL], chats: List[TL], users: List[TL]):
        cls.urls = urls
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "RecentMeUrls":
        urls = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return RecentMeUrls(urls=urls, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.urls))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class TermsOfServiceUpdateEmpty(TL):
    ID = 0xe3309f7f

    def __init__(cls, expires: int):
        cls.expires = expires

    @staticmethod
    def read(data) -> "TermsOfServiceUpdateEmpty":
        expires = Int.read(data)
        return TermsOfServiceUpdateEmpty(expires=expires)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.expires))
        return data.getvalue()


class TermsOfServiceUpdate(TL):
    ID = 0x28ecf961

    def __init__(cls, expires: int, terms_of_service: TL):
        cls.expires = expires
        cls.terms_of_service = terms_of_service

    @staticmethod
    def read(data) -> "TermsOfServiceUpdate":
        expires = Int.read(data)
        terms_of_service = data.getobj()
        return TermsOfServiceUpdate(expires=expires, terms_of_service=terms_of_service)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.expires))
        data.write(cls.terms_of_service.getvalue())
        return data.getvalue()


class DeepLinkInfoEmpty(TL):
    ID = 0x66afa166

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "DeepLinkInfoEmpty":
        
        return DeepLinkInfoEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class DeepLinkInfo(TL):
    ID = 0x6a4ee832

    def __init__(cls, message: str, update_app: bool = None, entities: List[TL] = None):
        cls.update_app = update_app
        cls.message = message
        cls.entities = entities

    @staticmethod
    def read(data) -> "DeepLinkInfo":
        flags = Int.read(data)
        update_app = True if flags & 1 else False
        message = String.read(data)
        entities = data.getobj() if flags & 2 else []
        return DeepLinkInfo(update_app=update_app, message=message, entities=entities)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.update_app is not None else 0
        flags |= 2 if cls.entities is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.message))
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        return data.getvalue()


class PassportConfigNotModified(TL):
    ID = 0xbfb9f457

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PassportConfigNotModified":
        
        return PassportConfigNotModified()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PassportConfig(TL):
    ID = 0xa098d6af

    def __init__(cls, hash: int, countries_langs: TL):
        cls.hash = hash
        cls.countries_langs = countries_langs

    @staticmethod
    def read(data) -> "PassportConfig":
        hash = Int.read(data)
        countries_langs = data.getobj()
        return PassportConfig(hash=hash, countries_langs=countries_langs)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        data.write(cls.countries_langs.getvalue())
        return data.getvalue()


class SupportName(TL):
    ID = 0x8c05f1c9

    def __init__(cls, name: str):
        cls.name = name

    @staticmethod
    def read(data) -> "SupportName":
        name = String.read(data)
        return SupportName(name=name)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.name))
        return data.getvalue()


class UserInfoEmpty(TL):
    ID = 0xf3ae2eed

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UserInfoEmpty":
        
        return UserInfoEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UserInfo(TL):
    ID = 0x1eb3758

    def __init__(cls, message: str, entities: List[TL], author: str, date: int):
        cls.message = message
        cls.entities = entities
        cls.author = author
        cls.date = date

    @staticmethod
    def read(data) -> "UserInfo":
        message = String.read(data)
        entities = data.getobj()
        author = String.read(data)
        date = Int.read(data)
        return UserInfo(message=message, entities=entities, author=author, date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.message))
        data.write(Vector().getvalue(cls.entities))
        data.write(String.getvalue(cls.author))
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class PromoDataEmpty(TL):
    ID = 0x98f6ac75

    def __init__(cls, expires: int):
        cls.expires = expires

    @staticmethod
    def read(data) -> "PromoDataEmpty":
        expires = Int.read(data)
        return PromoDataEmpty(expires=expires)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.expires))
        return data.getvalue()


class PromoData(TL):
    ID = 0x8c39793f

    def __init__(cls, expires: int, peer: TL, chats: List[TL], users: List[TL], proxy: bool = None, psa_type: str = None, psa_message: str = None):
        cls.proxy = proxy
        cls.expires = expires
        cls.peer = peer
        cls.chats = chats
        cls.users = users
        cls.psa_type = psa_type
        cls.psa_message = psa_message

    @staticmethod
    def read(data) -> "PromoData":
        flags = Int.read(data)
        proxy = True if flags & 1 else False
        expires = Int.read(data)
        peer = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        psa_type = String.read(data) if flags & 2 else None
        psa_message = String.read(data) if flags & 4 else None
        return PromoData(proxy=proxy, expires=expires, peer=peer, chats=chats, users=users, psa_type=psa_type, psa_message=psa_message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.proxy is not None else 0
        flags |= 2 if cls.psa_type is not None else 0
        flags |= 4 if cls.psa_message is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.expires))
        data.write(cls.peer.getvalue())
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        
        if cls.psa_type is not None:
            data.write(String.getvalue(cls.psa_type))
        
        if cls.psa_message is not None:
            data.write(String.getvalue(cls.psa_message))
        return data.getvalue()


class CountryCode(TL):
    ID = 0x4203c5ef

    def __init__(cls, country_code: str, prefixes: List[str] = None, patterns: List[str] = None):
        cls.country_code = country_code
        cls.prefixes = prefixes
        cls.patterns = patterns

    @staticmethod
    def read(data) -> "CountryCode":
        flags = Int.read(data)
        country_code = String.read(data)
        prefixes = String.read(data) if flags & 1 else None
        patterns = String.read(data) if flags & 2 else None
        return CountryCode(country_code=country_code, prefixes=prefixes, patterns=patterns)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.prefixes is not None else 0
        flags |= 2 if cls.patterns is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.country_code))
        
        if cls.prefixes is not None:
            data.write(Vector().getvalue(cls.prefixes, String))
        
        if cls.patterns is not None:
            data.write(Vector().getvalue(cls.patterns, String))
        return data.getvalue()


class Country(TL):
    ID = 0xc3878e23

    def __init__(cls, iso2: str, default_name: str, country_codes: List[TL], hidden: bool = None, name: str = None):
        cls.hidden = hidden
        cls.iso2 = iso2
        cls.default_name = default_name
        cls.name = name
        cls.country_codes = country_codes

    @staticmethod
    def read(data) -> "Country":
        flags = Int.read(data)
        hidden = True if flags & 1 else False
        iso2 = String.read(data)
        default_name = String.read(data)
        name = String.read(data) if flags & 2 else None
        country_codes = data.getobj()
        return Country(hidden=hidden, iso2=iso2, default_name=default_name, name=name, country_codes=country_codes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.hidden is not None else 0
        flags |= 2 if cls.name is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.iso2))
        data.write(String.getvalue(cls.default_name))
        
        if cls.name is not None:
            data.write(String.getvalue(cls.name))
        data.write(Vector().getvalue(cls.country_codes))
        return data.getvalue()


class CountriesListNotModified(TL):
    ID = 0x93cc1f32

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "CountriesListNotModified":
        
        return CountriesListNotModified()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class CountriesList(TL):
    ID = 0x87d0759e

    def __init__(cls, countries: List[TL], hash: int):
        cls.countries = countries
        cls.hash = hash

    @staticmethod
    def read(data) -> "CountriesList":
        countries = data.getobj()
        hash = Int.read(data)
        return CountriesList(countries=countries, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.countries))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()
