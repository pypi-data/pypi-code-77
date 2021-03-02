from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class ChannelParticipants(TL):
    ID = 0xf56ee2a8

    def __init__(cls, count: int, participants: List[TL], users: List[TL]):
        cls.count = count
        cls.participants = participants
        cls.users = users

    @staticmethod
    def read(data) -> "ChannelParticipants":
        count = Int.read(data)
        participants = data.getobj()
        users = data.getobj()
        return ChannelParticipants(count=count, participants=participants, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.count))
        data.write(Vector().getvalue(cls.participants))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class ChannelParticipantsNotModified(TL):
    ID = 0xf0173fe9

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ChannelParticipantsNotModified":
        
        return ChannelParticipantsNotModified()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ChannelParticipant(TL):
    ID = 0xd0d9b163

    def __init__(cls, participant: TL, users: List[TL]):
        cls.participant = participant
        cls.users = users

    @staticmethod
    def read(data) -> "ChannelParticipant":
        participant = data.getobj()
        users = data.getobj()
        return ChannelParticipant(participant=participant, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.participant.getvalue())
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class AdminLogResults(TL):
    ID = 0xed8af74d

    def __init__(cls, events: List[TL], chats: List[TL], users: List[TL]):
        cls.events = events
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "AdminLogResults":
        events = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return AdminLogResults(events=events, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.events))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()
