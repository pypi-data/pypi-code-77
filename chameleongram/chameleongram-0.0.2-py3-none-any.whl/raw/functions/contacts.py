from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class GetContactIDs(TL):
    ID = 0x2caa4a42

    def __init__(cls, hash: int):
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetContactIDs":
        hash = Int.read(data)
        return GetContactIDs(hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class GetStatuses(TL):
    ID = 0xc4a353ee

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetStatuses":
        
        return GetStatuses()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetContacts(TL):
    ID = 0xc023849f

    def __init__(cls, hash: int):
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetContacts":
        hash = Int.read(data)
        return GetContacts(hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class ImportContacts(TL):
    ID = 0x2c800be5

    def __init__(cls, contacts: List[TL]):
        cls.contacts = contacts

    @staticmethod
    def read(data) -> "ImportContacts":
        contacts = data.getobj()
        return ImportContacts(contacts=contacts)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.contacts))
        return data.getvalue()


class DeleteContacts(TL):
    ID = 0x96a0e00

    def __init__(cls, id: List[TL]):
        cls.id = id

    @staticmethod
    def read(data) -> "DeleteContacts":
        id = data.getobj()
        return DeleteContacts(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.id))
        return data.getvalue()


class DeleteByPhones(TL):
    ID = 0x1013fd9e

    def __init__(cls, phones: List[str]):
        cls.phones = phones

    @staticmethod
    def read(data) -> "DeleteByPhones":
        phones = data.getobj(String)
        return DeleteByPhones(phones=phones)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.phones, String))
        return data.getvalue()


class Block(TL):
    ID = 0x68cc1411

    def __init__(cls, id: TL):
        cls.id = id

    @staticmethod
    def read(data) -> "Block":
        id = data.getobj()
        return Block(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.id.getvalue())
        return data.getvalue()


class Unblock(TL):
    ID = 0xbea65d50

    def __init__(cls, id: TL):
        cls.id = id

    @staticmethod
    def read(data) -> "Unblock":
        id = data.getobj()
        return Unblock(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.id.getvalue())
        return data.getvalue()


class GetBlocked(TL):
    ID = 0xf57c350f

    def __init__(cls, offset: int, limit: int):
        cls.offset = offset
        cls.limit = limit

    @staticmethod
    def read(data) -> "GetBlocked":
        offset = Int.read(data)
        limit = Int.read(data)
        return GetBlocked(offset=offset, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()


class Search(TL):
    ID = 0x11f812d8

    def __init__(cls, q: str, limit: int):
        cls.q = q
        cls.limit = limit

    @staticmethod
    def read(data) -> "Search":
        q = String.read(data)
        limit = Int.read(data)
        return Search(q=q, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.q))
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()


class ResolveUsername(TL):
    ID = 0xf93ccba3

    def __init__(cls, username: str):
        cls.username = username

    @staticmethod
    def read(data) -> "ResolveUsername":
        username = String.read(data)
        return ResolveUsername(username=username)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.username))
        return data.getvalue()


class GetTopPeers(TL):
    ID = 0xd4982db5

    def __init__(cls, offset: int, limit: int, hash: int, correspondents: bool = None, bots_pm: bool = None, bots_inline: bool = None, phone_calls: bool = None, forward_users: bool = None, forward_chats: bool = None, groups: bool = None, channels: bool = None):
        cls.correspondents = correspondents
        cls.bots_pm = bots_pm
        cls.bots_inline = bots_inline
        cls.phone_calls = phone_calls
        cls.forward_users = forward_users
        cls.forward_chats = forward_chats
        cls.groups = groups
        cls.channels = channels
        cls.offset = offset
        cls.limit = limit
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetTopPeers":
        flags = Int.read(data)
        correspondents = True if flags & 1 else False
        bots_pm = True if flags & 2 else False
        bots_inline = True if flags & 4 else False
        phone_calls = True if flags & 8 else False
        forward_users = True if flags & 16 else False
        forward_chats = True if flags & 32 else False
        groups = True if flags & 1024 else False
        channels = True if flags & 32768 else False
        offset = Int.read(data)
        limit = Int.read(data)
        hash = Int.read(data)
        return GetTopPeers(correspondents=correspondents, bots_pm=bots_pm, bots_inline=bots_inline, phone_calls=phone_calls, forward_users=forward_users, forward_chats=forward_chats, groups=groups, channels=channels, offset=offset, limit=limit, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.correspondents is not None else 0
        flags |= 2 if cls.bots_pm is not None else 0
        flags |= 4 if cls.bots_inline is not None else 0
        flags |= 8 if cls.phone_calls is not None else 0
        flags |= 16 if cls.forward_users is not None else 0
        flags |= 32 if cls.forward_chats is not None else 0
        flags |= 1024 if cls.groups is not None else 0
        flags |= 32768 if cls.channels is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.limit))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class ResetTopPeerRating(TL):
    ID = 0x1ae373ac

    def __init__(cls, category: TL, peer: TL):
        cls.category = category
        cls.peer = peer

    @staticmethod
    def read(data) -> "ResetTopPeerRating":
        category = data.getobj()
        peer = data.getobj()
        return ResetTopPeerRating(category=category, peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.category.getvalue())
        data.write(cls.peer.getvalue())
        return data.getvalue()


class ResetSaved(TL):
    ID = 0x879537f1

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ResetSaved":
        
        return ResetSaved()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetSaved(TL):
    ID = 0x82f1e39f

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetSaved":
        
        return GetSaved()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ToggleTopPeers(TL):
    ID = 0x8514bdda

    def __init__(cls, enabled: bool):
        cls.enabled = enabled

    @staticmethod
    def read(data) -> "ToggleTopPeers":
        enabled = Bool.read(data)
        return ToggleTopPeers(enabled=enabled)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bool.getvalue(cls.enabled))
        return data.getvalue()


class AddContact(TL):
    ID = 0xe8f463d0

    def __init__(cls, id: TL, first_name: str, last_name: str, phone: str, add_phone_privacy_exception: bool = None):
        cls.add_phone_privacy_exception = add_phone_privacy_exception
        cls.id = id
        cls.first_name = first_name
        cls.last_name = last_name
        cls.phone = phone

    @staticmethod
    def read(data) -> "AddContact":
        flags = Int.read(data)
        add_phone_privacy_exception = True if flags & 1 else False
        id = data.getobj()
        first_name = String.read(data)
        last_name = String.read(data)
        phone = String.read(data)
        return AddContact(add_phone_privacy_exception=add_phone_privacy_exception, id=id, first_name=first_name, last_name=last_name, phone=phone)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.add_phone_privacy_exception is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.id.getvalue())
        data.write(String.getvalue(cls.first_name))
        data.write(String.getvalue(cls.last_name))
        data.write(String.getvalue(cls.phone))
        return data.getvalue()


class AcceptContact(TL):
    ID = 0xf831a20f

    def __init__(cls, id: TL):
        cls.id = id

    @staticmethod
    def read(data) -> "AcceptContact":
        id = data.getobj()
        return AcceptContact(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.id.getvalue())
        return data.getvalue()


class GetLocated(TL):
    ID = 0xd348bc44

    def __init__(cls, geo_point: TL, background: bool = None, self_expires: int = None):
        cls.background = background
        cls.geo_point = geo_point
        cls.self_expires = self_expires

    @staticmethod
    def read(data) -> "GetLocated":
        flags = Int.read(data)
        background = True if flags & 2 else False
        geo_point = data.getobj()
        self_expires = Int.read(data) if flags & 1 else None
        return GetLocated(background=background, geo_point=geo_point, self_expires=self_expires)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.background is not None else 0
        flags |= 1 if cls.self_expires is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.geo_point.getvalue())
        
        if cls.self_expires is not None:
            data.write(Int.getvalue(cls.self_expires))
        return data.getvalue()


class BlockFromReplies(TL):
    ID = 0x29a8962c

    def __init__(cls, msg_id: int, delete_message: bool = None, delete_history: bool = None, report_spam: bool = None):
        cls.delete_message = delete_message
        cls.delete_history = delete_history
        cls.report_spam = report_spam
        cls.msg_id = msg_id

    @staticmethod
    def read(data) -> "BlockFromReplies":
        flags = Int.read(data)
        delete_message = True if flags & 1 else False
        delete_history = True if flags & 2 else False
        report_spam = True if flags & 4 else False
        msg_id = Int.read(data)
        return BlockFromReplies(delete_message=delete_message, delete_history=delete_history, report_spam=report_spam, msg_id=msg_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.delete_message is not None else 0
        flags |= 2 if cls.delete_history is not None else 0
        flags |= 4 if cls.report_spam is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.msg_id))
        return data.getvalue()
