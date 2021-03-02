from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class GetCallConfig(TL):
    ID = 0x55451fa9

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetCallConfig":
        
        return GetCallConfig()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class RequestCall(TL):
    ID = 0x42ff96ed

    def __init__(cls, user_id: TL, random_id: int, g_a_hash: bytes, protocol: TL, video: bool = None):
        cls.video = video
        cls.user_id = user_id
        cls.random_id = random_id
        cls.g_a_hash = g_a_hash
        cls.protocol = protocol

    @staticmethod
    def read(data) -> "RequestCall":
        flags = Int.read(data)
        video = True if flags & 1 else False
        user_id = data.getobj()
        random_id = Int.read(data)
        g_a_hash = Bytes.read(data)
        protocol = data.getobj()
        return RequestCall(video=video, user_id=user_id, random_id=random_id, g_a_hash=g_a_hash, protocol=protocol)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.video is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.user_id.getvalue())
        data.write(Int.getvalue(cls.random_id))
        data.write(Bytes.getvalue(cls.g_a_hash))
        data.write(cls.protocol.getvalue())
        return data.getvalue()


class AcceptCall(TL):
    ID = 0x3bd2b4a0

    def __init__(cls, peer: TL, g_b: bytes, protocol: TL):
        cls.peer = peer
        cls.g_b = g_b
        cls.protocol = protocol

    @staticmethod
    def read(data) -> "AcceptCall":
        peer = data.getobj()
        g_b = Bytes.read(data)
        protocol = data.getobj()
        return AcceptCall(peer=peer, g_b=g_b, protocol=protocol)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Bytes.getvalue(cls.g_b))
        data.write(cls.protocol.getvalue())
        return data.getvalue()


class ConfirmCall(TL):
    ID = 0x2efe1722

    def __init__(cls, peer: TL, g_a: bytes, key_fingerprint: int, protocol: TL):
        cls.peer = peer
        cls.g_a = g_a
        cls.key_fingerprint = key_fingerprint
        cls.protocol = protocol

    @staticmethod
    def read(data) -> "ConfirmCall":
        peer = data.getobj()
        g_a = Bytes.read(data)
        key_fingerprint = Long.read(data)
        protocol = data.getobj()
        return ConfirmCall(peer=peer, g_a=g_a, key_fingerprint=key_fingerprint, protocol=protocol)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Bytes.getvalue(cls.g_a))
        data.write(Long.getvalue(cls.key_fingerprint))
        data.write(cls.protocol.getvalue())
        return data.getvalue()


class ReceivedCall(TL):
    ID = 0x17d54f61

    def __init__(cls, peer: TL):
        cls.peer = peer

    @staticmethod
    def read(data) -> "ReceivedCall":
        peer = data.getobj()
        return ReceivedCall(peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class DiscardCall(TL):
    ID = 0xb2cbc1c0

    def __init__(cls, peer: TL, duration: int, reason: TL, connection_id: int, video: bool = None):
        cls.video = video
        cls.peer = peer
        cls.duration = duration
        cls.reason = reason
        cls.connection_id = connection_id

    @staticmethod
    def read(data) -> "DiscardCall":
        flags = Int.read(data)
        video = True if flags & 1 else False
        peer = data.getobj()
        duration = Int.read(data)
        reason = data.getobj()
        connection_id = Long.read(data)
        return DiscardCall(video=video, peer=peer, duration=duration, reason=reason, connection_id=connection_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.video is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.duration))
        data.write(cls.reason.getvalue())
        data.write(Long.getvalue(cls.connection_id))
        return data.getvalue()


class SetCallRating(TL):
    ID = 0x59ead627

    def __init__(cls, peer: TL, rating: int, comment: str, user_initiative: bool = None):
        cls.user_initiative = user_initiative
        cls.peer = peer
        cls.rating = rating
        cls.comment = comment

    @staticmethod
    def read(data) -> "SetCallRating":
        flags = Int.read(data)
        user_initiative = True if flags & 1 else False
        peer = data.getobj()
        rating = Int.read(data)
        comment = String.read(data)
        return SetCallRating(user_initiative=user_initiative, peer=peer, rating=rating, comment=comment)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.user_initiative is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.rating))
        data.write(String.getvalue(cls.comment))
        return data.getvalue()


class SaveCallDebug(TL):
    ID = 0x277add7e

    def __init__(cls, peer: TL, debug: TL):
        cls.peer = peer
        cls.debug = debug

    @staticmethod
    def read(data) -> "SaveCallDebug":
        peer = data.getobj()
        debug = data.getobj()
        return SaveCallDebug(peer=peer, debug=debug)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(cls.debug.getvalue())
        return data.getvalue()


class SendSignalingData(TL):
    ID = 0xff7a9383

    def __init__(cls, peer: TL, data: bytes):
        cls.peer = peer
        cls.data = data

    @staticmethod
    def read(data) -> "SendSignalingData":
        peer = data.getobj()
        data = Bytes.read(data)
        return SendSignalingData(peer=peer, data=data)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Bytes.getvalue(cls.data))
        return data.getvalue()


class CreateGroupCall(TL):
    ID = 0xbd3dabe0

    def __init__(cls, peer: TL, random_id: int):
        cls.peer = peer
        cls.random_id = random_id

    @staticmethod
    def read(data) -> "CreateGroupCall":
        peer = data.getobj()
        random_id = Int.read(data)
        return CreateGroupCall(peer=peer, random_id=random_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.random_id))
        return data.getvalue()


class JoinGroupCall(TL):
    ID = 0x5f9c8e62

    def __init__(cls, call: TL, params: TL, muted: bool = None):
        cls.muted = muted
        cls.call = call
        cls.params = params

    @staticmethod
    def read(data) -> "JoinGroupCall":
        flags = Int.read(data)
        muted = True if flags & 1 else False
        call = data.getobj()
        params = data.getobj()
        return JoinGroupCall(muted=muted, call=call, params=params)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.muted is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.call.getvalue())
        data.write(cls.params.getvalue())
        return data.getvalue()


class LeaveGroupCall(TL):
    ID = 0x500377f9

    def __init__(cls, call: TL, source: int):
        cls.call = call
        cls.source = source

    @staticmethod
    def read(data) -> "LeaveGroupCall":
        call = data.getobj()
        source = Int.read(data)
        return LeaveGroupCall(call=call, source=source)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.call.getvalue())
        data.write(Int.getvalue(cls.source))
        return data.getvalue()


class EditGroupCallMember(TL):
    ID = 0xa5e76cd8

    def __init__(cls, call: TL, user_id: TL, muted: bool = None, volume: int = None):
        cls.muted = muted
        cls.call = call
        cls.user_id = user_id
        cls.volume = volume

    @staticmethod
    def read(data) -> "EditGroupCallMember":
        flags = Int.read(data)
        muted = True if flags & 1 else False
        call = data.getobj()
        user_id = data.getobj()
        volume = Int.read(data) if flags & 2 else None
        return EditGroupCallMember(muted=muted, call=call, user_id=user_id, volume=volume)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.muted is not None else 0
        flags |= 2 if cls.volume is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.call.getvalue())
        data.write(cls.user_id.getvalue())
        
        if cls.volume is not None:
            data.write(Int.getvalue(cls.volume))
        return data.getvalue()


class InviteToGroupCall(TL):
    ID = 0x7b393160

    def __init__(cls, call: TL, users: List[TL]):
        cls.call = call
        cls.users = users

    @staticmethod
    def read(data) -> "InviteToGroupCall":
        call = data.getobj()
        users = data.getobj()
        return InviteToGroupCall(call=call, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.call.getvalue())
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class DiscardGroupCall(TL):
    ID = 0x7a777135

    def __init__(cls, call: TL):
        cls.call = call

    @staticmethod
    def read(data) -> "DiscardGroupCall":
        call = data.getobj()
        return DiscardGroupCall(call=call)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.call.getvalue())
        return data.getvalue()


class ToggleGroupCallSettings(TL):
    ID = 0x74bbb43d

    def __init__(cls, call: TL, join_muted: bool = None):
        cls.call = call
        cls.join_muted = join_muted

    @staticmethod
    def read(data) -> "ToggleGroupCallSettings":
        flags = Int.read(data)
        call = data.getobj()
        join_muted = Bool.read(data) if flags & 1 else None
        return ToggleGroupCallSettings(call=call, join_muted=join_muted)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.join_muted is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.call.getvalue())
        return data.getvalue()


class GetGroupCall(TL):
    ID = 0xc7cb017

    def __init__(cls, call: TL):
        cls.call = call

    @staticmethod
    def read(data) -> "GetGroupCall":
        call = data.getobj()
        return GetGroupCall(call=call)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.call.getvalue())
        return data.getvalue()


class GetGroupParticipants(TL):
    ID = 0xc9f1d285

    def __init__(cls, call: TL, ids: List[int], sources: List[int], offset: str, limit: int):
        cls.call = call
        cls.ids = ids
        cls.sources = sources
        cls.offset = offset
        cls.limit = limit

    @staticmethod
    def read(data) -> "GetGroupParticipants":
        call = data.getobj()
        ids = data.getobj(Int)
        sources = data.getobj(Int)
        offset = String.read(data)
        limit = Int.read(data)
        return GetGroupParticipants(call=call, ids=ids, sources=sources, offset=offset, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.call.getvalue())
        data.write(Vector().getvalue(cls.ids, Int))
        data.write(Vector().getvalue(cls.sources, Int))
        data.write(String.getvalue(cls.offset))
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()


class CheckGroupCall(TL):
    ID = 0xb74a7bea

    def __init__(cls, call: TL, source: int):
        cls.call = call
        cls.source = source

    @staticmethod
    def read(data) -> "CheckGroupCall":
        call = data.getobj()
        source = Int.read(data)
        return CheckGroupCall(call=call, source=source)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.call.getvalue())
        data.write(Int.getvalue(cls.source))
        return data.getvalue()
