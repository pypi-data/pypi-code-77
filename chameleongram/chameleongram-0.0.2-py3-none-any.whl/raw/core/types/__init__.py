from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO
from .help import ConfigSimple

class ResPQ(TL):
    ID = 0x05162463

    def __init__(cls, nonce: int, server_nonce: int, pq: bytes, server_public_key_fingerprints: List[int]):
        cls.nonce = nonce
        cls.server_nonce = server_nonce
        cls.pq = pq
        cls.server_public_key_fingerprints = server_public_key_fingerprints

    @staticmethod
    def read(data) -> "ResPQ":
        nonce = Int128.read(data)
        server_nonce = Int128.read(data)
        pq = Bytes.read(data)
        server_public_key_fingerprints = data.getobj(Long)
        return ResPQ(nonce=nonce, server_nonce=server_nonce, pq=pq, server_public_key_fingerprints=server_public_key_fingerprints)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int128.getvalue(cls.nonce))
        data.write(Int128.getvalue(cls.server_nonce))
        data.write(Bytes.getvalue(cls.pq))
        data.write(Vector().getvalue(cls.server_public_key_fingerprints, Long))
        return data.getvalue()


class PQInnerData(TL):
    ID = 0x83c95aec

    def __init__(cls, pq: bytes, p: bytes, q: bytes, nonce: int, server_nonce: int, new_nonce: int):
        cls.pq = pq
        cls.p = p
        cls.q = q
        cls.nonce = nonce
        cls.server_nonce = server_nonce
        cls.new_nonce = new_nonce

    @staticmethod
    def read(data) -> "PQInnerData":
        pq = Bytes.read(data)
        p = Bytes.read(data)
        q = Bytes.read(data)
        nonce = Int128.read(data)
        server_nonce = Int128.read(data)
        new_nonce = Int256.read(data)
        return PQInnerData(pq=pq, p=p, q=q, nonce=nonce, server_nonce=server_nonce, new_nonce=new_nonce)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.pq))
        data.write(Bytes.getvalue(cls.p))
        data.write(Bytes.getvalue(cls.q))
        data.write(Int128.getvalue(cls.nonce))
        data.write(Int128.getvalue(cls.server_nonce))
        data.write(Int256.getvalue(cls.new_nonce))
        return data.getvalue()


class PQInnerDataDc(TL):
    ID = 0xa9f55f95

    def __init__(cls, pq: bytes, p: bytes, q: bytes, nonce: int, server_nonce: int, new_nonce: int, dc: int):
        cls.pq = pq
        cls.p = p
        cls.q = q
        cls.nonce = nonce
        cls.server_nonce = server_nonce
        cls.new_nonce = new_nonce
        cls.dc = dc

    @staticmethod
    def read(data) -> "PQInnerDataDc":
        pq = Bytes.read(data)
        p = Bytes.read(data)
        q = Bytes.read(data)
        nonce = Int128.read(data)
        server_nonce = Int128.read(data)
        new_nonce = Int256.read(data)
        dc = Int.read(data)
        return PQInnerDataDc(pq=pq, p=p, q=q, nonce=nonce, server_nonce=server_nonce, new_nonce=new_nonce, dc=dc)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.pq))
        data.write(Bytes.getvalue(cls.p))
        data.write(Bytes.getvalue(cls.q))
        data.write(Int128.getvalue(cls.nonce))
        data.write(Int128.getvalue(cls.server_nonce))
        data.write(Int256.getvalue(cls.new_nonce))
        data.write(Int.getvalue(cls.dc))
        return data.getvalue()


class PQInnerDataTemp(TL):
    ID = 0x3c6a84d4

    def __init__(cls, pq: bytes, p: bytes, q: bytes, nonce: int, server_nonce: int, new_nonce: int, expires_in: int):
        cls.pq = pq
        cls.p = p
        cls.q = q
        cls.nonce = nonce
        cls.server_nonce = server_nonce
        cls.new_nonce = new_nonce
        cls.expires_in = expires_in

    @staticmethod
    def read(data) -> "PQInnerDataTemp":
        pq = Bytes.read(data)
        p = Bytes.read(data)
        q = Bytes.read(data)
        nonce = Int128.read(data)
        server_nonce = Int128.read(data)
        new_nonce = Int256.read(data)
        expires_in = Int.read(data)
        return PQInnerDataTemp(pq=pq, p=p, q=q, nonce=nonce, server_nonce=server_nonce, new_nonce=new_nonce, expires_in=expires_in)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.pq))
        data.write(Bytes.getvalue(cls.p))
        data.write(Bytes.getvalue(cls.q))
        data.write(Int128.getvalue(cls.nonce))
        data.write(Int128.getvalue(cls.server_nonce))
        data.write(Int256.getvalue(cls.new_nonce))
        data.write(Int.getvalue(cls.expires_in))
        return data.getvalue()


class PQInnerDataTempDc(TL):
    ID = 0x56fddf88

    def __init__(cls, pq: bytes, p: bytes, q: bytes, nonce: int, server_nonce: int, new_nonce: int, dc: int, expires_in: int):
        cls.pq = pq
        cls.p = p
        cls.q = q
        cls.nonce = nonce
        cls.server_nonce = server_nonce
        cls.new_nonce = new_nonce
        cls.dc = dc
        cls.expires_in = expires_in

    @staticmethod
    def read(data) -> "PQInnerDataTempDc":
        pq = Bytes.read(data)
        p = Bytes.read(data)
        q = Bytes.read(data)
        nonce = Int128.read(data)
        server_nonce = Int128.read(data)
        new_nonce = Int256.read(data)
        dc = Int.read(data)
        expires_in = Int.read(data)
        return PQInnerDataTempDc(pq=pq, p=p, q=q, nonce=nonce, server_nonce=server_nonce, new_nonce=new_nonce, dc=dc, expires_in=expires_in)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.pq))
        data.write(Bytes.getvalue(cls.p))
        data.write(Bytes.getvalue(cls.q))
        data.write(Int128.getvalue(cls.nonce))
        data.write(Int128.getvalue(cls.server_nonce))
        data.write(Int256.getvalue(cls.new_nonce))
        data.write(Int.getvalue(cls.dc))
        data.write(Int.getvalue(cls.expires_in))
        return data.getvalue()


class BindAuthKeyInner(TL):
    ID = 0x75a3f765

    def __init__(cls, nonce: int, temp_auth_key_id: int, perm_auth_key_id: int, temp_session_id: int, expires_at: int):
        cls.nonce = nonce
        cls.temp_auth_key_id = temp_auth_key_id
        cls.perm_auth_key_id = perm_auth_key_id
        cls.temp_session_id = temp_session_id
        cls.expires_at = expires_at

    @staticmethod
    def read(data) -> "BindAuthKeyInner":
        nonce = Long.read(data)
        temp_auth_key_id = Long.read(data)
        perm_auth_key_id = Long.read(data)
        temp_session_id = Long.read(data)
        expires_at = Int.read(data)
        return BindAuthKeyInner(nonce=nonce, temp_auth_key_id=temp_auth_key_id, perm_auth_key_id=perm_auth_key_id, temp_session_id=temp_session_id, expires_at=expires_at)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.nonce))
        data.write(Long.getvalue(cls.temp_auth_key_id))
        data.write(Long.getvalue(cls.perm_auth_key_id))
        data.write(Long.getvalue(cls.temp_session_id))
        data.write(Int.getvalue(cls.expires_at))
        return data.getvalue()


class ServerDHParamsFail(TL):
    ID = 0x79cb045d

    def __init__(cls, nonce: int, server_nonce: int, new_nonce_hash: int):
        cls.nonce = nonce
        cls.server_nonce = server_nonce
        cls.new_nonce_hash = new_nonce_hash

    @staticmethod
    def read(data) -> "ServerDHParamsFail":
        nonce = Int128.read(data)
        server_nonce = Int128.read(data)
        new_nonce_hash = Int128.read(data)
        return ServerDHParamsFail(nonce=nonce, server_nonce=server_nonce, new_nonce_hash=new_nonce_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int128.getvalue(cls.nonce))
        data.write(Int128.getvalue(cls.server_nonce))
        data.write(Int128.getvalue(cls.new_nonce_hash))
        return data.getvalue()


class ServerDHParamsOk(TL):
    ID = 0xd0e8075c

    def __init__(cls, nonce: int, server_nonce: int, encrypted_answer: bytes):
        cls.nonce = nonce
        cls.server_nonce = server_nonce
        cls.encrypted_answer = encrypted_answer

    @staticmethod
    def read(data) -> "ServerDHParamsOk":
        nonce = Int128.read(data)
        server_nonce = Int128.read(data)
        encrypted_answer = Bytes.read(data)
        return ServerDHParamsOk(nonce=nonce, server_nonce=server_nonce, encrypted_answer=encrypted_answer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int128.getvalue(cls.nonce))
        data.write(Int128.getvalue(cls.server_nonce))
        data.write(Bytes.getvalue(cls.encrypted_answer))
        return data.getvalue()


class ServerDHInnerData(TL):
    ID = 0xb5890dba

    def __init__(cls, nonce: int, server_nonce: int, g: int, dh_prime: bytes, g_a: bytes, server_time: int):
        cls.nonce = nonce
        cls.server_nonce = server_nonce
        cls.g = g
        cls.dh_prime = dh_prime
        cls.g_a = g_a
        cls.server_time = server_time

    @staticmethod
    def read(data) -> "ServerDHInnerData":
        nonce = Int128.read(data)
        server_nonce = Int128.read(data)
        g = Int.read(data)
        dh_prime = Bytes.read(data)
        g_a = Bytes.read(data)
        server_time = Int.read(data)
        return ServerDHInnerData(nonce=nonce, server_nonce=server_nonce, g=g, dh_prime=dh_prime, g_a=g_a, server_time=server_time)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int128.getvalue(cls.nonce))
        data.write(Int128.getvalue(cls.server_nonce))
        data.write(Int.getvalue(cls.g))
        data.write(Bytes.getvalue(cls.dh_prime))
        data.write(Bytes.getvalue(cls.g_a))
        data.write(Int.getvalue(cls.server_time))
        return data.getvalue()


class ClientDHInnerData(TL):
    ID = 0x6643b654

    def __init__(cls, nonce: int, server_nonce: int, retry_id: int, g_b: bytes):
        cls.nonce = nonce
        cls.server_nonce = server_nonce
        cls.retry_id = retry_id
        cls.g_b = g_b

    @staticmethod
    def read(data) -> "ClientDHInnerData":
        nonce = Int128.read(data)
        server_nonce = Int128.read(data)
        retry_id = Long.read(data)
        g_b = Bytes.read(data)
        return ClientDHInnerData(nonce=nonce, server_nonce=server_nonce, retry_id=retry_id, g_b=g_b)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int128.getvalue(cls.nonce))
        data.write(Int128.getvalue(cls.server_nonce))
        data.write(Long.getvalue(cls.retry_id))
        data.write(Bytes.getvalue(cls.g_b))
        return data.getvalue()


class DhGenOk(TL):
    ID = 0x3bcbf734

    def __init__(cls, nonce: int, server_nonce: int, new_nonce_hash1: int):
        cls.nonce = nonce
        cls.server_nonce = server_nonce
        cls.new_nonce_hash1 = new_nonce_hash1

    @staticmethod
    def read(data) -> "DhGenOk":
        nonce = Int128.read(data)
        server_nonce = Int128.read(data)
        new_nonce_hash1 = Int128.read(data)
        return DhGenOk(nonce=nonce, server_nonce=server_nonce, new_nonce_hash1=new_nonce_hash1)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int128.getvalue(cls.nonce))
        data.write(Int128.getvalue(cls.server_nonce))
        data.write(Int128.getvalue(cls.new_nonce_hash1))
        return data.getvalue()


class DhGenRetry(TL):
    ID = 0x46dc1fb9

    def __init__(cls, nonce: int, server_nonce: int, new_nonce_hash2: int):
        cls.nonce = nonce
        cls.server_nonce = server_nonce
        cls.new_nonce_hash2 = new_nonce_hash2

    @staticmethod
    def read(data) -> "DhGenRetry":
        nonce = Int128.read(data)
        server_nonce = Int128.read(data)
        new_nonce_hash2 = Int128.read(data)
        return DhGenRetry(nonce=nonce, server_nonce=server_nonce, new_nonce_hash2=new_nonce_hash2)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int128.getvalue(cls.nonce))
        data.write(Int128.getvalue(cls.server_nonce))
        data.write(Int128.getvalue(cls.new_nonce_hash2))
        return data.getvalue()


class DhGenFail(TL):
    ID = 0xa69dae02

    def __init__(cls, nonce: int, server_nonce: int, new_nonce_hash3: int):
        cls.nonce = nonce
        cls.server_nonce = server_nonce
        cls.new_nonce_hash3 = new_nonce_hash3

    @staticmethod
    def read(data) -> "DhGenFail":
        nonce = Int128.read(data)
        server_nonce = Int128.read(data)
        new_nonce_hash3 = Int128.read(data)
        return DhGenFail(nonce=nonce, server_nonce=server_nonce, new_nonce_hash3=new_nonce_hash3)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int128.getvalue(cls.nonce))
        data.write(Int128.getvalue(cls.server_nonce))
        data.write(Int128.getvalue(cls.new_nonce_hash3))
        return data.getvalue()


class DestroyAuthKeyOk(TL):
    ID = 0xf660e1d4

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "DestroyAuthKeyOk":
        
        return DestroyAuthKeyOk()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class DestroyAuthKeyNone(TL):
    ID = 0x0a9f2259

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "DestroyAuthKeyNone":
        
        return DestroyAuthKeyNone()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class DestroyAuthKeyFail(TL):
    ID = 0xea109b13

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "DestroyAuthKeyFail":
        
        return DestroyAuthKeyFail()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class MsgsAck(TL):
    ID = 0x62d6b459

    def __init__(cls, msg_ids: List[int]):
        cls.msg_ids = msg_ids

    @staticmethod
    def read(data) -> "MsgsAck":
        msg_ids = data.getobj(Long)
        return MsgsAck(msg_ids=msg_ids)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.msg_ids, Long))
        return data.getvalue()


class BadMsgNotification(TL):
    ID = 0xa7eff811

    def __init__(cls, bad_msg_id: int, bad_msg_seqno: int, error_code: int):
        cls.bad_msg_id = bad_msg_id
        cls.bad_msg_seqno = bad_msg_seqno
        cls.error_code = error_code

    @staticmethod
    def read(data) -> "BadMsgNotification":
        bad_msg_id = Long.read(data)
        bad_msg_seqno = Int.read(data)
        error_code = Int.read(data)
        return BadMsgNotification(bad_msg_id=bad_msg_id, bad_msg_seqno=bad_msg_seqno, error_code=error_code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.bad_msg_id))
        data.write(Int.getvalue(cls.bad_msg_seqno))
        data.write(Int.getvalue(cls.error_code))
        return data.getvalue()


class BadServerSalt(TL):
    ID = 0xedab447b

    def __init__(cls, bad_msg_id: int, bad_msg_seqno: int, error_code: int, new_server_salt: int):
        cls.bad_msg_id = bad_msg_id
        cls.bad_msg_seqno = bad_msg_seqno
        cls.error_code = error_code
        cls.new_server_salt = new_server_salt

    @staticmethod
    def read(data) -> "BadServerSalt":
        bad_msg_id = Long.read(data)
        bad_msg_seqno = Int.read(data)
        error_code = Int.read(data)
        new_server_salt = Long.read(data)
        return BadServerSalt(bad_msg_id=bad_msg_id, bad_msg_seqno=bad_msg_seqno, error_code=error_code, new_server_salt=new_server_salt)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.bad_msg_id))
        data.write(Int.getvalue(cls.bad_msg_seqno))
        data.write(Int.getvalue(cls.error_code))
        data.write(Long.getvalue(cls.new_server_salt))
        return data.getvalue()


class MsgsStateReq(TL):
    ID = 0xda69fb52

    def __init__(cls, msg_ids: List[int]):
        cls.msg_ids = msg_ids

    @staticmethod
    def read(data) -> "MsgsStateReq":
        msg_ids = data.getobj(Long)
        return MsgsStateReq(msg_ids=msg_ids)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.msg_ids, Long))
        return data.getvalue()


class MsgsStateInfo(TL):
    ID = 0x04deb57d

    def __init__(cls, req_msg_id: int, info: str):
        cls.req_msg_id = req_msg_id
        cls.info = info

    @staticmethod
    def read(data) -> "MsgsStateInfo":
        req_msg_id = Long.read(data)
        info = String.read(data)
        return MsgsStateInfo(req_msg_id=req_msg_id, info=info)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.req_msg_id))
        data.write(String.getvalue(cls.info))
        return data.getvalue()


class MsgsAllInfo(TL):
    ID = 0x8cc0d131

    def __init__(cls, msg_ids: List[int], info: str):
        cls.msg_ids = msg_ids
        cls.info = info

    @staticmethod
    def read(data) -> "MsgsAllInfo":
        msg_ids = data.getobj(Long)
        info = String.read(data)
        return MsgsAllInfo(msg_ids=msg_ids, info=info)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.msg_ids, Long))
        data.write(String.getvalue(cls.info))
        return data.getvalue()


class MsgDetailedInfo(TL):
    ID = 0x276d3ec6

    def __init__(cls, msg_id: int, answer_msg_id: int, bytes: int, status: int):
        cls.msg_id = msg_id
        cls.answer_msg_id = answer_msg_id
        cls.bytes = bytes
        cls.status = status

    @staticmethod
    def read(data) -> "MsgDetailedInfo":
        msg_id = Long.read(data)
        answer_msg_id = Long.read(data)
        bytes = Int.read(data)
        status = Int.read(data)
        return MsgDetailedInfo(msg_id=msg_id, answer_msg_id=answer_msg_id, bytes=bytes, status=status)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.msg_id))
        data.write(Long.getvalue(cls.answer_msg_id))
        data.write(Int.getvalue(cls.bytes))
        data.write(Int.getvalue(cls.status))
        return data.getvalue()


class MsgNewDetailedInfo(TL):
    ID = 0x809db6df

    def __init__(cls, answer_msg_id: int, bytes: int, status: int):
        cls.answer_msg_id = answer_msg_id
        cls.bytes = bytes
        cls.status = status

    @staticmethod
    def read(data) -> "MsgNewDetailedInfo":
        answer_msg_id = Long.read(data)
        bytes = Int.read(data)
        status = Int.read(data)
        return MsgNewDetailedInfo(answer_msg_id=answer_msg_id, bytes=bytes, status=status)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.answer_msg_id))
        data.write(Int.getvalue(cls.bytes))
        data.write(Int.getvalue(cls.status))
        return data.getvalue()


class MsgResendReq(TL):
    ID = 0x7d861a08

    def __init__(cls, msg_ids: List[int]):
        cls.msg_ids = msg_ids

    @staticmethod
    def read(data) -> "MsgResendReq":
        msg_ids = data.getobj(Long)
        return MsgResendReq(msg_ids=msg_ids)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.msg_ids, Long))
        return data.getvalue()


class RpcResult(TL):
    ID = 0xf35c6d01

    def __init__(cls, req_msg_id: int, result: TL):
        cls.req_msg_id = req_msg_id
        cls.result = result

    @staticmethod
    def read(data) -> "RpcResult":
        req_msg_id = Long.read(data)
        result = data.getobj()
        return RpcResult(req_msg_id=req_msg_id, result=result)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.req_msg_id))
        data.write(cls.result.getvalue())
        return data.getvalue()


class RpcError(TL):
    ID = 0x2144ca19

    def __init__(cls, error_code: int, error_message: str):
        cls.error_code = error_code
        cls.error_message = error_message

    @staticmethod
    def read(data) -> "RpcError":
        error_code = Int.read(data)
        error_message = String.read(data)
        return RpcError(error_code=error_code, error_message=error_message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.error_code))
        data.write(String.getvalue(cls.error_message))
        return data.getvalue()


class RpcAnswerUnknown(TL):
    ID = 0x5e2ad36e

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "RpcAnswerUnknown":
        
        return RpcAnswerUnknown()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class RpcAnswerDroppedRunning(TL):
    ID = 0xcd78e586

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "RpcAnswerDroppedRunning":
        
        return RpcAnswerDroppedRunning()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class RpcAnswerDropped(TL):
    ID = 0xa43ad8b7

    def __init__(cls, msg_id: int, seq_no: int, bytes: int):
        cls.msg_id = msg_id
        cls.seq_no = seq_no
        cls.bytes = bytes

    @staticmethod
    def read(data) -> "RpcAnswerDropped":
        msg_id = Long.read(data)
        seq_no = Int.read(data)
        bytes = Int.read(data)
        return RpcAnswerDropped(msg_id=msg_id, seq_no=seq_no, bytes=bytes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.msg_id))
        data.write(Int.getvalue(cls.seq_no))
        data.write(Int.getvalue(cls.bytes))
        return data.getvalue()


class Pong(TL):
    ID = 0x347773c5

    def __init__(cls, msg_id: int, ping_id: int):
        cls.msg_id = msg_id
        cls.ping_id = ping_id

    @staticmethod
    def read(data) -> "Pong":
        msg_id = Long.read(data)
        ping_id = Long.read(data)
        return Pong(msg_id=msg_id, ping_id=ping_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.msg_id))
        data.write(Long.getvalue(cls.ping_id))
        return data.getvalue()


class DestroySessionOk(TL):
    ID = 0xe22045fc

    def __init__(cls, session_id: int):
        cls.session_id = session_id

    @staticmethod
    def read(data) -> "DestroySessionOk":
        session_id = Long.read(data)
        return DestroySessionOk(session_id=session_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.session_id))
        return data.getvalue()


class DestroySessionNone(TL):
    ID = 0x62d350c9

    def __init__(cls, session_id: int):
        cls.session_id = session_id

    @staticmethod
    def read(data) -> "DestroySessionNone":
        session_id = Long.read(data)
        return DestroySessionNone(session_id=session_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.session_id))
        return data.getvalue()


class NewSessionCreated(TL):
    ID = 0x9ec20908

    def __init__(cls, first_msg_id: int, unique_id: int, server_salt: int):
        cls.first_msg_id = first_msg_id
        cls.unique_id = unique_id
        cls.server_salt = server_salt

    @staticmethod
    def read(data) -> "NewSessionCreated":
        first_msg_id = Long.read(data)
        unique_id = Long.read(data)
        server_salt = Long.read(data)
        return NewSessionCreated(first_msg_id=first_msg_id, unique_id=unique_id, server_salt=server_salt)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.first_msg_id))
        data.write(Long.getvalue(cls.unique_id))
        data.write(Long.getvalue(cls.server_salt))
        return data.getvalue()


class HttpWait(TL):
    ID = 0x9299359f

    def __init__(cls, max_delay: int, wait_after: int, max_wait: int):
        cls.max_delay = max_delay
        cls.wait_after = wait_after
        cls.max_wait = max_wait

    @staticmethod
    def read(data) -> "HttpWait":
        max_delay = Int.read(data)
        wait_after = Int.read(data)
        max_wait = Int.read(data)
        return HttpWait(max_delay=max_delay, wait_after=wait_after, max_wait=max_wait)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.max_delay))
        data.write(Int.getvalue(cls.wait_after))
        data.write(Int.getvalue(cls.max_wait))
        return data.getvalue()


class IpPort(TL):
    ID = 0xd433ad73

    def __init__(cls, ipv4: int, port: int):
        cls.ipv4 = ipv4
        cls.port = port

    @staticmethod
    def read(data) -> "IpPort":
        ipv4 = Int.read(data)
        port = Int.read(data)
        return IpPort(ipv4=ipv4, port=port)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.ipv4))
        data.write(Int.getvalue(cls.port))
        return data.getvalue()


class IpPortSecret(TL):
    ID = 0x37982646

    def __init__(cls, ipv4: int, port: int, secret: bytes):
        cls.ipv4 = ipv4
        cls.port = port
        cls.secret = secret

    @staticmethod
    def read(data) -> "IpPortSecret":
        ipv4 = Int.read(data)
        port = Int.read(data)
        secret = Bytes.read(data)
        return IpPortSecret(ipv4=ipv4, port=port, secret=secret)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.ipv4))
        data.write(Int.getvalue(cls.port))
        data.write(Bytes.getvalue(cls.secret))
        return data.getvalue()


class AccessPointRule(TL):
    ID = 0x4679b65f

    def __init__(cls, phone_prefix_rules: str, dc_id: int, ips: List[TL]):
        cls.phone_prefix_rules = phone_prefix_rules
        cls.dc_id = dc_id
        cls.ips = ips

    @staticmethod
    def read(data) -> "AccessPointRule":
        phone_prefix_rules = String.read(data)
        dc_id = Int.read(data)
        ips = data.getobj()
        return AccessPointRule(phone_prefix_rules=phone_prefix_rules, dc_id=dc_id, ips=ips)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone_prefix_rules))
        data.write(Int.getvalue(cls.dc_id))
        data.write(Vector().getvalue(cls.ips))
        return data.getvalue()
