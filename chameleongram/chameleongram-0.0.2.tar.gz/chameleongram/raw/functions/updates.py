from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class GetState(TL):
    ID = 0xedd4882a

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetState":
        
        return GetState()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetDifference(TL):
    ID = 0x25939651

    def __init__(cls, pts: int, date: int, qts: int, pts_total_limit: int = None):
        cls.pts = pts
        cls.pts_total_limit = pts_total_limit
        cls.date = date
        cls.qts = qts

    @staticmethod
    def read(data) -> "GetDifference":
        flags = Int.read(data)
        pts = Int.read(data)
        pts_total_limit = Int.read(data) if flags & 1 else None
        date = Int.read(data)
        qts = Int.read(data)
        return GetDifference(pts=pts, pts_total_limit=pts_total_limit, date=date, qts=qts)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.pts_total_limit is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.pts))
        
        if cls.pts_total_limit is not None:
            data.write(Int.getvalue(cls.pts_total_limit))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.qts))
        return data.getvalue()


class GetChannelDifference(TL):
    ID = 0x3173d78

    def __init__(cls, channel: TL, filter: TL, pts: int, limit: int, force: bool = None):
        cls.force = force
        cls.channel = channel
        cls.filter = filter
        cls.pts = pts
        cls.limit = limit

    @staticmethod
    def read(data) -> "GetChannelDifference":
        flags = Int.read(data)
        force = True if flags & 1 else False
        channel = data.getobj()
        filter = data.getobj()
        pts = Int.read(data)
        limit = Int.read(data)
        return GetChannelDifference(force=force, channel=channel, filter=filter, pts=pts, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.force is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.channel.getvalue())
        data.write(cls.filter.getvalue())
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()
