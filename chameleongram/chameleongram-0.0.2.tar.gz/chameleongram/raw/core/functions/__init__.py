from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class ReqPq(TL):
    ID = 0x60469778

    def __init__(cls, nonce: int):
        cls.nonce = nonce

    @staticmethod
    def read(data) -> "ReqPq":
        nonce = Int128.read(data)
        return ReqPq(nonce=nonce)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int128.getvalue(cls.nonce))
        return data.getvalue()


class ReqPqMulti(TL):
    ID = 0xbe7e8ef1

    def __init__(cls, nonce: int):
        cls.nonce = nonce

    @staticmethod
    def read(data) -> "ReqPqMulti":
        nonce = Int128.read(data)
        return ReqPqMulti(nonce=nonce)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int128.getvalue(cls.nonce))
        return data.getvalue()


class ReqDHParams(TL):
    ID = 0xd712e4be

    def __init__(cls, nonce: int, server_nonce: int, p: bytes, q: bytes, public_key_fingerprint: int, encrypted_data: bytes):
        cls.nonce = nonce
        cls.server_nonce = server_nonce
        cls.p = p
        cls.q = q
        cls.public_key_fingerprint = public_key_fingerprint
        cls.encrypted_data = encrypted_data

    @staticmethod
    def read(data) -> "ReqDHParams":
        nonce = Int128.read(data)
        server_nonce = Int128.read(data)
        p = Bytes.read(data)
        q = Bytes.read(data)
        public_key_fingerprint = Long.read(data)
        encrypted_data = Bytes.read(data)
        return ReqDHParams(nonce=nonce, server_nonce=server_nonce, p=p, q=q, public_key_fingerprint=public_key_fingerprint, encrypted_data=encrypted_data)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int128.getvalue(cls.nonce))
        data.write(Int128.getvalue(cls.server_nonce))
        data.write(Bytes.getvalue(cls.p))
        data.write(Bytes.getvalue(cls.q))
        data.write(Long.getvalue(cls.public_key_fingerprint))
        data.write(Bytes.getvalue(cls.encrypted_data))
        return data.getvalue()


class SetClientDHParams(TL):
    ID = 0xf5045f1f

    def __init__(cls, nonce: int, server_nonce: int, encrypted_data: bytes):
        cls.nonce = nonce
        cls.server_nonce = server_nonce
        cls.encrypted_data = encrypted_data

    @staticmethod
    def read(data) -> "SetClientDHParams":
        nonce = Int128.read(data)
        server_nonce = Int128.read(data)
        encrypted_data = Bytes.read(data)
        return SetClientDHParams(nonce=nonce, server_nonce=server_nonce, encrypted_data=encrypted_data)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int128.getvalue(cls.nonce))
        data.write(Int128.getvalue(cls.server_nonce))
        data.write(Bytes.getvalue(cls.encrypted_data))
        return data.getvalue()


class DestroyAuthKey(TL):
    ID = 0xd1435160

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "DestroyAuthKey":
        
        return DestroyAuthKey()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class RpcDropAnswer(TL):
    ID = 0x58e4a740

    def __init__(cls, req_msg_id: int):
        cls.req_msg_id = req_msg_id

    @staticmethod
    def read(data) -> "RpcDropAnswer":
        req_msg_id = Long.read(data)
        return RpcDropAnswer(req_msg_id=req_msg_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.req_msg_id))
        return data.getvalue()


class GetFutureSalts(TL):
    ID = 0xb921bd04

    def __init__(cls, num: int):
        cls.num = num

    @staticmethod
    def read(data) -> "GetFutureSalts":
        num = Int.read(data)
        return GetFutureSalts(num=num)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.num))
        return data.getvalue()


class Ping(TL):
    ID = 0x7abe77ec

    def __init__(cls, ping_id: int):
        cls.ping_id = ping_id

    @staticmethod
    def read(data) -> "Ping":
        ping_id = Long.read(data)
        return Ping(ping_id=ping_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.ping_id))
        return data.getvalue()


class PingDelayDisconnect(TL):
    ID = 0xf3427b8c

    def __init__(cls, ping_id: int, disconnect_delay: int):
        cls.ping_id = ping_id
        cls.disconnect_delay = disconnect_delay

    @staticmethod
    def read(data) -> "PingDelayDisconnect":
        ping_id = Long.read(data)
        disconnect_delay = Int.read(data)
        return PingDelayDisconnect(ping_id=ping_id, disconnect_delay=disconnect_delay)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.ping_id))
        data.write(Int.getvalue(cls.disconnect_delay))
        return data.getvalue()


class DestroySession(TL):
    ID = 0xe7512126

    def __init__(cls, session_id: int):
        cls.session_id = session_id

    @staticmethod
    def read(data) -> "DestroySession":
        session_id = Long.read(data)
        return DestroySession(session_id=session_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.session_id))
        return data.getvalue()
