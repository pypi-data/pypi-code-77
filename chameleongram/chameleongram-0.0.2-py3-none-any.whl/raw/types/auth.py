from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class SentCode(TL):
    ID = 0x5e002502

    def __init__(cls, type: TL, phone_code_hash: str, next_type: TL = None, timeout: int = None):
        cls.type = type
        cls.phone_code_hash = phone_code_hash
        cls.next_type = next_type
        cls.timeout = timeout

    @staticmethod
    def read(data) -> "SentCode":
        flags = Int.read(data)
        type = data.getobj()
        phone_code_hash = String.read(data)
        next_type = data.getobj() if flags & 2 else None
        timeout = Int.read(data) if flags & 4 else None
        return SentCode(type=type, phone_code_hash=phone_code_hash, next_type=next_type, timeout=timeout)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.next_type is not None else 0
        flags |= 4 if cls.timeout is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.type.getvalue())
        data.write(String.getvalue(cls.phone_code_hash))
        
        if cls.next_type is not None:
            data.write(cls.next_type.getvalue())
        
        if cls.timeout is not None:
            data.write(Int.getvalue(cls.timeout))
        return data.getvalue()


class Authorization(TL):
    ID = 0xcd050916

    def __init__(cls, user: TL, tmp_sessions: int = None):
        cls.tmp_sessions = tmp_sessions
        cls.user = user

    @staticmethod
    def read(data) -> "Authorization":
        flags = Int.read(data)
        tmp_sessions = Int.read(data) if flags & 1 else None
        user = data.getobj()
        return Authorization(tmp_sessions=tmp_sessions, user=user)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.tmp_sessions is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.tmp_sessions is not None:
            data.write(Int.getvalue(cls.tmp_sessions))
        data.write(cls.user.getvalue())
        return data.getvalue()


class AuthorizationSignUpRequired(TL):
    ID = 0x44747e9a

    def __init__(cls, terms_of_service: TL = None):
        cls.terms_of_service = terms_of_service

    @staticmethod
    def read(data) -> "AuthorizationSignUpRequired":
        flags = Int.read(data)
        terms_of_service = data.getobj() if flags & 1 else None
        return AuthorizationSignUpRequired(terms_of_service=terms_of_service)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.terms_of_service is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.terms_of_service is not None:
            data.write(cls.terms_of_service.getvalue())
        return data.getvalue()


class ExportedAuthorization(TL):
    ID = 0xdf969c2d

    def __init__(cls, id: int, bytes: bytes):
        cls.id = id
        cls.bytes = bytes

    @staticmethod
    def read(data) -> "ExportedAuthorization":
        id = Int.read(data)
        bytes = Bytes.read(data)
        return ExportedAuthorization(id=id, bytes=bytes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.id))
        data.write(Bytes.getvalue(cls.bytes))
        return data.getvalue()


class PasswordRecovery(TL):
    ID = 0x137948a5

    def __init__(cls, email_pattern: str):
        cls.email_pattern = email_pattern

    @staticmethod
    def read(data) -> "PasswordRecovery":
        email_pattern = String.read(data)
        return PasswordRecovery(email_pattern=email_pattern)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.email_pattern))
        return data.getvalue()


class CodeTypeSms(TL):
    ID = 0x72a3158c

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "CodeTypeSms":
        
        return CodeTypeSms()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class CodeTypeCall(TL):
    ID = 0x741cd3e3

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "CodeTypeCall":
        
        return CodeTypeCall()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class CodeTypeFlashCall(TL):
    ID = 0x226ccefb

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "CodeTypeFlashCall":
        
        return CodeTypeFlashCall()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SentCodeTypeApp(TL):
    ID = 0x3dbb5986

    def __init__(cls, length: int):
        cls.length = length

    @staticmethod
    def read(data) -> "SentCodeTypeApp":
        length = Int.read(data)
        return SentCodeTypeApp(length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class SentCodeTypeSms(TL):
    ID = 0xc000bba2

    def __init__(cls, length: int):
        cls.length = length

    @staticmethod
    def read(data) -> "SentCodeTypeSms":
        length = Int.read(data)
        return SentCodeTypeSms(length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class SentCodeTypeCall(TL):
    ID = 0x5353e5a7

    def __init__(cls, length: int):
        cls.length = length

    @staticmethod
    def read(data) -> "SentCodeTypeCall":
        length = Int.read(data)
        return SentCodeTypeCall(length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class SentCodeTypeFlashCall(TL):
    ID = 0xab03c6d9

    def __init__(cls, pattern: str):
        cls.pattern = pattern

    @staticmethod
    def read(data) -> "SentCodeTypeFlashCall":
        pattern = String.read(data)
        return SentCodeTypeFlashCall(pattern=pattern)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.pattern))
        return data.getvalue()


class LoginToken(TL):
    ID = 0x629f1980

    def __init__(cls, expires: int, token: bytes):
        cls.expires = expires
        cls.token = token

    @staticmethod
    def read(data) -> "LoginToken":
        expires = Int.read(data)
        token = Bytes.read(data)
        return LoginToken(expires=expires, token=token)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.expires))
        data.write(Bytes.getvalue(cls.token))
        return data.getvalue()


class LoginTokenMigrateTo(TL):
    ID = 0x68e9916

    def __init__(cls, dc_id: int, token: bytes):
        cls.dc_id = dc_id
        cls.token = token

    @staticmethod
    def read(data) -> "LoginTokenMigrateTo":
        dc_id = Int.read(data)
        token = Bytes.read(data)
        return LoginTokenMigrateTo(dc_id=dc_id, token=token)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.dc_id))
        data.write(Bytes.getvalue(cls.token))
        return data.getvalue()


class LoginTokenSuccess(TL):
    ID = 0x390d5c5e

    def __init__(cls, authorization: TL):
        cls.authorization = authorization

    @staticmethod
    def read(data) -> "LoginTokenSuccess":
        authorization = data.getobj()
        return LoginTokenSuccess(authorization=authorization)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.authorization.getvalue())
        return data.getvalue()
