from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class GetBroadcastStats(TL):
    ID = 0xab42441a

    def __init__(cls, channel: TL, dark: bool = None):
        cls.dark = dark
        cls.channel = channel

    @staticmethod
    def read(data) -> "GetBroadcastStats":
        flags = Int.read(data)
        dark = True if flags & 1 else False
        channel = data.getobj()
        return GetBroadcastStats(dark=dark, channel=channel)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.dark is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.channel.getvalue())
        return data.getvalue()


class LoadAsyncGraph(TL):
    ID = 0x621d5fa0

    def __init__(cls, token: str, x: int = None):
        cls.token = token
        cls.x = x

    @staticmethod
    def read(data) -> "LoadAsyncGraph":
        flags = Int.read(data)
        token = String.read(data)
        x = Long.read(data) if flags & 1 else None
        return LoadAsyncGraph(token=token, x=x)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.x is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.token))
        
        if cls.x is not None:
            data.write(Long.getvalue(cls.x))
        return data.getvalue()


class GetMegagroupStats(TL):
    ID = 0xdcdf8607

    def __init__(cls, channel: TL, dark: bool = None):
        cls.dark = dark
        cls.channel = channel

    @staticmethod
    def read(data) -> "GetMegagroupStats":
        flags = Int.read(data)
        dark = True if flags & 1 else False
        channel = data.getobj()
        return GetMegagroupStats(dark=dark, channel=channel)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.dark is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.channel.getvalue())
        return data.getvalue()


class GetMessagePublicForwards(TL):
    ID = 0x5630281b

    def __init__(cls, channel: TL, msg_id: int, offset_rate: int, offset_peer: TL, offset_id: int, limit: int):
        cls.channel = channel
        cls.msg_id = msg_id
        cls.offset_rate = offset_rate
        cls.offset_peer = offset_peer
        cls.offset_id = offset_id
        cls.limit = limit

    @staticmethod
    def read(data) -> "GetMessagePublicForwards":
        channel = data.getobj()
        msg_id = Int.read(data)
        offset_rate = Int.read(data)
        offset_peer = data.getobj()
        offset_id = Int.read(data)
        limit = Int.read(data)
        return GetMessagePublicForwards(channel=channel, msg_id=msg_id, offset_rate=offset_rate, offset_peer=offset_peer, offset_id=offset_id, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        data.write(Int.getvalue(cls.offset_rate))
        data.write(cls.offset_peer.getvalue())
        data.write(Int.getvalue(cls.offset_id))
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()


class GetMessageStats(TL):
    ID = 0xb6e0a3f5

    def __init__(cls, channel: TL, msg_id: int, dark: bool = None):
        cls.dark = dark
        cls.channel = channel
        cls.msg_id = msg_id

    @staticmethod
    def read(data) -> "GetMessageStats":
        flags = Int.read(data)
        dark = True if flags & 1 else False
        channel = data.getobj()
        msg_id = Int.read(data)
        return GetMessageStats(dark=dark, channel=channel, msg_id=msg_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.dark is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.channel.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        return data.getvalue()
