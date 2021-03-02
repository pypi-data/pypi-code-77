from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class RegisterDevice(TL):
    ID = 0x68976c6f

    def __init__(cls, token_type: int, token: str, app_sandbox: bool, secret: bytes, other_uids: List[int], no_muted: bool = None):
        cls.no_muted = no_muted
        cls.token_type = token_type
        cls.token = token
        cls.app_sandbox = app_sandbox
        cls.secret = secret
        cls.other_uids = other_uids

    @staticmethod
    def read(data) -> "RegisterDevice":
        flags = Int.read(data)
        no_muted = True if flags & 1 else False
        token_type = Int.read(data)
        token = String.read(data)
        app_sandbox = Bool.read(data)
        secret = Bytes.read(data)
        other_uids = data.getobj(Int)
        return RegisterDevice(no_muted=no_muted, token_type=token_type, token=token, app_sandbox=app_sandbox, secret=secret, other_uids=other_uids)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.no_muted is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.token_type))
        data.write(String.getvalue(cls.token))
        data.write(Bool.getvalue(cls.app_sandbox))
        data.write(Bytes.getvalue(cls.secret))
        data.write(Vector().getvalue(cls.other_uids, Int))
        return data.getvalue()


class UnregisterDevice(TL):
    ID = 0x3076c4bf

    def __init__(cls, token_type: int, token: str, other_uids: List[int]):
        cls.token_type = token_type
        cls.token = token
        cls.other_uids = other_uids

    @staticmethod
    def read(data) -> "UnregisterDevice":
        token_type = Int.read(data)
        token = String.read(data)
        other_uids = data.getobj(Int)
        return UnregisterDevice(token_type=token_type, token=token, other_uids=other_uids)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.token_type))
        data.write(String.getvalue(cls.token))
        data.write(Vector().getvalue(cls.other_uids, Int))
        return data.getvalue()


class UpdateNotifySettings(TL):
    ID = 0x84be5b93

    def __init__(cls, peer: TL, settings: TL):
        cls.peer = peer
        cls.settings = settings

    @staticmethod
    def read(data) -> "UpdateNotifySettings":
        peer = data.getobj()
        settings = data.getobj()
        return UpdateNotifySettings(peer=peer, settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(cls.settings.getvalue())
        return data.getvalue()


class GetNotifySettings(TL):
    ID = 0x12b3ad31

    def __init__(cls, peer: TL):
        cls.peer = peer

    @staticmethod
    def read(data) -> "GetNotifySettings":
        peer = data.getobj()
        return GetNotifySettings(peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class ResetNotifySettings(TL):
    ID = 0xdb7e1747

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ResetNotifySettings":
        
        return ResetNotifySettings()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UpdateProfile(TL):
    ID = 0x78515775

    def __init__(cls, first_name: str = None, last_name: str = None, about: str = None):
        cls.first_name = first_name
        cls.last_name = last_name
        cls.about = about

    @staticmethod
    def read(data) -> "UpdateProfile":
        flags = Int.read(data)
        first_name = String.read(data) if flags & 1 else None
        last_name = String.read(data) if flags & 2 else None
        about = String.read(data) if flags & 4 else None
        return UpdateProfile(first_name=first_name, last_name=last_name, about=about)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.first_name is not None else 0
        flags |= 2 if cls.last_name is not None else 0
        flags |= 4 if cls.about is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.first_name is not None:
            data.write(String.getvalue(cls.first_name))
        
        if cls.last_name is not None:
            data.write(String.getvalue(cls.last_name))
        
        if cls.about is not None:
            data.write(String.getvalue(cls.about))
        return data.getvalue()


class UpdateStatus(TL):
    ID = 0x6628562c

    def __init__(cls, offline: bool):
        cls.offline = offline

    @staticmethod
    def read(data) -> "UpdateStatus":
        offline = Bool.read(data)
        return UpdateStatus(offline=offline)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bool.getvalue(cls.offline))
        return data.getvalue()


class GetWallPapers(TL):
    ID = 0xaabb1763

    def __init__(cls, hash: int):
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetWallPapers":
        hash = Int.read(data)
        return GetWallPapers(hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class ReportPeer(TL):
    ID = 0xc5ba3d86

    def __init__(cls, peer: TL, reason: TL, message: str):
        cls.peer = peer
        cls.reason = reason
        cls.message = message

    @staticmethod
    def read(data) -> "ReportPeer":
        peer = data.getobj()
        reason = data.getobj()
        message = String.read(data)
        return ReportPeer(peer=peer, reason=reason, message=message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(cls.reason.getvalue())
        data.write(String.getvalue(cls.message))
        return data.getvalue()


class CheckUsername(TL):
    ID = 0x2714d86c

    def __init__(cls, username: str):
        cls.username = username

    @staticmethod
    def read(data) -> "CheckUsername":
        username = String.read(data)
        return CheckUsername(username=username)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.username))
        return data.getvalue()


class UpdateUsername(TL):
    ID = 0x3e0bdd7c

    def __init__(cls, username: str):
        cls.username = username

    @staticmethod
    def read(data) -> "UpdateUsername":
        username = String.read(data)
        return UpdateUsername(username=username)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.username))
        return data.getvalue()


class GetPrivacy(TL):
    ID = 0xdadbc950

    def __init__(cls, key: TL):
        cls.key = key

    @staticmethod
    def read(data) -> "GetPrivacy":
        key = data.getobj()
        return GetPrivacy(key=key)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.key.getvalue())
        return data.getvalue()


class SetPrivacy(TL):
    ID = 0xc9f81ce8

    def __init__(cls, key: TL, rules: List[TL]):
        cls.key = key
        cls.rules = rules

    @staticmethod
    def read(data) -> "SetPrivacy":
        key = data.getobj()
        rules = data.getobj()
        return SetPrivacy(key=key, rules=rules)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.key.getvalue())
        data.write(Vector().getvalue(cls.rules))
        return data.getvalue()


class DeleteAccount(TL):
    ID = 0x418d4e0b

    def __init__(cls, reason: str):
        cls.reason = reason

    @staticmethod
    def read(data) -> "DeleteAccount":
        reason = String.read(data)
        return DeleteAccount(reason=reason)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.reason))
        return data.getvalue()


class GetAccountTTL(TL):
    ID = 0x8fc711d

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetAccountTTL":
        
        return GetAccountTTL()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SetAccountTTL(TL):
    ID = 0x2442485e

    def __init__(cls, ttl: TL):
        cls.ttl = ttl

    @staticmethod
    def read(data) -> "SetAccountTTL":
        ttl = data.getobj()
        return SetAccountTTL(ttl=ttl)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.ttl.getvalue())
        return data.getvalue()


class SendChangePhoneCode(TL):
    ID = 0x82574ae5

    def __init__(cls, phone_number: str, settings: TL):
        cls.phone_number = phone_number
        cls.settings = settings

    @staticmethod
    def read(data) -> "SendChangePhoneCode":
        phone_number = String.read(data)
        settings = data.getobj()
        return SendChangePhoneCode(phone_number=phone_number, settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone_number))
        data.write(cls.settings.getvalue())
        return data.getvalue()


class ChangePhone(TL):
    ID = 0x70c32edb

    def __init__(cls, phone_number: str, phone_code_hash: str, phone_code: str):
        cls.phone_number = phone_number
        cls.phone_code_hash = phone_code_hash
        cls.phone_code = phone_code

    @staticmethod
    def read(data) -> "ChangePhone":
        phone_number = String.read(data)
        phone_code_hash = String.read(data)
        phone_code = String.read(data)
        return ChangePhone(phone_number=phone_number, phone_code_hash=phone_code_hash, phone_code=phone_code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone_number))
        data.write(String.getvalue(cls.phone_code_hash))
        data.write(String.getvalue(cls.phone_code))
        return data.getvalue()


class UpdateDeviceLocked(TL):
    ID = 0x38df3532

    def __init__(cls, period: int):
        cls.period = period

    @staticmethod
    def read(data) -> "UpdateDeviceLocked":
        period = Int.read(data)
        return UpdateDeviceLocked(period=period)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.period))
        return data.getvalue()


class GetAuthorizations(TL):
    ID = 0xe320c158

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetAuthorizations":
        
        return GetAuthorizations()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ResetAuthorization(TL):
    ID = 0xdf77f3bc

    def __init__(cls, hash: int):
        cls.hash = hash

    @staticmethod
    def read(data) -> "ResetAuthorization":
        hash = Long.read(data)
        return ResetAuthorization(hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.hash))
        return data.getvalue()


class GetPassword(TL):
    ID = 0x548a30f5

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetPassword":
        
        return GetPassword()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetPasswordSettings(TL):
    ID = 0x9cd4eaf9

    def __init__(cls, password: TL):
        cls.password = password

    @staticmethod
    def read(data) -> "GetPasswordSettings":
        password = data.getobj()
        return GetPasswordSettings(password=password)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.password.getvalue())
        return data.getvalue()


class UpdatePasswordSettings(TL):
    ID = 0xa59b102f

    def __init__(cls, password: TL, new_settings: TL):
        cls.password = password
        cls.new_settings = new_settings

    @staticmethod
    def read(data) -> "UpdatePasswordSettings":
        password = data.getobj()
        new_settings = data.getobj()
        return UpdatePasswordSettings(password=password, new_settings=new_settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.password.getvalue())
        data.write(cls.new_settings.getvalue())
        return data.getvalue()


class SendConfirmPhoneCode(TL):
    ID = 0x1b3faa88

    def __init__(cls, hash: str, settings: TL):
        cls.hash = hash
        cls.settings = settings

    @staticmethod
    def read(data) -> "SendConfirmPhoneCode":
        hash = String.read(data)
        settings = data.getobj()
        return SendConfirmPhoneCode(hash=hash, settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.hash))
        data.write(cls.settings.getvalue())
        return data.getvalue()


class ConfirmPhone(TL):
    ID = 0x5f2178c3

    def __init__(cls, phone_code_hash: str, phone_code: str):
        cls.phone_code_hash = phone_code_hash
        cls.phone_code = phone_code

    @staticmethod
    def read(data) -> "ConfirmPhone":
        phone_code_hash = String.read(data)
        phone_code = String.read(data)
        return ConfirmPhone(phone_code_hash=phone_code_hash, phone_code=phone_code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone_code_hash))
        data.write(String.getvalue(cls.phone_code))
        return data.getvalue()


class GetTmpPassword(TL):
    ID = 0x449e0b51

    def __init__(cls, password: TL, period: int):
        cls.password = password
        cls.period = period

    @staticmethod
    def read(data) -> "GetTmpPassword":
        password = data.getobj()
        period = Int.read(data)
        return GetTmpPassword(password=password, period=period)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.password.getvalue())
        data.write(Int.getvalue(cls.period))
        return data.getvalue()


class GetWebAuthorizations(TL):
    ID = 0x182e6d6f

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetWebAuthorizations":
        
        return GetWebAuthorizations()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ResetWebAuthorization(TL):
    ID = 0x2d01b9ef

    def __init__(cls, hash: int):
        cls.hash = hash

    @staticmethod
    def read(data) -> "ResetWebAuthorization":
        hash = Long.read(data)
        return ResetWebAuthorization(hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.hash))
        return data.getvalue()


class ResetWebAuthorizations(TL):
    ID = 0x682d2594

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ResetWebAuthorizations":
        
        return ResetWebAuthorizations()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetAllSecureValues(TL):
    ID = 0xb288bc7d

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetAllSecureValues":
        
        return GetAllSecureValues()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetSecureValue(TL):
    ID = 0x73665bc2

    def __init__(cls, types: List[TL]):
        cls.types = types

    @staticmethod
    def read(data) -> "GetSecureValue":
        types = data.getobj()
        return GetSecureValue(types=types)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.types))
        return data.getvalue()


class SaveSecureValue(TL):
    ID = 0x899fe31d

    def __init__(cls, value: TL, secure_secret_id: int):
        cls.value = value
        cls.secure_secret_id = secure_secret_id

    @staticmethod
    def read(data) -> "SaveSecureValue":
        value = data.getobj()
        secure_secret_id = Long.read(data)
        return SaveSecureValue(value=value, secure_secret_id=secure_secret_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.value.getvalue())
        data.write(Long.getvalue(cls.secure_secret_id))
        return data.getvalue()


class DeleteSecureValue(TL):
    ID = 0xb880bc4b

    def __init__(cls, types: List[TL]):
        cls.types = types

    @staticmethod
    def read(data) -> "DeleteSecureValue":
        types = data.getobj()
        return DeleteSecureValue(types=types)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.types))
        return data.getvalue()


class GetAuthorizationForm(TL):
    ID = 0xb86ba8e1

    def __init__(cls, bot_id: int, scope: str, public_key: str):
        cls.bot_id = bot_id
        cls.scope = scope
        cls.public_key = public_key

    @staticmethod
    def read(data) -> "GetAuthorizationForm":
        bot_id = Int.read(data)
        scope = String.read(data)
        public_key = String.read(data)
        return GetAuthorizationForm(bot_id=bot_id, scope=scope, public_key=public_key)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.bot_id))
        data.write(String.getvalue(cls.scope))
        data.write(String.getvalue(cls.public_key))
        return data.getvalue()


class AcceptAuthorization(TL):
    ID = 0xe7027c94

    def __init__(cls, bot_id: int, scope: str, public_key: str, value_hashes: List[TL], credentials: TL):
        cls.bot_id = bot_id
        cls.scope = scope
        cls.public_key = public_key
        cls.value_hashes = value_hashes
        cls.credentials = credentials

    @staticmethod
    def read(data) -> "AcceptAuthorization":
        bot_id = Int.read(data)
        scope = String.read(data)
        public_key = String.read(data)
        value_hashes = data.getobj()
        credentials = data.getobj()
        return AcceptAuthorization(bot_id=bot_id, scope=scope, public_key=public_key, value_hashes=value_hashes, credentials=credentials)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.bot_id))
        data.write(String.getvalue(cls.scope))
        data.write(String.getvalue(cls.public_key))
        data.write(Vector().getvalue(cls.value_hashes))
        data.write(cls.credentials.getvalue())
        return data.getvalue()


class SendVerifyPhoneCode(TL):
    ID = 0xa5a356f9

    def __init__(cls, phone_number: str, settings: TL):
        cls.phone_number = phone_number
        cls.settings = settings

    @staticmethod
    def read(data) -> "SendVerifyPhoneCode":
        phone_number = String.read(data)
        settings = data.getobj()
        return SendVerifyPhoneCode(phone_number=phone_number, settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone_number))
        data.write(cls.settings.getvalue())
        return data.getvalue()


class VerifyPhone(TL):
    ID = 0x4dd3a7f6

    def __init__(cls, phone_number: str, phone_code_hash: str, phone_code: str):
        cls.phone_number = phone_number
        cls.phone_code_hash = phone_code_hash
        cls.phone_code = phone_code

    @staticmethod
    def read(data) -> "VerifyPhone":
        phone_number = String.read(data)
        phone_code_hash = String.read(data)
        phone_code = String.read(data)
        return VerifyPhone(phone_number=phone_number, phone_code_hash=phone_code_hash, phone_code=phone_code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone_number))
        data.write(String.getvalue(cls.phone_code_hash))
        data.write(String.getvalue(cls.phone_code))
        return data.getvalue()


class SendVerifyEmailCode(TL):
    ID = 0x7011509f

    def __init__(cls, email: str):
        cls.email = email

    @staticmethod
    def read(data) -> "SendVerifyEmailCode":
        email = String.read(data)
        return SendVerifyEmailCode(email=email)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.email))
        return data.getvalue()


class VerifyEmail(TL):
    ID = 0xecba39db

    def __init__(cls, email: str, code: str):
        cls.email = email
        cls.code = code

    @staticmethod
    def read(data) -> "VerifyEmail":
        email = String.read(data)
        code = String.read(data)
        return VerifyEmail(email=email, code=code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.email))
        data.write(String.getvalue(cls.code))
        return data.getvalue()


class InitTakeoutSession(TL):
    ID = 0xf05b4804

    def __init__(cls, contacts: bool = None, message_users: bool = None, message_chats: bool = None, message_megagroups: bool = None, message_channels: bool = None, files: bool = None, file_max_size: int = None):
        cls.contacts = contacts
        cls.message_users = message_users
        cls.message_chats = message_chats
        cls.message_megagroups = message_megagroups
        cls.message_channels = message_channels
        cls.files = files
        cls.file_max_size = file_max_size

    @staticmethod
    def read(data) -> "InitTakeoutSession":
        flags = Int.read(data)
        contacts = True if flags & 1 else False
        message_users = True if flags & 2 else False
        message_chats = True if flags & 4 else False
        message_megagroups = True if flags & 8 else False
        message_channels = True if flags & 16 else False
        files = True if flags & 32 else False
        file_max_size = Int.read(data) if flags & 32 else None
        return InitTakeoutSession(contacts=contacts, message_users=message_users, message_chats=message_chats, message_megagroups=message_megagroups, message_channels=message_channels, files=files, file_max_size=file_max_size)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.contacts is not None else 0
        flags |= 2 if cls.message_users is not None else 0
        flags |= 4 if cls.message_chats is not None else 0
        flags |= 8 if cls.message_megagroups is not None else 0
        flags |= 16 if cls.message_channels is not None else 0
        flags |= 32 if cls.files is not None else 0
        flags |= 32 if cls.file_max_size is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.file_max_size is not None:
            data.write(Int.getvalue(cls.file_max_size))
        return data.getvalue()


class FinishTakeoutSession(TL):
    ID = 0x1d2652ee

    def __init__(cls, success: bool = None):
        cls.success = success

    @staticmethod
    def read(data) -> "FinishTakeoutSession":
        flags = Int.read(data)
        success = True if flags & 1 else False
        return FinishTakeoutSession(success=success)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.success is not None else 0
        data.write(Int.getvalue(flags))
        return data.getvalue()


class ConfirmPasswordEmail(TL):
    ID = 0x8fdf1920

    def __init__(cls, code: str):
        cls.code = code

    @staticmethod
    def read(data) -> "ConfirmPasswordEmail":
        code = String.read(data)
        return ConfirmPasswordEmail(code=code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.code))
        return data.getvalue()


class ResendPasswordEmail(TL):
    ID = 0x7a7f2a15

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ResendPasswordEmail":
        
        return ResendPasswordEmail()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class CancelPasswordEmail(TL):
    ID = 0xc1cbd5b6

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "CancelPasswordEmail":
        
        return CancelPasswordEmail()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetContactSignUpNotification(TL):
    ID = 0x9f07c728

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetContactSignUpNotification":
        
        return GetContactSignUpNotification()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SetContactSignUpNotification(TL):
    ID = 0xcff43f61

    def __init__(cls, silent: bool):
        cls.silent = silent

    @staticmethod
    def read(data) -> "SetContactSignUpNotification":
        silent = Bool.read(data)
        return SetContactSignUpNotification(silent=silent)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bool.getvalue(cls.silent))
        return data.getvalue()


class GetNotifyExceptions(TL):
    ID = 0x53577479

    def __init__(cls, compare_sound: bool = None, peer: TL = None):
        cls.compare_sound = compare_sound
        cls.peer = peer

    @staticmethod
    def read(data) -> "GetNotifyExceptions":
        flags = Int.read(data)
        compare_sound = True if flags & 2 else False
        peer = data.getobj() if flags & 1 else None
        return GetNotifyExceptions(compare_sound=compare_sound, peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.compare_sound is not None else 0
        flags |= 1 if cls.peer is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.peer is not None:
            data.write(cls.peer.getvalue())
        return data.getvalue()


class GetWallPaper(TL):
    ID = 0xfc8ddbea

    def __init__(cls, wallpaper: TL):
        cls.wallpaper = wallpaper

    @staticmethod
    def read(data) -> "GetWallPaper":
        wallpaper = data.getobj()
        return GetWallPaper(wallpaper=wallpaper)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.wallpaper.getvalue())
        return data.getvalue()


class UploadWallPaper(TL):
    ID = 0xdd853661

    def __init__(cls, file: TL, mime_type: str, settings: TL):
        cls.file = file
        cls.mime_type = mime_type
        cls.settings = settings

    @staticmethod
    def read(data) -> "UploadWallPaper":
        file = data.getobj()
        mime_type = String.read(data)
        settings = data.getobj()
        return UploadWallPaper(file=file, mime_type=mime_type, settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.file.getvalue())
        data.write(String.getvalue(cls.mime_type))
        data.write(cls.settings.getvalue())
        return data.getvalue()


class SaveWallPaper(TL):
    ID = 0x6c5a5b37

    def __init__(cls, wallpaper: TL, unsave: bool, settings: TL):
        cls.wallpaper = wallpaper
        cls.unsave = unsave
        cls.settings = settings

    @staticmethod
    def read(data) -> "SaveWallPaper":
        wallpaper = data.getobj()
        unsave = Bool.read(data)
        settings = data.getobj()
        return SaveWallPaper(wallpaper=wallpaper, unsave=unsave, settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.wallpaper.getvalue())
        data.write(Bool.getvalue(cls.unsave))
        data.write(cls.settings.getvalue())
        return data.getvalue()


class InstallWallPaper(TL):
    ID = 0xfeed5769

    def __init__(cls, wallpaper: TL, settings: TL):
        cls.wallpaper = wallpaper
        cls.settings = settings

    @staticmethod
    def read(data) -> "InstallWallPaper":
        wallpaper = data.getobj()
        settings = data.getobj()
        return InstallWallPaper(wallpaper=wallpaper, settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.wallpaper.getvalue())
        data.write(cls.settings.getvalue())
        return data.getvalue()


class ResetWallPapers(TL):
    ID = 0xbb3b9804

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ResetWallPapers":
        
        return ResetWallPapers()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetAutoDownloadSettings(TL):
    ID = 0x56da0b3f

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetAutoDownloadSettings":
        
        return GetAutoDownloadSettings()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SaveAutoDownloadSettings(TL):
    ID = 0x76f36233

    def __init__(cls, settings: TL, low: bool = None, high: bool = None):
        cls.low = low
        cls.high = high
        cls.settings = settings

    @staticmethod
    def read(data) -> "SaveAutoDownloadSettings":
        flags = Int.read(data)
        low = True if flags & 1 else False
        high = True if flags & 2 else False
        settings = data.getobj()
        return SaveAutoDownloadSettings(low=low, high=high, settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.low is not None else 0
        flags |= 2 if cls.high is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.settings.getvalue())
        return data.getvalue()


class UploadTheme(TL):
    ID = 0x1c3db333

    def __init__(cls, file: TL, file_name: str, mime_type: str, thumb: TL = None):
        cls.file = file
        cls.thumb = thumb
        cls.file_name = file_name
        cls.mime_type = mime_type

    @staticmethod
    def read(data) -> "UploadTheme":
        flags = Int.read(data)
        file = data.getobj()
        thumb = data.getobj() if flags & 1 else None
        file_name = String.read(data)
        mime_type = String.read(data)
        return UploadTheme(file=file, thumb=thumb, file_name=file_name, mime_type=mime_type)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.thumb is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.file.getvalue())
        
        if cls.thumb is not None:
            data.write(cls.thumb.getvalue())
        data.write(String.getvalue(cls.file_name))
        data.write(String.getvalue(cls.mime_type))
        return data.getvalue()


class CreateTheme(TL):
    ID = 0x8432c21f

    def __init__(cls, slug: str, title: str, document: TL = None, settings: TL = None):
        cls.slug = slug
        cls.title = title
        cls.document = document
        cls.settings = settings

    @staticmethod
    def read(data) -> "CreateTheme":
        flags = Int.read(data)
        slug = String.read(data)
        title = String.read(data)
        document = data.getobj() if flags & 4 else None
        settings = data.getobj() if flags & 8 else None
        return CreateTheme(slug=slug, title=title, document=document, settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 4 if cls.document is not None else 0
        flags |= 8 if cls.settings is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.slug))
        data.write(String.getvalue(cls.title))
        
        if cls.document is not None:
            data.write(cls.document.getvalue())
        
        if cls.settings is not None:
            data.write(cls.settings.getvalue())
        return data.getvalue()


class UpdateTheme(TL):
    ID = 0x5cb367d5

    def __init__(cls, format: str, theme: TL, slug: str = None, title: str = None, document: TL = None, settings: TL = None):
        cls.format = format
        cls.theme = theme
        cls.slug = slug
        cls.title = title
        cls.document = document
        cls.settings = settings

    @staticmethod
    def read(data) -> "UpdateTheme":
        flags = Int.read(data)
        format = String.read(data)
        theme = data.getobj()
        slug = String.read(data) if flags & 1 else None
        title = String.read(data) if flags & 2 else None
        document = data.getobj() if flags & 4 else None
        settings = data.getobj() if flags & 8 else None
        return UpdateTheme(format=format, theme=theme, slug=slug, title=title, document=document, settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.slug is not None else 0
        flags |= 2 if cls.title is not None else 0
        flags |= 4 if cls.document is not None else 0
        flags |= 8 if cls.settings is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.format))
        data.write(cls.theme.getvalue())
        
        if cls.slug is not None:
            data.write(String.getvalue(cls.slug))
        
        if cls.title is not None:
            data.write(String.getvalue(cls.title))
        
        if cls.document is not None:
            data.write(cls.document.getvalue())
        
        if cls.settings is not None:
            data.write(cls.settings.getvalue())
        return data.getvalue()


class SaveTheme(TL):
    ID = 0xf257106c

    def __init__(cls, theme: TL, unsave: bool):
        cls.theme = theme
        cls.unsave = unsave

    @staticmethod
    def read(data) -> "SaveTheme":
        theme = data.getobj()
        unsave = Bool.read(data)
        return SaveTheme(theme=theme, unsave=unsave)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.theme.getvalue())
        data.write(Bool.getvalue(cls.unsave))
        return data.getvalue()


class InstallTheme(TL):
    ID = 0x7ae43737

    def __init__(cls, dark: bool = None, format: str = None, theme: TL = None):
        cls.dark = dark
        cls.format = format
        cls.theme = theme

    @staticmethod
    def read(data) -> "InstallTheme":
        flags = Int.read(data)
        dark = True if flags & 1 else False
        format = String.read(data) if flags & 2 else None
        theme = data.getobj() if flags & 2 else None
        return InstallTheme(dark=dark, format=format, theme=theme)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.dark is not None else 0
        flags |= 2 if cls.format is not None else 0
        flags |= 2 if cls.theme is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.format is not None:
            data.write(String.getvalue(cls.format))
        
        if cls.theme is not None:
            data.write(cls.theme.getvalue())
        return data.getvalue()


class GetTheme(TL):
    ID = 0x8d9d742b

    def __init__(cls, format: str, theme: TL, document_id: int):
        cls.format = format
        cls.theme = theme
        cls.document_id = document_id

    @staticmethod
    def read(data) -> "GetTheme":
        format = String.read(data)
        theme = data.getobj()
        document_id = Long.read(data)
        return GetTheme(format=format, theme=theme, document_id=document_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.format))
        data.write(cls.theme.getvalue())
        data.write(Long.getvalue(cls.document_id))
        return data.getvalue()


class GetThemes(TL):
    ID = 0x285946f8

    def __init__(cls, format: str, hash: int):
        cls.format = format
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetThemes":
        format = String.read(data)
        hash = Int.read(data)
        return GetThemes(format=format, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.format))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class SetContentSettings(TL):
    ID = 0xb574b16b

    def __init__(cls, sensitive_enabled: bool = None):
        cls.sensitive_enabled = sensitive_enabled

    @staticmethod
    def read(data) -> "SetContentSettings":
        flags = Int.read(data)
        sensitive_enabled = True if flags & 1 else False
        return SetContentSettings(sensitive_enabled=sensitive_enabled)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.sensitive_enabled is not None else 0
        data.write(Int.getvalue(flags))
        return data.getvalue()


class GetContentSettings(TL):
    ID = 0x8b9b4dae

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetContentSettings":
        
        return GetContentSettings()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetMultiWallPapers(TL):
    ID = 0x65ad71dc

    def __init__(cls, wallpapers: List[TL]):
        cls.wallpapers = wallpapers

    @staticmethod
    def read(data) -> "GetMultiWallPapers":
        wallpapers = data.getobj()
        return GetMultiWallPapers(wallpapers=wallpapers)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.wallpapers))
        return data.getvalue()


class GetGlobalPrivacySettings(TL):
    ID = 0xeb2b4cf6

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetGlobalPrivacySettings":
        
        return GetGlobalPrivacySettings()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SetGlobalPrivacySettings(TL):
    ID = 0x1edaaac2

    def __init__(cls, settings: TL):
        cls.settings = settings

    @staticmethod
    def read(data) -> "SetGlobalPrivacySettings":
        settings = data.getobj()
        return SetGlobalPrivacySettings(settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.settings.getvalue())
        return data.getvalue()


class ReportProfilePhoto(TL):
    ID = 0xfa8cc6f5

    def __init__(cls, peer: TL, photo_id: TL, reason: TL, message: str):
        cls.peer = peer
        cls.photo_id = photo_id
        cls.reason = reason
        cls.message = message

    @staticmethod
    def read(data) -> "ReportProfilePhoto":
        peer = data.getobj()
        photo_id = data.getobj()
        reason = data.getobj()
        message = String.read(data)
        return ReportProfilePhoto(peer=peer, photo_id=photo_id, reason=reason, message=message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(cls.photo_id.getvalue())
        data.write(cls.reason.getvalue())
        data.write(String.getvalue(cls.message))
        return data.getvalue()
