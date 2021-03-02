from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class PrivacyRules(TL):
    ID = 0x50a04e45

    def __init__(cls, rules: List[TL], chats: List[TL], users: List[TL]):
        cls.rules = rules
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "PrivacyRules":
        rules = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return PrivacyRules(rules=rules, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.rules))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class Authorizations(TL):
    ID = 0x1250abde

    def __init__(cls, authorizations: List[TL]):
        cls.authorizations = authorizations

    @staticmethod
    def read(data) -> "Authorizations":
        authorizations = data.getobj()
        return Authorizations(authorizations=authorizations)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.authorizations))
        return data.getvalue()


class Password(TL):
    ID = 0xad2641f8

    def __init__(cls, new_algo: TL, new_secure_algo: TL, secure_random: bytes, has_recovery: bool = None, has_secure_values: bool = None, has_password: bool = None, current_algo: TL = None, srp_B: bytes = None, srp_id: int = None, hint: str = None, email_unconfirmed_pattern: str = None):
        cls.has_recovery = has_recovery
        cls.has_secure_values = has_secure_values
        cls.has_password = has_password
        cls.current_algo = current_algo
        cls.srp_B = srp_B
        cls.srp_id = srp_id
        cls.hint = hint
        cls.email_unconfirmed_pattern = email_unconfirmed_pattern
        cls.new_algo = new_algo
        cls.new_secure_algo = new_secure_algo
        cls.secure_random = secure_random

    @staticmethod
    def read(data) -> "Password":
        flags = Int.read(data)
        has_recovery = True if flags & 1 else False
        has_secure_values = True if flags & 2 else False
        has_password = True if flags & 4 else False
        current_algo = data.getobj() if flags & 4 else None
        srp_B = Bytes.read(data) if flags & 4 else None
        srp_id = Long.read(data) if flags & 4 else None
        hint = String.read(data) if flags & 8 else None
        email_unconfirmed_pattern = String.read(data) if flags & 16 else None
        new_algo = data.getobj()
        new_secure_algo = data.getobj()
        secure_random = Bytes.read(data)
        return Password(has_recovery=has_recovery, has_secure_values=has_secure_values, has_password=has_password, current_algo=current_algo, srp_B=srp_B, srp_id=srp_id, hint=hint, email_unconfirmed_pattern=email_unconfirmed_pattern, new_algo=new_algo, new_secure_algo=new_secure_algo, secure_random=secure_random)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.has_recovery is not None else 0
        flags |= 2 if cls.has_secure_values is not None else 0
        flags |= 4 if cls.has_password is not None else 0
        flags |= 4 if cls.current_algo is not None else 0
        flags |= 4 if cls.srp_B is not None else 0
        flags |= 4 if cls.srp_id is not None else 0
        flags |= 8 if cls.hint is not None else 0
        flags |= 16 if cls.email_unconfirmed_pattern is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.current_algo is not None:
            data.write(cls.current_algo.getvalue())
        
        if cls.srp_B is not None:
            data.write(Bytes.getvalue(cls.srp_B))
        
        if cls.srp_id is not None:
            data.write(Long.getvalue(cls.srp_id))
        
        if cls.hint is not None:
            data.write(String.getvalue(cls.hint))
        
        if cls.email_unconfirmed_pattern is not None:
            data.write(String.getvalue(cls.email_unconfirmed_pattern))
        data.write(cls.new_algo.getvalue())
        data.write(cls.new_secure_algo.getvalue())
        data.write(Bytes.getvalue(cls.secure_random))
        return data.getvalue()


class PasswordSettings(TL):
    ID = 0x9a5c33e5

    def __init__(cls, email: str = None, secure_settings: TL = None):
        cls.email = email
        cls.secure_settings = secure_settings

    @staticmethod
    def read(data) -> "PasswordSettings":
        flags = Int.read(data)
        email = String.read(data) if flags & 1 else None
        secure_settings = data.getobj() if flags & 2 else None
        return PasswordSettings(email=email, secure_settings=secure_settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.email is not None else 0
        flags |= 2 if cls.secure_settings is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.email is not None:
            data.write(String.getvalue(cls.email))
        
        if cls.secure_settings is not None:
            data.write(cls.secure_settings.getvalue())
        return data.getvalue()


class PasswordInputSettings(TL):
    ID = 0xc23727c9

    def __init__(cls, new_algo: TL = None, new_password_hash: bytes = None, hint: str = None, email: str = None, new_secure_settings: TL = None):
        cls.new_algo = new_algo
        cls.new_password_hash = new_password_hash
        cls.hint = hint
        cls.email = email
        cls.new_secure_settings = new_secure_settings

    @staticmethod
    def read(data) -> "PasswordInputSettings":
        flags = Int.read(data)
        new_algo = data.getobj() if flags & 1 else None
        new_password_hash = Bytes.read(data) if flags & 1 else None
        hint = String.read(data) if flags & 1 else None
        email = String.read(data) if flags & 2 else None
        new_secure_settings = data.getobj() if flags & 4 else None
        return PasswordInputSettings(new_algo=new_algo, new_password_hash=new_password_hash, hint=hint, email=email, new_secure_settings=new_secure_settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.new_algo is not None else 0
        flags |= 1 if cls.new_password_hash is not None else 0
        flags |= 1 if cls.hint is not None else 0
        flags |= 2 if cls.email is not None else 0
        flags |= 4 if cls.new_secure_settings is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.new_algo is not None:
            data.write(cls.new_algo.getvalue())
        
        if cls.new_password_hash is not None:
            data.write(Bytes.getvalue(cls.new_password_hash))
        
        if cls.hint is not None:
            data.write(String.getvalue(cls.hint))
        
        if cls.email is not None:
            data.write(String.getvalue(cls.email))
        
        if cls.new_secure_settings is not None:
            data.write(cls.new_secure_settings.getvalue())
        return data.getvalue()


class TmpPassword(TL):
    ID = 0xdb64fd34

    def __init__(cls, tmp_password: bytes, valid_until: int):
        cls.tmp_password = tmp_password
        cls.valid_until = valid_until

    @staticmethod
    def read(data) -> "TmpPassword":
        tmp_password = Bytes.read(data)
        valid_until = Int.read(data)
        return TmpPassword(tmp_password=tmp_password, valid_until=valid_until)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.tmp_password))
        data.write(Int.getvalue(cls.valid_until))
        return data.getvalue()


class WebAuthorizations(TL):
    ID = 0xed56c9fc

    def __init__(cls, authorizations: List[TL], users: List[TL]):
        cls.authorizations = authorizations
        cls.users = users

    @staticmethod
    def read(data) -> "WebAuthorizations":
        authorizations = data.getobj()
        users = data.getobj()
        return WebAuthorizations(authorizations=authorizations, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.authorizations))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class AuthorizationForm(TL):
    ID = 0xad2e1cd8

    def __init__(cls, required_types: List[TL], values: List[TL], errors: List[TL], users: List[TL], privacy_policy_url: str = None):
        cls.required_types = required_types
        cls.values = values
        cls.errors = errors
        cls.users = users
        cls.privacy_policy_url = privacy_policy_url

    @staticmethod
    def read(data) -> "AuthorizationForm":
        flags = Int.read(data)
        required_types = data.getobj()
        values = data.getobj()
        errors = data.getobj()
        users = data.getobj()
        privacy_policy_url = String.read(data) if flags & 1 else None
        return AuthorizationForm(required_types=required_types, values=values, errors=errors, users=users, privacy_policy_url=privacy_policy_url)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.privacy_policy_url is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Vector().getvalue(cls.required_types))
        data.write(Vector().getvalue(cls.values))
        data.write(Vector().getvalue(cls.errors))
        data.write(Vector().getvalue(cls.users))
        
        if cls.privacy_policy_url is not None:
            data.write(String.getvalue(cls.privacy_policy_url))
        return data.getvalue()


class SentEmailCode(TL):
    ID = 0x811f854f

    def __init__(cls, email_pattern: str, length: int):
        cls.email_pattern = email_pattern
        cls.length = length

    @staticmethod
    def read(data) -> "SentEmailCode":
        email_pattern = String.read(data)
        length = Int.read(data)
        return SentEmailCode(email_pattern=email_pattern, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.email_pattern))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class Takeout(TL):
    ID = 0x4dba4501

    def __init__(cls, id: int):
        cls.id = id

    @staticmethod
    def read(data) -> "Takeout":
        id = Long.read(data)
        return Takeout(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        return data.getvalue()


class WallPapersNotModified(TL):
    ID = 0x1c199183

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "WallPapersNotModified":
        
        return WallPapersNotModified()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class WallPapers(TL):
    ID = 0x702b65a9

    def __init__(cls, hash: int, wallpapers: List[TL]):
        cls.hash = hash
        cls.wallpapers = wallpapers

    @staticmethod
    def read(data) -> "WallPapers":
        hash = Int.read(data)
        wallpapers = data.getobj()
        return WallPapers(hash=hash, wallpapers=wallpapers)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        data.write(Vector().getvalue(cls.wallpapers))
        return data.getvalue()


class AutoDownloadSettings(TL):
    ID = 0x63cacf26

    def __init__(cls, low: TL, medium: TL, high: TL):
        cls.low = low
        cls.medium = medium
        cls.high = high

    @staticmethod
    def read(data) -> "AutoDownloadSettings":
        low = data.getobj()
        medium = data.getobj()
        high = data.getobj()
        return AutoDownloadSettings(low=low, medium=medium, high=high)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.low.getvalue())
        data.write(cls.medium.getvalue())
        data.write(cls.high.getvalue())
        return data.getvalue()


class ThemesNotModified(TL):
    ID = 0xf41eb622

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ThemesNotModified":
        
        return ThemesNotModified()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class Themes(TL):
    ID = 0x7f676421

    def __init__(cls, hash: int, themes: List[TL]):
        cls.hash = hash
        cls.themes = themes

    @staticmethod
    def read(data) -> "Themes":
        hash = Int.read(data)
        themes = data.getobj()
        return Themes(hash=hash, themes=themes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        data.write(Vector().getvalue(cls.themes))
        return data.getvalue()


class ContentSettings(TL):
    ID = 0x57e28221

    def __init__(cls, sensitive_enabled: bool = None, sensitive_can_change: bool = None):
        cls.sensitive_enabled = sensitive_enabled
        cls.sensitive_can_change = sensitive_can_change

    @staticmethod
    def read(data) -> "ContentSettings":
        flags = Int.read(data)
        sensitive_enabled = True if flags & 1 else False
        sensitive_can_change = True if flags & 2 else False
        return ContentSettings(sensitive_enabled=sensitive_enabled, sensitive_can_change=sensitive_can_change)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.sensitive_enabled is not None else 0
        flags |= 2 if cls.sensitive_can_change is not None else 0
        data.write(Int.getvalue(flags))
        return data.getvalue()
