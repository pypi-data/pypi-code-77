from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class PhoneCall(TL):
    ID = 0xec82e140

    def __init__(cls, phone_call: TL, users: List[TL]):
        cls.phone_call = phone_call
        cls.users = users

    @staticmethod
    def read(data) -> "PhoneCall":
        phone_call = data.getobj()
        users = data.getobj()
        return PhoneCall(phone_call=phone_call, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.phone_call.getvalue())
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class GroupCall(TL):
    ID = 0x66ab0bfc

    def __init__(cls, call: TL, participants: List[TL], participants_next_offset: str, users: List[TL]):
        cls.call = call
        cls.participants = participants
        cls.participants_next_offset = participants_next_offset
        cls.users = users

    @staticmethod
    def read(data) -> "GroupCall":
        call = data.getobj()
        participants = data.getobj()
        participants_next_offset = String.read(data)
        users = data.getobj()
        return GroupCall(call=call, participants=participants, participants_next_offset=participants_next_offset, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.call.getvalue())
        data.write(Vector().getvalue(cls.participants))
        data.write(String.getvalue(cls.participants_next_offset))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class GroupParticipants(TL):
    ID = 0x9cfeb92d

    def __init__(cls, count: int, participants: List[TL], next_offset: str, users: List[TL], version: int):
        cls.count = count
        cls.participants = participants
        cls.next_offset = next_offset
        cls.users = users
        cls.version = version

    @staticmethod
    def read(data) -> "GroupParticipants":
        count = Int.read(data)
        participants = data.getobj()
        next_offset = String.read(data)
        users = data.getobj()
        version = Int.read(data)
        return GroupParticipants(count=count, participants=participants, next_offset=next_offset, users=users, version=version)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.count))
        data.write(Vector().getvalue(cls.participants))
        data.write(String.getvalue(cls.next_offset))
        data.write(Vector().getvalue(cls.users))
        data.write(Int.getvalue(cls.version))
        return data.getvalue()
