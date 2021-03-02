from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class SendCode(TL):
    ID = 0xa677244f

    def __init__(cls, phone_number: str, api_id: int, api_hash: str, settings: TL):
        cls.phone_number = phone_number
        cls.api_id = api_id
        cls.api_hash = api_hash
        cls.settings = settings

    @staticmethod
    def read(data) -> "SendCode":
        phone_number = String.read(data)
        api_id = Int.read(data)
        api_hash = String.read(data)
        settings = data.getobj()
        return SendCode(phone_number=phone_number, api_id=api_id, api_hash=api_hash, settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone_number))
        data.write(Int.getvalue(cls.api_id))
        data.write(String.getvalue(cls.api_hash))
        data.write(cls.settings.getvalue())
        return data.getvalue()


class SignUp(TL):
    ID = 0x80eee427

    def __init__(cls, phone_number: str, phone_code_hash: str, first_name: str, last_name: str):
        cls.phone_number = phone_number
        cls.phone_code_hash = phone_code_hash
        cls.first_name = first_name
        cls.last_name = last_name

    @staticmethod
    def read(data) -> "SignUp":
        phone_number = String.read(data)
        phone_code_hash = String.read(data)
        first_name = String.read(data)
        last_name = String.read(data)
        return SignUp(phone_number=phone_number, phone_code_hash=phone_code_hash, first_name=first_name, last_name=last_name)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone_number))
        data.write(String.getvalue(cls.phone_code_hash))
        data.write(String.getvalue(cls.first_name))
        data.write(String.getvalue(cls.last_name))
        return data.getvalue()


class SignIn(TL):
    ID = 0xbcd51581

    def __init__(cls, phone_number: str, phone_code_hash: str, phone_code: str):
        cls.phone_number = phone_number
        cls.phone_code_hash = phone_code_hash
        cls.phone_code = phone_code

    @staticmethod
    def read(data) -> "SignIn":
        phone_number = String.read(data)
        phone_code_hash = String.read(data)
        phone_code = String.read(data)
        return SignIn(phone_number=phone_number, phone_code_hash=phone_code_hash, phone_code=phone_code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone_number))
        data.write(String.getvalue(cls.phone_code_hash))
        data.write(String.getvalue(cls.phone_code))
        return data.getvalue()


class LogOut(TL):
    ID = 0x5717da40

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "LogOut":
        
        return LogOut()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ResetAuthorizations(TL):
    ID = 0x9fab0d1a

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ResetAuthorizations":
        
        return ResetAuthorizations()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ExportAuthorization(TL):
    ID = 0xe5bfffcd

    def __init__(cls, dc_id: int):
        cls.dc_id = dc_id

    @staticmethod
    def read(data) -> "ExportAuthorization":
        dc_id = Int.read(data)
        return ExportAuthorization(dc_id=dc_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.dc_id))
        return data.getvalue()


class ImportAuthorization(TL):
    ID = 0xe3ef9613

    def __init__(cls, id: int, bytes: bytes):
        cls.id = id
        cls.bytes = bytes

    @staticmethod
    def read(data) -> "ImportAuthorization":
        id = Int.read(data)
        bytes = Bytes.read(data)
        return ImportAuthorization(id=id, bytes=bytes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.id))
        data.write(Bytes.getvalue(cls.bytes))
        return data.getvalue()


class BindTempAuthKey(TL):
    ID = 0xcdd42a05

    def __init__(cls, perm_auth_key_id: int, nonce: int, expires_at: int, encrypted_message: bytes):
        cls.perm_auth_key_id = perm_auth_key_id
        cls.nonce = nonce
        cls.expires_at = expires_at
        cls.encrypted_message = encrypted_message

    @staticmethod
    def read(data) -> "BindTempAuthKey":
        perm_auth_key_id = Long.read(data)
        nonce = Long.read(data)
        expires_at = Int.read(data)
        encrypted_message = Bytes.read(data)
        return BindTempAuthKey(perm_auth_key_id=perm_auth_key_id, nonce=nonce, expires_at=expires_at, encrypted_message=encrypted_message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.perm_auth_key_id))
        data.write(Long.getvalue(cls.nonce))
        data.write(Int.getvalue(cls.expires_at))
        data.write(Bytes.getvalue(cls.encrypted_message))
        return data.getvalue()


class ImportBotAuthorization(TL):
    ID = 0x67a3ff2c

    def __init__(cls, api_id: int, api_hash: str, bot_auth_token: str):
        cls.api_id = api_id
        cls.api_hash = api_hash
        cls.bot_auth_token = bot_auth_token

    @staticmethod
    def read(data) -> "ImportBotAuthorization":
        flags = Int.read(data)
        api_id = Int.read(data)
        api_hash = String.read(data)
        bot_auth_token = String.read(data)
        return ImportBotAuthorization(api_id=api_id, api_hash=api_hash, bot_auth_token=bot_auth_token)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.api_id))
        data.write(String.getvalue(cls.api_hash))
        data.write(String.getvalue(cls.bot_auth_token))
        return data.getvalue()


class CheckPassword(TL):
    ID = 0xd18b4d16

    def __init__(cls, password: TL):
        cls.password = password

    @staticmethod
    def read(data) -> "CheckPassword":
        password = data.getobj()
        return CheckPassword(password=password)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.password.getvalue())
        return data.getvalue()


class RequestPasswordRecovery(TL):
    ID = 0xd897bc66

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "RequestPasswordRecovery":
        
        return RequestPasswordRecovery()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class RecoverPassword(TL):
    ID = 0x4ea56e92

    def __init__(cls, code: str):
        cls.code = code

    @staticmethod
    def read(data) -> "RecoverPassword":
        code = String.read(data)
        return RecoverPassword(code=code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.code))
        return data.getvalue()


class ResendCode(TL):
    ID = 0x3ef1a9bf

    def __init__(cls, phone_number: str, phone_code_hash: str):
        cls.phone_number = phone_number
        cls.phone_code_hash = phone_code_hash

    @staticmethod
    def read(data) -> "ResendCode":
        phone_number = String.read(data)
        phone_code_hash = String.read(data)
        return ResendCode(phone_number=phone_number, phone_code_hash=phone_code_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone_number))
        data.write(String.getvalue(cls.phone_code_hash))
        return data.getvalue()


class CancelCode(TL):
    ID = 0x1f040578

    def __init__(cls, phone_number: str, phone_code_hash: str):
        cls.phone_number = phone_number
        cls.phone_code_hash = phone_code_hash

    @staticmethod
    def read(data) -> "CancelCode":
        phone_number = String.read(data)
        phone_code_hash = String.read(data)
        return CancelCode(phone_number=phone_number, phone_code_hash=phone_code_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone_number))
        data.write(String.getvalue(cls.phone_code_hash))
        return data.getvalue()


class DropTempAuthKeys(TL):
    ID = 0x8e48a188

    def __init__(cls, except_auth_keys: List[int]):
        cls.except_auth_keys = except_auth_keys

    @staticmethod
    def read(data) -> "DropTempAuthKeys":
        except_auth_keys = data.getobj(Long)
        return DropTempAuthKeys(except_auth_keys=except_auth_keys)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.except_auth_keys, Long))
        return data.getvalue()


class ExportLoginToken(TL):
    ID = 0xb1b41517

    def __init__(cls, api_id: int, api_hash: str, except_ids: List[int]):
        cls.api_id = api_id
        cls.api_hash = api_hash
        cls.except_ids = except_ids

    @staticmethod
    def read(data) -> "ExportLoginToken":
        api_id = Int.read(data)
        api_hash = String.read(data)
        except_ids = data.getobj(Int)
        return ExportLoginToken(api_id=api_id, api_hash=api_hash, except_ids=except_ids)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.api_id))
        data.write(String.getvalue(cls.api_hash))
        data.write(Vector().getvalue(cls.except_ids, Int))
        return data.getvalue()


class ImportLoginToken(TL):
    ID = 0x95ac5ce4

    def __init__(cls, token: bytes):
        cls.token = token

    @staticmethod
    def read(data) -> "ImportLoginToken":
        token = Bytes.read(data)
        return ImportLoginToken(token=token)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.token))
        return data.getvalue()


class AcceptLoginToken(TL):
    ID = 0xe894ad4d

    def __init__(cls, token: bytes):
        cls.token = token

    @staticmethod
    def read(data) -> "AcceptLoginToken":
        token = Bytes.read(data)
        return AcceptLoginToken(token=token)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.token))
        return data.getvalue()
