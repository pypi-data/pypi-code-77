from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class State(TL):
    ID = 0xa56c2a3e

    def __init__(cls, pts: int, qts: int, date: int, seq: int, unread_count: int):
        cls.pts = pts
        cls.qts = qts
        cls.date = date
        cls.seq = seq
        cls.unread_count = unread_count

    @staticmethod
    def read(data) -> "State":
        pts = Int.read(data)
        qts = Int.read(data)
        date = Int.read(data)
        seq = Int.read(data)
        unread_count = Int.read(data)
        return State(pts=pts, qts=qts, date=date, seq=seq, unread_count=unread_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.qts))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.seq))
        data.write(Int.getvalue(cls.unread_count))
        return data.getvalue()


class DifferenceEmpty(TL):
    ID = 0x5d75a138

    def __init__(cls, date: int, seq: int):
        cls.date = date
        cls.seq = seq

    @staticmethod
    def read(data) -> "DifferenceEmpty":
        date = Int.read(data)
        seq = Int.read(data)
        return DifferenceEmpty(date=date, seq=seq)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.seq))
        return data.getvalue()


class Difference(TL):
    ID = 0xf49ca0

    def __init__(cls, new_messages: List[TL], new_encrypted_messages: List[TL], other_updates: List[TL], chats: List[TL], users: List[TL], state: TL):
        cls.new_messages = new_messages
        cls.new_encrypted_messages = new_encrypted_messages
        cls.other_updates = other_updates
        cls.chats = chats
        cls.users = users
        cls.state = state

    @staticmethod
    def read(data) -> "Difference":
        new_messages = data.getobj()
        new_encrypted_messages = data.getobj()
        other_updates = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        state = data.getobj()
        return Difference(new_messages=new_messages, new_encrypted_messages=new_encrypted_messages, other_updates=other_updates, chats=chats, users=users, state=state)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.new_messages))
        data.write(Vector().getvalue(cls.new_encrypted_messages))
        data.write(Vector().getvalue(cls.other_updates))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        data.write(cls.state.getvalue())
        return data.getvalue()


class DifferenceSlice(TL):
    ID = 0xa8fb1981

    def __init__(cls, new_messages: List[TL], new_encrypted_messages: List[TL], other_updates: List[TL], chats: List[TL], users: List[TL], intermediate_state: TL):
        cls.new_messages = new_messages
        cls.new_encrypted_messages = new_encrypted_messages
        cls.other_updates = other_updates
        cls.chats = chats
        cls.users = users
        cls.intermediate_state = intermediate_state

    @staticmethod
    def read(data) -> "DifferenceSlice":
        new_messages = data.getobj()
        new_encrypted_messages = data.getobj()
        other_updates = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        intermediate_state = data.getobj()
        return DifferenceSlice(new_messages=new_messages, new_encrypted_messages=new_encrypted_messages, other_updates=other_updates, chats=chats, users=users, intermediate_state=intermediate_state)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.new_messages))
        data.write(Vector().getvalue(cls.new_encrypted_messages))
        data.write(Vector().getvalue(cls.other_updates))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        data.write(cls.intermediate_state.getvalue())
        return data.getvalue()


class DifferenceTooLong(TL):
    ID = 0x4afe8f6d

    def __init__(cls, pts: int):
        cls.pts = pts

    @staticmethod
    def read(data) -> "DifferenceTooLong":
        pts = Int.read(data)
        return DifferenceTooLong(pts=pts)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.pts))
        return data.getvalue()


class ChannelDifferenceEmpty(TL):
    ID = 0x3e11affb

    def __init__(cls, pts: int, final: bool = None, timeout: int = None):
        cls.final = final
        cls.pts = pts
        cls.timeout = timeout

    @staticmethod
    def read(data) -> "ChannelDifferenceEmpty":
        flags = Int.read(data)
        final = True if flags & 1 else False
        pts = Int.read(data)
        timeout = Int.read(data) if flags & 2 else None
        return ChannelDifferenceEmpty(final=final, pts=pts, timeout=timeout)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.final is not None else 0
        flags |= 2 if cls.timeout is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.pts))
        
        if cls.timeout is not None:
            data.write(Int.getvalue(cls.timeout))
        return data.getvalue()


class ChannelDifferenceTooLong(TL):
    ID = 0xa4bcc6fe

    def __init__(cls, dialog: TL, messages: List[TL], chats: List[TL], users: List[TL], final: bool = None, timeout: int = None):
        cls.final = final
        cls.timeout = timeout
        cls.dialog = dialog
        cls.messages = messages
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "ChannelDifferenceTooLong":
        flags = Int.read(data)
        final = True if flags & 1 else False
        timeout = Int.read(data) if flags & 2 else None
        dialog = data.getobj()
        messages = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return ChannelDifferenceTooLong(final=final, timeout=timeout, dialog=dialog, messages=messages, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.final is not None else 0
        flags |= 2 if cls.timeout is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.timeout is not None:
            data.write(Int.getvalue(cls.timeout))
        data.write(cls.dialog.getvalue())
        data.write(Vector().getvalue(cls.messages))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class ChannelDifference(TL):
    ID = 0x2064674e

    def __init__(cls, pts: int, new_messages: List[TL], other_updates: List[TL], chats: List[TL], users: List[TL], final: bool = None, timeout: int = None):
        cls.final = final
        cls.pts = pts
        cls.timeout = timeout
        cls.new_messages = new_messages
        cls.other_updates = other_updates
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "ChannelDifference":
        flags = Int.read(data)
        final = True if flags & 1 else False
        pts = Int.read(data)
        timeout = Int.read(data) if flags & 2 else None
        new_messages = data.getobj()
        other_updates = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return ChannelDifference(final=final, pts=pts, timeout=timeout, new_messages=new_messages, other_updates=other_updates, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.final is not None else 0
        flags |= 2 if cls.timeout is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.pts))
        
        if cls.timeout is not None:
            data.write(Int.getvalue(cls.timeout))
        data.write(Vector().getvalue(cls.new_messages))
        data.write(Vector().getvalue(cls.other_updates))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()
