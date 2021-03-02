from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class GetMessages(TL):
    ID = 0x63c66506

    def __init__(cls, id: List[TL]):
        cls.id = id

    @staticmethod
    def read(data) -> "GetMessages":
        id = data.getobj()
        return GetMessages(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.id))
        return data.getvalue()


class GetDialogs(TL):
    ID = 0xa0ee3b73

    def __init__(cls, offset_date: int, offset_id: int, offset_peer: TL, limit: int, hash: int, exclude_pinned: bool = None, folder_id: int = None):
        cls.exclude_pinned = exclude_pinned
        cls.folder_id = folder_id
        cls.offset_date = offset_date
        cls.offset_id = offset_id
        cls.offset_peer = offset_peer
        cls.limit = limit
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetDialogs":
        flags = Int.read(data)
        exclude_pinned = True if flags & 1 else False
        folder_id = Int.read(data) if flags & 2 else None
        offset_date = Int.read(data)
        offset_id = Int.read(data)
        offset_peer = data.getobj()
        limit = Int.read(data)
        hash = Int.read(data)
        return GetDialogs(exclude_pinned=exclude_pinned, folder_id=folder_id, offset_date=offset_date, offset_id=offset_id, offset_peer=offset_peer, limit=limit, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.exclude_pinned is not None else 0
        flags |= 2 if cls.folder_id is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.folder_id is not None:
            data.write(Int.getvalue(cls.folder_id))
        data.write(Int.getvalue(cls.offset_date))
        data.write(Int.getvalue(cls.offset_id))
        data.write(cls.offset_peer.getvalue())
        data.write(Int.getvalue(cls.limit))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class GetHistory(TL):
    ID = 0xdcbb8260

    def __init__(cls, peer: TL, offset_id: int, offset_date: int, add_offset: int, limit: int, max_id: int, min_id: int, hash: int):
        cls.peer = peer
        cls.offset_id = offset_id
        cls.offset_date = offset_date
        cls.add_offset = add_offset
        cls.limit = limit
        cls.max_id = max_id
        cls.min_id = min_id
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetHistory":
        peer = data.getobj()
        offset_id = Int.read(data)
        offset_date = Int.read(data)
        add_offset = Int.read(data)
        limit = Int.read(data)
        max_id = Int.read(data)
        min_id = Int.read(data)
        hash = Int.read(data)
        return GetHistory(peer=peer, offset_id=offset_id, offset_date=offset_date, add_offset=add_offset, limit=limit, max_id=max_id, min_id=min_id, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.offset_id))
        data.write(Int.getvalue(cls.offset_date))
        data.write(Int.getvalue(cls.add_offset))
        data.write(Int.getvalue(cls.limit))
        data.write(Int.getvalue(cls.max_id))
        data.write(Int.getvalue(cls.min_id))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class Search(TL):
    ID = 0xc352eec

    def __init__(cls, peer: TL, q: str, filter: TL, min_date: int, max_date: int, offset_id: int, add_offset: int, limit: int, max_id: int, min_id: int, hash: int, from_id: TL = None, top_msg_id: int = None):
        cls.peer = peer
        cls.q = q
        cls.from_id = from_id
        cls.top_msg_id = top_msg_id
        cls.filter = filter
        cls.min_date = min_date
        cls.max_date = max_date
        cls.offset_id = offset_id
        cls.add_offset = add_offset
        cls.limit = limit
        cls.max_id = max_id
        cls.min_id = min_id
        cls.hash = hash

    @staticmethod
    def read(data) -> "Search":
        flags = Int.read(data)
        peer = data.getobj()
        q = String.read(data)
        from_id = data.getobj() if flags & 1 else None
        top_msg_id = Int.read(data) if flags & 2 else None
        filter = data.getobj()
        min_date = Int.read(data)
        max_date = Int.read(data)
        offset_id = Int.read(data)
        add_offset = Int.read(data)
        limit = Int.read(data)
        max_id = Int.read(data)
        min_id = Int.read(data)
        hash = Int.read(data)
        return Search(peer=peer, q=q, from_id=from_id, top_msg_id=top_msg_id, filter=filter, min_date=min_date, max_date=max_date, offset_id=offset_id, add_offset=add_offset, limit=limit, max_id=max_id, min_id=min_id, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.from_id is not None else 0
        flags |= 2 if cls.top_msg_id is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(String.getvalue(cls.q))
        
        if cls.from_id is not None:
            data.write(cls.from_id.getvalue())
        
        if cls.top_msg_id is not None:
            data.write(Int.getvalue(cls.top_msg_id))
        data.write(cls.filter.getvalue())
        data.write(Int.getvalue(cls.min_date))
        data.write(Int.getvalue(cls.max_date))
        data.write(Int.getvalue(cls.offset_id))
        data.write(Int.getvalue(cls.add_offset))
        data.write(Int.getvalue(cls.limit))
        data.write(Int.getvalue(cls.max_id))
        data.write(Int.getvalue(cls.min_id))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class ReadHistory(TL):
    ID = 0xe306d3a

    def __init__(cls, peer: TL, max_id: int):
        cls.peer = peer
        cls.max_id = max_id

    @staticmethod
    def read(data) -> "ReadHistory":
        peer = data.getobj()
        max_id = Int.read(data)
        return ReadHistory(peer=peer, max_id=max_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.max_id))
        return data.getvalue()


class DeleteHistory(TL):
    ID = 0x1c015b09

    def __init__(cls, peer: TL, max_id: int, just_clear: bool = None, revoke: bool = None):
        cls.just_clear = just_clear
        cls.revoke = revoke
        cls.peer = peer
        cls.max_id = max_id

    @staticmethod
    def read(data) -> "DeleteHistory":
        flags = Int.read(data)
        just_clear = True if flags & 1 else False
        revoke = True if flags & 2 else False
        peer = data.getobj()
        max_id = Int.read(data)
        return DeleteHistory(just_clear=just_clear, revoke=revoke, peer=peer, max_id=max_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.just_clear is not None else 0
        flags |= 2 if cls.revoke is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.max_id))
        return data.getvalue()


class DeleteMessages(TL):
    ID = 0xe58e95d2

    def __init__(cls, id: List[int], revoke: bool = None):
        cls.revoke = revoke
        cls.id = id

    @staticmethod
    def read(data) -> "DeleteMessages":
        flags = Int.read(data)
        revoke = True if flags & 1 else False
        id = data.getobj(Int)
        return DeleteMessages(revoke=revoke, id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.revoke is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Vector().getvalue(cls.id, Int))
        return data.getvalue()


class ReceivedMessages(TL):
    ID = 0x5a954c0

    def __init__(cls, max_id: int):
        cls.max_id = max_id

    @staticmethod
    def read(data) -> "ReceivedMessages":
        max_id = Int.read(data)
        return ReceivedMessages(max_id=max_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.max_id))
        return data.getvalue()


class SetTyping(TL):
    ID = 0x58943ee2

    def __init__(cls, peer: TL, action: TL, top_msg_id: int = None):
        cls.peer = peer
        cls.top_msg_id = top_msg_id
        cls.action = action

    @staticmethod
    def read(data) -> "SetTyping":
        flags = Int.read(data)
        peer = data.getobj()
        top_msg_id = Int.read(data) if flags & 1 else None
        action = data.getobj()
        return SetTyping(peer=peer, top_msg_id=top_msg_id, action=action)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.top_msg_id is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        
        if cls.top_msg_id is not None:
            data.write(Int.getvalue(cls.top_msg_id))
        data.write(cls.action.getvalue())
        return data.getvalue()


class SendMessage(TL):
    ID = 0x520c3870

    def __init__(cls, peer: TL, message: str, random_id: int, no_webpage: bool = None, silent: bool = None, background: bool = None, clear_draft: bool = None, reply_to_msg_id: int = None, reply_markup: TL = None, entities: List[TL] = None, schedule_date: int = None):
        cls.no_webpage = no_webpage
        cls.silent = silent
        cls.background = background
        cls.clear_draft = clear_draft
        cls.peer = peer
        cls.reply_to_msg_id = reply_to_msg_id
        cls.message = message
        cls.random_id = random_id
        cls.reply_markup = reply_markup
        cls.entities = entities
        cls.schedule_date = schedule_date

    @staticmethod
    def read(data) -> "SendMessage":
        flags = Int.read(data)
        no_webpage = True if flags & 2 else False
        silent = True if flags & 32 else False
        background = True if flags & 64 else False
        clear_draft = True if flags & 128 else False
        peer = data.getobj()
        reply_to_msg_id = Int.read(data) if flags & 1 else None
        message = String.read(data)
        random_id = Long.read(data)
        reply_markup = data.getobj() if flags & 4 else None
        entities = data.getobj() if flags & 8 else []
        schedule_date = Int.read(data) if flags & 1024 else None
        return SendMessage(no_webpage=no_webpage, silent=silent, background=background, clear_draft=clear_draft, peer=peer, reply_to_msg_id=reply_to_msg_id, message=message, random_id=random_id, reply_markup=reply_markup, entities=entities, schedule_date=schedule_date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.no_webpage is not None else 0
        flags |= 32 if cls.silent is not None else 0
        flags |= 64 if cls.background is not None else 0
        flags |= 128 if cls.clear_draft is not None else 0
        flags |= 1 if cls.reply_to_msg_id is not None else 0
        flags |= 4 if cls.reply_markup is not None else 0
        flags |= 8 if cls.entities is not None else 0
        flags |= 1024 if cls.schedule_date is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        
        if cls.reply_to_msg_id is not None:
            data.write(Int.getvalue(cls.reply_to_msg_id))
        data.write(String.getvalue(cls.message))
        data.write(Long.getvalue(cls.random_id))
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        
        if cls.schedule_date is not None:
            data.write(Int.getvalue(cls.schedule_date))
        return data.getvalue()


class SendMedia(TL):
    ID = 0x3491eba9

    def __init__(cls, peer: TL, media: TL, message: str, random_id: int, silent: bool = None, background: bool = None, clear_draft: bool = None, reply_to_msg_id: int = None, reply_markup: TL = None, entities: List[TL] = None, schedule_date: int = None):
        cls.silent = silent
        cls.background = background
        cls.clear_draft = clear_draft
        cls.peer = peer
        cls.reply_to_msg_id = reply_to_msg_id
        cls.media = media
        cls.message = message
        cls.random_id = random_id
        cls.reply_markup = reply_markup
        cls.entities = entities
        cls.schedule_date = schedule_date

    @staticmethod
    def read(data) -> "SendMedia":
        flags = Int.read(data)
        silent = True if flags & 32 else False
        background = True if flags & 64 else False
        clear_draft = True if flags & 128 else False
        peer = data.getobj()
        reply_to_msg_id = Int.read(data) if flags & 1 else None
        media = data.getobj()
        message = String.read(data)
        random_id = Long.read(data)
        reply_markup = data.getobj() if flags & 4 else None
        entities = data.getobj() if flags & 8 else []
        schedule_date = Int.read(data) if flags & 1024 else None
        return SendMedia(silent=silent, background=background, clear_draft=clear_draft, peer=peer, reply_to_msg_id=reply_to_msg_id, media=media, message=message, random_id=random_id, reply_markup=reply_markup, entities=entities, schedule_date=schedule_date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 32 if cls.silent is not None else 0
        flags |= 64 if cls.background is not None else 0
        flags |= 128 if cls.clear_draft is not None else 0
        flags |= 1 if cls.reply_to_msg_id is not None else 0
        flags |= 4 if cls.reply_markup is not None else 0
        flags |= 8 if cls.entities is not None else 0
        flags |= 1024 if cls.schedule_date is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        
        if cls.reply_to_msg_id is not None:
            data.write(Int.getvalue(cls.reply_to_msg_id))
        data.write(cls.media.getvalue())
        data.write(String.getvalue(cls.message))
        data.write(Long.getvalue(cls.random_id))
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        
        if cls.schedule_date is not None:
            data.write(Int.getvalue(cls.schedule_date))
        return data.getvalue()


class ForwardMessages(TL):
    ID = 0xd9fee60e

    def __init__(cls, from_peer: TL, id: List[int], random_id: List[int], to_peer: TL, silent: bool = None, background: bool = None, with_my_score: bool = None, schedule_date: int = None):
        cls.silent = silent
        cls.background = background
        cls.with_my_score = with_my_score
        cls.from_peer = from_peer
        cls.id = id
        cls.random_id = random_id
        cls.to_peer = to_peer
        cls.schedule_date = schedule_date

    @staticmethod
    def read(data) -> "ForwardMessages":
        flags = Int.read(data)
        silent = True if flags & 32 else False
        background = True if flags & 64 else False
        with_my_score = True if flags & 256 else False
        from_peer = data.getobj()
        id = data.getobj(Int)
        random_id = data.getobj(Long)
        to_peer = data.getobj()
        schedule_date = Int.read(data) if flags & 1024 else None
        return ForwardMessages(silent=silent, background=background, with_my_score=with_my_score, from_peer=from_peer, id=id, random_id=random_id, to_peer=to_peer, schedule_date=schedule_date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 32 if cls.silent is not None else 0
        flags |= 64 if cls.background is not None else 0
        flags |= 256 if cls.with_my_score is not None else 0
        flags |= 1024 if cls.schedule_date is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.from_peer.getvalue())
        data.write(Vector().getvalue(cls.id, Int))
        data.write(Vector().getvalue(cls.random_id, Long))
        data.write(cls.to_peer.getvalue())
        
        if cls.schedule_date is not None:
            data.write(Int.getvalue(cls.schedule_date))
        return data.getvalue()


class ReportSpam(TL):
    ID = 0xcf1592db

    def __init__(cls, peer: TL):
        cls.peer = peer

    @staticmethod
    def read(data) -> "ReportSpam":
        peer = data.getobj()
        return ReportSpam(peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class GetPeerSettings(TL):
    ID = 0x3672e09c

    def __init__(cls, peer: TL):
        cls.peer = peer

    @staticmethod
    def read(data) -> "GetPeerSettings":
        peer = data.getobj()
        return GetPeerSettings(peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class Report(TL):
    ID = 0x8953ab4e

    def __init__(cls, peer: TL, id: List[int], reason: TL, message: str):
        cls.peer = peer
        cls.id = id
        cls.reason = reason
        cls.message = message

    @staticmethod
    def read(data) -> "Report":
        peer = data.getobj()
        id = data.getobj(Int)
        reason = data.getobj()
        message = String.read(data)
        return Report(peer=peer, id=id, reason=reason, message=message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Vector().getvalue(cls.id, Int))
        data.write(cls.reason.getvalue())
        data.write(String.getvalue(cls.message))
        return data.getvalue()


class GetChats(TL):
    ID = 0x3c6aa187

    def __init__(cls, id: List[int]):
        cls.id = id

    @staticmethod
    def read(data) -> "GetChats":
        id = data.getobj(Int)
        return GetChats(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.id, Int))
        return data.getvalue()


class GetFullChat(TL):
    ID = 0x3b831c66

    def __init__(cls, chat_id: int):
        cls.chat_id = chat_id

    @staticmethod
    def read(data) -> "GetFullChat":
        chat_id = Int.read(data)
        return GetFullChat(chat_id=chat_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        return data.getvalue()


class EditChatTitle(TL):
    ID = 0xdc452855

    def __init__(cls, chat_id: int, title: str):
        cls.chat_id = chat_id
        cls.title = title

    @staticmethod
    def read(data) -> "EditChatTitle":
        chat_id = Int.read(data)
        title = String.read(data)
        return EditChatTitle(chat_id=chat_id, title=title)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        data.write(String.getvalue(cls.title))
        return data.getvalue()


class EditChatPhoto(TL):
    ID = 0xca4c79d8

    def __init__(cls, chat_id: int, photo: TL):
        cls.chat_id = chat_id
        cls.photo = photo

    @staticmethod
    def read(data) -> "EditChatPhoto":
        chat_id = Int.read(data)
        photo = data.getobj()
        return EditChatPhoto(chat_id=chat_id, photo=photo)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        data.write(cls.photo.getvalue())
        return data.getvalue()


class AddChatUser(TL):
    ID = 0xf9a0aa09

    def __init__(cls, chat_id: int, user_id: TL, fwd_limit: int):
        cls.chat_id = chat_id
        cls.user_id = user_id
        cls.fwd_limit = fwd_limit

    @staticmethod
    def read(data) -> "AddChatUser":
        chat_id = Int.read(data)
        user_id = data.getobj()
        fwd_limit = Int.read(data)
        return AddChatUser(chat_id=chat_id, user_id=user_id, fwd_limit=fwd_limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        data.write(cls.user_id.getvalue())
        data.write(Int.getvalue(cls.fwd_limit))
        return data.getvalue()


class DeleteChatUser(TL):
    ID = 0xc534459a

    def __init__(cls, chat_id: int, user_id: TL, revoke_history: bool = None):
        cls.revoke_history = revoke_history
        cls.chat_id = chat_id
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "DeleteChatUser":
        flags = Int.read(data)
        revoke_history = True if flags & 1 else False
        chat_id = Int.read(data)
        user_id = data.getobj()
        return DeleteChatUser(revoke_history=revoke_history, chat_id=chat_id, user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.revoke_history is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.chat_id))
        data.write(cls.user_id.getvalue())
        return data.getvalue()


class CreateChat(TL):
    ID = 0x9cb126e

    def __init__(cls, users: List[TL], title: str):
        cls.users = users
        cls.title = title

    @staticmethod
    def read(data) -> "CreateChat":
        users = data.getobj()
        title = String.read(data)
        return CreateChat(users=users, title=title)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.users))
        data.write(String.getvalue(cls.title))
        return data.getvalue()


class GetDhConfig(TL):
    ID = 0x26cf8950

    def __init__(cls, version: int, random_length: int):
        cls.version = version
        cls.random_length = random_length

    @staticmethod
    def read(data) -> "GetDhConfig":
        version = Int.read(data)
        random_length = Int.read(data)
        return GetDhConfig(version=version, random_length=random_length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.version))
        data.write(Int.getvalue(cls.random_length))
        return data.getvalue()


class RequestEncryption(TL):
    ID = 0xf64daf43

    def __init__(cls, user_id: TL, random_id: int, g_a: bytes):
        cls.user_id = user_id
        cls.random_id = random_id
        cls.g_a = g_a

    @staticmethod
    def read(data) -> "RequestEncryption":
        user_id = data.getobj()
        random_id = Int.read(data)
        g_a = Bytes.read(data)
        return RequestEncryption(user_id=user_id, random_id=random_id, g_a=g_a)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.user_id.getvalue())
        data.write(Int.getvalue(cls.random_id))
        data.write(Bytes.getvalue(cls.g_a))
        return data.getvalue()


class AcceptEncryption(TL):
    ID = 0x3dbc0415

    def __init__(cls, peer: TL, g_b: bytes, key_fingerprint: int):
        cls.peer = peer
        cls.g_b = g_b
        cls.key_fingerprint = key_fingerprint

    @staticmethod
    def read(data) -> "AcceptEncryption":
        peer = data.getobj()
        g_b = Bytes.read(data)
        key_fingerprint = Long.read(data)
        return AcceptEncryption(peer=peer, g_b=g_b, key_fingerprint=key_fingerprint)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Bytes.getvalue(cls.g_b))
        data.write(Long.getvalue(cls.key_fingerprint))
        return data.getvalue()


class DiscardEncryption(TL):
    ID = 0xf393aea0

    def __init__(cls, chat_id: int, delete_history: bool = None):
        cls.delete_history = delete_history
        cls.chat_id = chat_id

    @staticmethod
    def read(data) -> "DiscardEncryption":
        flags = Int.read(data)
        delete_history = True if flags & 1 else False
        chat_id = Int.read(data)
        return DiscardEncryption(delete_history=delete_history, chat_id=chat_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.delete_history is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.chat_id))
        return data.getvalue()


class SetEncryptedTyping(TL):
    ID = 0x791451ed

    def __init__(cls, peer: TL, typing: bool):
        cls.peer = peer
        cls.typing = typing

    @staticmethod
    def read(data) -> "SetEncryptedTyping":
        peer = data.getobj()
        typing = Bool.read(data)
        return SetEncryptedTyping(peer=peer, typing=typing)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Bool.getvalue(cls.typing))
        return data.getvalue()


class ReadEncryptedHistory(TL):
    ID = 0x7f4b690a

    def __init__(cls, peer: TL, max_date: int):
        cls.peer = peer
        cls.max_date = max_date

    @staticmethod
    def read(data) -> "ReadEncryptedHistory":
        peer = data.getobj()
        max_date = Int.read(data)
        return ReadEncryptedHistory(peer=peer, max_date=max_date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.max_date))
        return data.getvalue()


class SendEncrypted(TL):
    ID = 0x44fa7a15

    def __init__(cls, peer: TL, random_id: int, data: bytes, silent: bool = None):
        cls.silent = silent
        cls.peer = peer
        cls.random_id = random_id
        cls.data = data

    @staticmethod
    def read(data) -> "SendEncrypted":
        flags = Int.read(data)
        silent = True if flags & 1 else False
        peer = data.getobj()
        random_id = Long.read(data)
        data = Bytes.read(data)
        return SendEncrypted(silent=silent, peer=peer, random_id=random_id, data=data)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.silent is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(Long.getvalue(cls.random_id))
        data.write(Bytes.getvalue(cls.data))
        return data.getvalue()


class SendEncryptedFile(TL):
    ID = 0x5559481d

    def __init__(cls, peer: TL, random_id: int, data: bytes, file: TL, silent: bool = None):
        cls.silent = silent
        cls.peer = peer
        cls.random_id = random_id
        cls.data = data
        cls.file = file

    @staticmethod
    def read(data) -> "SendEncryptedFile":
        flags = Int.read(data)
        silent = True if flags & 1 else False
        peer = data.getobj()
        random_id = Long.read(data)
        data = Bytes.read(data)
        file = data.getobj()
        return SendEncryptedFile(silent=silent, peer=peer, random_id=random_id, data=data, file=file)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.silent is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(Long.getvalue(cls.random_id))
        data.write(Bytes.getvalue(cls.data))
        data.write(cls.file.getvalue())
        return data.getvalue()


class SendEncryptedService(TL):
    ID = 0x32d439a4

    def __init__(cls, peer: TL, random_id: int, data: bytes):
        cls.peer = peer
        cls.random_id = random_id
        cls.data = data

    @staticmethod
    def read(data) -> "SendEncryptedService":
        peer = data.getobj()
        random_id = Long.read(data)
        data = Bytes.read(data)
        return SendEncryptedService(peer=peer, random_id=random_id, data=data)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Long.getvalue(cls.random_id))
        data.write(Bytes.getvalue(cls.data))
        return data.getvalue()


class ReceivedQueue(TL):
    ID = 0x55a5bb66

    def __init__(cls, max_qts: int):
        cls.max_qts = max_qts

    @staticmethod
    def read(data) -> "ReceivedQueue":
        max_qts = Int.read(data)
        return ReceivedQueue(max_qts=max_qts)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.max_qts))
        return data.getvalue()


class ReportEncryptedSpam(TL):
    ID = 0x4b0c8c0f

    def __init__(cls, peer: TL):
        cls.peer = peer

    @staticmethod
    def read(data) -> "ReportEncryptedSpam":
        peer = data.getobj()
        return ReportEncryptedSpam(peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class ReadMessageContents(TL):
    ID = 0x36a73f77

    def __init__(cls, id: List[int]):
        cls.id = id

    @staticmethod
    def read(data) -> "ReadMessageContents":
        id = data.getobj(Int)
        return ReadMessageContents(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.id, Int))
        return data.getvalue()


class GetStickers(TL):
    ID = 0x43d4f2c

    def __init__(cls, emoticon: str, hash: int):
        cls.emoticon = emoticon
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetStickers":
        emoticon = String.read(data)
        hash = Int.read(data)
        return GetStickers(emoticon=emoticon, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.emoticon))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class GetAllStickers(TL):
    ID = 0x1c9618b1

    def __init__(cls, hash: int):
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetAllStickers":
        hash = Int.read(data)
        return GetAllStickers(hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class GetWebPagePreview(TL):
    ID = 0x8b68b0cc

    def __init__(cls, message: str, entities: List[TL] = None):
        cls.message = message
        cls.entities = entities

    @staticmethod
    def read(data) -> "GetWebPagePreview":
        flags = Int.read(data)
        message = String.read(data)
        entities = data.getobj() if flags & 8 else []
        return GetWebPagePreview(message=message, entities=entities)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 8 if cls.entities is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.message))
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        return data.getvalue()


class ExportChatInvite(TL):
    ID = 0x14b9bcd7

    def __init__(cls, peer: TL, legacy_revoke_permanent: bool = None, expire_date: int = None, usage_limit: int = None):
        cls.legacy_revoke_permanent = legacy_revoke_permanent
        cls.peer = peer
        cls.expire_date = expire_date
        cls.usage_limit = usage_limit

    @staticmethod
    def read(data) -> "ExportChatInvite":
        flags = Int.read(data)
        legacy_revoke_permanent = True if flags & 4 else False
        peer = data.getobj()
        expire_date = Int.read(data) if flags & 1 else None
        usage_limit = Int.read(data) if flags & 2 else None
        return ExportChatInvite(legacy_revoke_permanent=legacy_revoke_permanent, peer=peer, expire_date=expire_date, usage_limit=usage_limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 4 if cls.legacy_revoke_permanent is not None else 0
        flags |= 1 if cls.expire_date is not None else 0
        flags |= 2 if cls.usage_limit is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        
        if cls.expire_date is not None:
            data.write(Int.getvalue(cls.expire_date))
        
        if cls.usage_limit is not None:
            data.write(Int.getvalue(cls.usage_limit))
        return data.getvalue()


class CheckChatInvite(TL):
    ID = 0x3eadb1bb

    def __init__(cls, hash: str):
        cls.hash = hash

    @staticmethod
    def read(data) -> "CheckChatInvite":
        hash = String.read(data)
        return CheckChatInvite(hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.hash))
        return data.getvalue()


class ImportChatInvite(TL):
    ID = 0x6c50051c

    def __init__(cls, hash: str):
        cls.hash = hash

    @staticmethod
    def read(data) -> "ImportChatInvite":
        hash = String.read(data)
        return ImportChatInvite(hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.hash))
        return data.getvalue()


class GetStickerSet(TL):
    ID = 0x2619a90e

    def __init__(cls, stickerset: TL):
        cls.stickerset = stickerset

    @staticmethod
    def read(data) -> "GetStickerSet":
        stickerset = data.getobj()
        return GetStickerSet(stickerset=stickerset)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.stickerset.getvalue())
        return data.getvalue()


class InstallStickerSet(TL):
    ID = 0xc78fe460

    def __init__(cls, stickerset: TL, archived: bool):
        cls.stickerset = stickerset
        cls.archived = archived

    @staticmethod
    def read(data) -> "InstallStickerSet":
        stickerset = data.getobj()
        archived = Bool.read(data)
        return InstallStickerSet(stickerset=stickerset, archived=archived)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.stickerset.getvalue())
        data.write(Bool.getvalue(cls.archived))
        return data.getvalue()


class UninstallStickerSet(TL):
    ID = 0xf96e55de

    def __init__(cls, stickerset: TL):
        cls.stickerset = stickerset

    @staticmethod
    def read(data) -> "UninstallStickerSet":
        stickerset = data.getobj()
        return UninstallStickerSet(stickerset=stickerset)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.stickerset.getvalue())
        return data.getvalue()


class StartBot(TL):
    ID = 0xe6df7378

    def __init__(cls, bot: TL, peer: TL, random_id: int, start_param: str):
        cls.bot = bot
        cls.peer = peer
        cls.random_id = random_id
        cls.start_param = start_param

    @staticmethod
    def read(data) -> "StartBot":
        bot = data.getobj()
        peer = data.getobj()
        random_id = Long.read(data)
        start_param = String.read(data)
        return StartBot(bot=bot, peer=peer, random_id=random_id, start_param=start_param)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.bot.getvalue())
        data.write(cls.peer.getvalue())
        data.write(Long.getvalue(cls.random_id))
        data.write(String.getvalue(cls.start_param))
        return data.getvalue()


class GetMessagesViews(TL):
    ID = 0x5784d3e1

    def __init__(cls, peer: TL, id: List[int], increment: bool):
        cls.peer = peer
        cls.id = id
        cls.increment = increment

    @staticmethod
    def read(data) -> "GetMessagesViews":
        peer = data.getobj()
        id = data.getobj(Int)
        increment = Bool.read(data)
        return GetMessagesViews(peer=peer, id=id, increment=increment)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Vector().getvalue(cls.id, Int))
        data.write(Bool.getvalue(cls.increment))
        return data.getvalue()


class EditChatAdmin(TL):
    ID = 0xa9e69f2e

    def __init__(cls, chat_id: int, user_id: TL, is_admin: bool):
        cls.chat_id = chat_id
        cls.user_id = user_id
        cls.is_admin = is_admin

    @staticmethod
    def read(data) -> "EditChatAdmin":
        chat_id = Int.read(data)
        user_id = data.getobj()
        is_admin = Bool.read(data)
        return EditChatAdmin(chat_id=chat_id, user_id=user_id, is_admin=is_admin)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        data.write(cls.user_id.getvalue())
        data.write(Bool.getvalue(cls.is_admin))
        return data.getvalue()


class MigrateChat(TL):
    ID = 0x15a3b8e3

    def __init__(cls, chat_id: int):
        cls.chat_id = chat_id

    @staticmethod
    def read(data) -> "MigrateChat":
        chat_id = Int.read(data)
        return MigrateChat(chat_id=chat_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        return data.getvalue()


class SearchGlobal(TL):
    ID = 0x4bc6589a

    def __init__(cls, q: str, filter: TL, min_date: int, max_date: int, offset_rate: int, offset_peer: TL, offset_id: int, limit: int, folder_id: int = None):
        cls.folder_id = folder_id
        cls.q = q
        cls.filter = filter
        cls.min_date = min_date
        cls.max_date = max_date
        cls.offset_rate = offset_rate
        cls.offset_peer = offset_peer
        cls.offset_id = offset_id
        cls.limit = limit

    @staticmethod
    def read(data) -> "SearchGlobal":
        flags = Int.read(data)
        folder_id = Int.read(data) if flags & 1 else None
        q = String.read(data)
        filter = data.getobj()
        min_date = Int.read(data)
        max_date = Int.read(data)
        offset_rate = Int.read(data)
        offset_peer = data.getobj()
        offset_id = Int.read(data)
        limit = Int.read(data)
        return SearchGlobal(folder_id=folder_id, q=q, filter=filter, min_date=min_date, max_date=max_date, offset_rate=offset_rate, offset_peer=offset_peer, offset_id=offset_id, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.folder_id is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.folder_id is not None:
            data.write(Int.getvalue(cls.folder_id))
        data.write(String.getvalue(cls.q))
        data.write(cls.filter.getvalue())
        data.write(Int.getvalue(cls.min_date))
        data.write(Int.getvalue(cls.max_date))
        data.write(Int.getvalue(cls.offset_rate))
        data.write(cls.offset_peer.getvalue())
        data.write(Int.getvalue(cls.offset_id))
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()


class ReorderStickerSets(TL):
    ID = 0x78337739

    def __init__(cls, order: List[int], masks: bool = None):
        cls.masks = masks
        cls.order = order

    @staticmethod
    def read(data) -> "ReorderStickerSets":
        flags = Int.read(data)
        masks = True if flags & 1 else False
        order = data.getobj(Long)
        return ReorderStickerSets(masks=masks, order=order)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.masks is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Vector().getvalue(cls.order, Long))
        return data.getvalue()


class GetDocumentByHash(TL):
    ID = 0x338e2464

    def __init__(cls, sha256: bytes, size: int, mime_type: str):
        cls.sha256 = sha256
        cls.size = size
        cls.mime_type = mime_type

    @staticmethod
    def read(data) -> "GetDocumentByHash":
        sha256 = Bytes.read(data)
        size = Int.read(data)
        mime_type = String.read(data)
        return GetDocumentByHash(sha256=sha256, size=size, mime_type=mime_type)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.sha256))
        data.write(Int.getvalue(cls.size))
        data.write(String.getvalue(cls.mime_type))
        return data.getvalue()


class GetSavedGifs(TL):
    ID = 0x83bf3d52

    def __init__(cls, hash: int):
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetSavedGifs":
        hash = Int.read(data)
        return GetSavedGifs(hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class SaveGif(TL):
    ID = 0x327a30cb

    def __init__(cls, id: TL, unsave: bool):
        cls.id = id
        cls.unsave = unsave

    @staticmethod
    def read(data) -> "SaveGif":
        id = data.getobj()
        unsave = Bool.read(data)
        return SaveGif(id=id, unsave=unsave)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.id.getvalue())
        data.write(Bool.getvalue(cls.unsave))
        return data.getvalue()


class GetInlineBotResults(TL):
    ID = 0x514e999d

    def __init__(cls, bot: TL, peer: TL, query: str, offset: str, geo_point: TL = None):
        cls.bot = bot
        cls.peer = peer
        cls.geo_point = geo_point
        cls.query = query
        cls.offset = offset

    @staticmethod
    def read(data) -> "GetInlineBotResults":
        flags = Int.read(data)
        bot = data.getobj()
        peer = data.getobj()
        geo_point = data.getobj() if flags & 1 else None
        query = String.read(data)
        offset = String.read(data)
        return GetInlineBotResults(bot=bot, peer=peer, geo_point=geo_point, query=query, offset=offset)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.geo_point is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.bot.getvalue())
        data.write(cls.peer.getvalue())
        
        if cls.geo_point is not None:
            data.write(cls.geo_point.getvalue())
        data.write(String.getvalue(cls.query))
        data.write(String.getvalue(cls.offset))
        return data.getvalue()


class SetInlineBotResults(TL):
    ID = 0xeb5ea206

    def __init__(cls, query_id: int, results: List[TL], cache_time: int, gallery: bool = None, private: bool = None, next_offset: str = None, switch_pm: TL = None):
        cls.gallery = gallery
        cls.private = private
        cls.query_id = query_id
        cls.results = results
        cls.cache_time = cache_time
        cls.next_offset = next_offset
        cls.switch_pm = switch_pm

    @staticmethod
    def read(data) -> "SetInlineBotResults":
        flags = Int.read(data)
        gallery = True if flags & 1 else False
        private = True if flags & 2 else False
        query_id = Long.read(data)
        results = data.getobj()
        cache_time = Int.read(data)
        next_offset = String.read(data) if flags & 4 else None
        switch_pm = data.getobj() if flags & 8 else None
        return SetInlineBotResults(gallery=gallery, private=private, query_id=query_id, results=results, cache_time=cache_time, next_offset=next_offset, switch_pm=switch_pm)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.gallery is not None else 0
        flags |= 2 if cls.private is not None else 0
        flags |= 4 if cls.next_offset is not None else 0
        flags |= 8 if cls.switch_pm is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.query_id))
        data.write(Vector().getvalue(cls.results))
        data.write(Int.getvalue(cls.cache_time))
        
        if cls.next_offset is not None:
            data.write(String.getvalue(cls.next_offset))
        
        if cls.switch_pm is not None:
            data.write(cls.switch_pm.getvalue())
        return data.getvalue()


class SendInlineBotResult(TL):
    ID = 0x220815b0

    def __init__(cls, peer: TL, random_id: int, query_id: int, id: str, silent: bool = None, background: bool = None, clear_draft: bool = None, hide_via: bool = None, reply_to_msg_id: int = None, schedule_date: int = None):
        cls.silent = silent
        cls.background = background
        cls.clear_draft = clear_draft
        cls.hide_via = hide_via
        cls.peer = peer
        cls.reply_to_msg_id = reply_to_msg_id
        cls.random_id = random_id
        cls.query_id = query_id
        cls.id = id
        cls.schedule_date = schedule_date

    @staticmethod
    def read(data) -> "SendInlineBotResult":
        flags = Int.read(data)
        silent = True if flags & 32 else False
        background = True if flags & 64 else False
        clear_draft = True if flags & 128 else False
        hide_via = True if flags & 2048 else False
        peer = data.getobj()
        reply_to_msg_id = Int.read(data) if flags & 1 else None
        random_id = Long.read(data)
        query_id = Long.read(data)
        id = String.read(data)
        schedule_date = Int.read(data) if flags & 1024 else None
        return SendInlineBotResult(silent=silent, background=background, clear_draft=clear_draft, hide_via=hide_via, peer=peer, reply_to_msg_id=reply_to_msg_id, random_id=random_id, query_id=query_id, id=id, schedule_date=schedule_date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 32 if cls.silent is not None else 0
        flags |= 64 if cls.background is not None else 0
        flags |= 128 if cls.clear_draft is not None else 0
        flags |= 2048 if cls.hide_via is not None else 0
        flags |= 1 if cls.reply_to_msg_id is not None else 0
        flags |= 1024 if cls.schedule_date is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        
        if cls.reply_to_msg_id is not None:
            data.write(Int.getvalue(cls.reply_to_msg_id))
        data.write(Long.getvalue(cls.random_id))
        data.write(Long.getvalue(cls.query_id))
        data.write(String.getvalue(cls.id))
        
        if cls.schedule_date is not None:
            data.write(Int.getvalue(cls.schedule_date))
        return data.getvalue()


class GetMessageEditData(TL):
    ID = 0xfda68d36

    def __init__(cls, peer: TL, id: int):
        cls.peer = peer
        cls.id = id

    @staticmethod
    def read(data) -> "GetMessageEditData":
        peer = data.getobj()
        id = Int.read(data)
        return GetMessageEditData(peer=peer, id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.id))
        return data.getvalue()


class EditMessage(TL):
    ID = 0x48f71778

    def __init__(cls, peer: TL, id: int, no_webpage: bool = None, message: str = None, media: TL = None, reply_markup: TL = None, entities: List[TL] = None, schedule_date: int = None):
        cls.no_webpage = no_webpage
        cls.peer = peer
        cls.id = id
        cls.message = message
        cls.media = media
        cls.reply_markup = reply_markup
        cls.entities = entities
        cls.schedule_date = schedule_date

    @staticmethod
    def read(data) -> "EditMessage":
        flags = Int.read(data)
        no_webpage = True if flags & 2 else False
        peer = data.getobj()
        id = Int.read(data)
        message = String.read(data) if flags & 2048 else None
        media = data.getobj() if flags & 16384 else None
        reply_markup = data.getobj() if flags & 4 else None
        entities = data.getobj() if flags & 8 else []
        schedule_date = Int.read(data) if flags & 32768 else None
        return EditMessage(no_webpage=no_webpage, peer=peer, id=id, message=message, media=media, reply_markup=reply_markup, entities=entities, schedule_date=schedule_date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.no_webpage is not None else 0
        flags |= 2048 if cls.message is not None else 0
        flags |= 16384 if cls.media is not None else 0
        flags |= 4 if cls.reply_markup is not None else 0
        flags |= 8 if cls.entities is not None else 0
        flags |= 32768 if cls.schedule_date is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.id))
        
        if cls.message is not None:
            data.write(String.getvalue(cls.message))
        
        if cls.media is not None:
            data.write(cls.media.getvalue())
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        
        if cls.schedule_date is not None:
            data.write(Int.getvalue(cls.schedule_date))
        return data.getvalue()


class EditInlineBotMessage(TL):
    ID = 0x83557dba

    def __init__(cls, id: TL, no_webpage: bool = None, message: str = None, media: TL = None, reply_markup: TL = None, entities: List[TL] = None):
        cls.no_webpage = no_webpage
        cls.id = id
        cls.message = message
        cls.media = media
        cls.reply_markup = reply_markup
        cls.entities = entities

    @staticmethod
    def read(data) -> "EditInlineBotMessage":
        flags = Int.read(data)
        no_webpage = True if flags & 2 else False
        id = data.getobj()
        message = String.read(data) if flags & 2048 else None
        media = data.getobj() if flags & 16384 else None
        reply_markup = data.getobj() if flags & 4 else None
        entities = data.getobj() if flags & 8 else []
        return EditInlineBotMessage(no_webpage=no_webpage, id=id, message=message, media=media, reply_markup=reply_markup, entities=entities)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.no_webpage is not None else 0
        flags |= 2048 if cls.message is not None else 0
        flags |= 16384 if cls.media is not None else 0
        flags |= 4 if cls.reply_markup is not None else 0
        flags |= 8 if cls.entities is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.id.getvalue())
        
        if cls.message is not None:
            data.write(String.getvalue(cls.message))
        
        if cls.media is not None:
            data.write(cls.media.getvalue())
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        return data.getvalue()


class GetBotCallbackAnswer(TL):
    ID = 0x9342ca07

    def __init__(cls, peer: TL, msg_id: int, game: bool = None, data: bytes = None, password: TL = None):
        cls.game = game
        cls.peer = peer
        cls.msg_id = msg_id
        cls.data = data
        cls.password = password

    @staticmethod
    def read(data) -> "GetBotCallbackAnswer":
        flags = Int.read(data)
        game = True if flags & 2 else False
        peer = data.getobj()
        msg_id = Int.read(data)
        data = Bytes.read(data) if flags & 1 else None
        password = data.getobj() if flags & 4 else None
        return GetBotCallbackAnswer(game=game, peer=peer, msg_id=msg_id, data=data, password=password)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.game is not None else 0
        flags |= 1 if cls.data is not None else 0
        flags |= 4 if cls.password is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        
        if cls.data is not None:
            data.write(Bytes.getvalue(cls.data))
        
        if cls.password is not None:
            data.write(cls.password.getvalue())
        return data.getvalue()


class SetBotCallbackAnswer(TL):
    ID = 0xd58f130a

    def __init__(cls, query_id: int, cache_time: int, alert: bool = None, message: str = None, url: str = None):
        cls.alert = alert
        cls.query_id = query_id
        cls.message = message
        cls.url = url
        cls.cache_time = cache_time

    @staticmethod
    def read(data) -> "SetBotCallbackAnswer":
        flags = Int.read(data)
        alert = True if flags & 2 else False
        query_id = Long.read(data)
        message = String.read(data) if flags & 1 else None
        url = String.read(data) if flags & 4 else None
        cache_time = Int.read(data)
        return SetBotCallbackAnswer(alert=alert, query_id=query_id, message=message, url=url, cache_time=cache_time)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.alert is not None else 0
        flags |= 1 if cls.message is not None else 0
        flags |= 4 if cls.url is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.query_id))
        
        if cls.message is not None:
            data.write(String.getvalue(cls.message))
        
        if cls.url is not None:
            data.write(String.getvalue(cls.url))
        data.write(Int.getvalue(cls.cache_time))
        return data.getvalue()


class GetPeerDialogs(TL):
    ID = 0xe470bcfd

    def __init__(cls, peers: List[TL]):
        cls.peers = peers

    @staticmethod
    def read(data) -> "GetPeerDialogs":
        peers = data.getobj()
        return GetPeerDialogs(peers=peers)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.peers))
        return data.getvalue()


class SaveDraft(TL):
    ID = 0xbc39e14b

    def __init__(cls, peer: TL, message: str, no_webpage: bool = None, reply_to_msg_id: int = None, entities: List[TL] = None):
        cls.no_webpage = no_webpage
        cls.reply_to_msg_id = reply_to_msg_id
        cls.peer = peer
        cls.message = message
        cls.entities = entities

    @staticmethod
    def read(data) -> "SaveDraft":
        flags = Int.read(data)
        no_webpage = True if flags & 2 else False
        reply_to_msg_id = Int.read(data) if flags & 1 else None
        peer = data.getobj()
        message = String.read(data)
        entities = data.getobj() if flags & 8 else []
        return SaveDraft(no_webpage=no_webpage, reply_to_msg_id=reply_to_msg_id, peer=peer, message=message, entities=entities)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.no_webpage is not None else 0
        flags |= 1 if cls.reply_to_msg_id is not None else 0
        flags |= 8 if cls.entities is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.reply_to_msg_id is not None:
            data.write(Int.getvalue(cls.reply_to_msg_id))
        data.write(cls.peer.getvalue())
        data.write(String.getvalue(cls.message))
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        return data.getvalue()


class GetAllDrafts(TL):
    ID = 0x6a3f8d65

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetAllDrafts":
        
        return GetAllDrafts()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetFeaturedStickers(TL):
    ID = 0x2dacca4f

    def __init__(cls, hash: int):
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetFeaturedStickers":
        hash = Int.read(data)
        return GetFeaturedStickers(hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class ReadFeaturedStickers(TL):
    ID = 0x5b118126

    def __init__(cls, id: List[int]):
        cls.id = id

    @staticmethod
    def read(data) -> "ReadFeaturedStickers":
        id = data.getobj(Long)
        return ReadFeaturedStickers(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.id, Long))
        return data.getvalue()


class GetRecentStickers(TL):
    ID = 0x5ea192c9

    def __init__(cls, hash: int, attached: bool = None):
        cls.attached = attached
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetRecentStickers":
        flags = Int.read(data)
        attached = True if flags & 1 else False
        hash = Int.read(data)
        return GetRecentStickers(attached=attached, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.attached is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class SaveRecentSticker(TL):
    ID = 0x392718f8

    def __init__(cls, id: TL, unsave: bool, attached: bool = None):
        cls.attached = attached
        cls.id = id
        cls.unsave = unsave

    @staticmethod
    def read(data) -> "SaveRecentSticker":
        flags = Int.read(data)
        attached = True if flags & 1 else False
        id = data.getobj()
        unsave = Bool.read(data)
        return SaveRecentSticker(attached=attached, id=id, unsave=unsave)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.attached is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.id.getvalue())
        data.write(Bool.getvalue(cls.unsave))
        return data.getvalue()


class ClearRecentStickers(TL):
    ID = 0x8999602d

    def __init__(cls, attached: bool = None):
        cls.attached = attached

    @staticmethod
    def read(data) -> "ClearRecentStickers":
        flags = Int.read(data)
        attached = True if flags & 1 else False
        return ClearRecentStickers(attached=attached)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.attached is not None else 0
        data.write(Int.getvalue(flags))
        return data.getvalue()


class GetArchivedStickers(TL):
    ID = 0x57f17692

    def __init__(cls, offset_id: int, limit: int, masks: bool = None):
        cls.masks = masks
        cls.offset_id = offset_id
        cls.limit = limit

    @staticmethod
    def read(data) -> "GetArchivedStickers":
        flags = Int.read(data)
        masks = True if flags & 1 else False
        offset_id = Long.read(data)
        limit = Int.read(data)
        return GetArchivedStickers(masks=masks, offset_id=offset_id, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.masks is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.offset_id))
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()


class GetMaskStickers(TL):
    ID = 0x65b8c79f

    def __init__(cls, hash: int):
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetMaskStickers":
        hash = Int.read(data)
        return GetMaskStickers(hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class GetAttachedStickers(TL):
    ID = 0xcc5b67cc

    def __init__(cls, media: TL):
        cls.media = media

    @staticmethod
    def read(data) -> "GetAttachedStickers":
        media = data.getobj()
        return GetAttachedStickers(media=media)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.media.getvalue())
        return data.getvalue()


class SetGameScore(TL):
    ID = 0x8ef8ecc0

    def __init__(cls, peer: TL, id: int, user_id: TL, score: int, edit_message: bool = None, force: bool = None):
        cls.edit_message = edit_message
        cls.force = force
        cls.peer = peer
        cls.id = id
        cls.user_id = user_id
        cls.score = score

    @staticmethod
    def read(data) -> "SetGameScore":
        flags = Int.read(data)
        edit_message = True if flags & 1 else False
        force = True if flags & 2 else False
        peer = data.getobj()
        id = Int.read(data)
        user_id = data.getobj()
        score = Int.read(data)
        return SetGameScore(edit_message=edit_message, force=force, peer=peer, id=id, user_id=user_id, score=score)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.edit_message is not None else 0
        flags |= 2 if cls.force is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.id))
        data.write(cls.user_id.getvalue())
        data.write(Int.getvalue(cls.score))
        return data.getvalue()


class SetInlineGameScore(TL):
    ID = 0x15ad9f64

    def __init__(cls, id: TL, user_id: TL, score: int, edit_message: bool = None, force: bool = None):
        cls.edit_message = edit_message
        cls.force = force
        cls.id = id
        cls.user_id = user_id
        cls.score = score

    @staticmethod
    def read(data) -> "SetInlineGameScore":
        flags = Int.read(data)
        edit_message = True if flags & 1 else False
        force = True if flags & 2 else False
        id = data.getobj()
        user_id = data.getobj()
        score = Int.read(data)
        return SetInlineGameScore(edit_message=edit_message, force=force, id=id, user_id=user_id, score=score)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.edit_message is not None else 0
        flags |= 2 if cls.force is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.id.getvalue())
        data.write(cls.user_id.getvalue())
        data.write(Int.getvalue(cls.score))
        return data.getvalue()


class GetGameHighScores(TL):
    ID = 0xe822649d

    def __init__(cls, peer: TL, id: int, user_id: TL):
        cls.peer = peer
        cls.id = id
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "GetGameHighScores":
        peer = data.getobj()
        id = Int.read(data)
        user_id = data.getobj()
        return GetGameHighScores(peer=peer, id=id, user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.id))
        data.write(cls.user_id.getvalue())
        return data.getvalue()


class GetInlineGameHighScores(TL):
    ID = 0xf635e1b

    def __init__(cls, id: TL, user_id: TL):
        cls.id = id
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "GetInlineGameHighScores":
        id = data.getobj()
        user_id = data.getobj()
        return GetInlineGameHighScores(id=id, user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.id.getvalue())
        data.write(cls.user_id.getvalue())
        return data.getvalue()


class GetCommonChats(TL):
    ID = 0xd0a48c4

    def __init__(cls, user_id: TL, max_id: int, limit: int):
        cls.user_id = user_id
        cls.max_id = max_id
        cls.limit = limit

    @staticmethod
    def read(data) -> "GetCommonChats":
        user_id = data.getobj()
        max_id = Int.read(data)
        limit = Int.read(data)
        return GetCommonChats(user_id=user_id, max_id=max_id, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.user_id.getvalue())
        data.write(Int.getvalue(cls.max_id))
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()


class GetAllChats(TL):
    ID = 0xeba80ff0

    def __init__(cls, except_ids: List[int]):
        cls.except_ids = except_ids

    @staticmethod
    def read(data) -> "GetAllChats":
        except_ids = data.getobj(Int)
        return GetAllChats(except_ids=except_ids)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.except_ids, Int))
        return data.getvalue()


class GetWebPage(TL):
    ID = 0x32ca8f91

    def __init__(cls, url: str, hash: int):
        cls.url = url
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetWebPage":
        url = String.read(data)
        hash = Int.read(data)
        return GetWebPage(url=url, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class ToggleDialogPin(TL):
    ID = 0xa731e257

    def __init__(cls, peer: TL, pinned: bool = None):
        cls.pinned = pinned
        cls.peer = peer

    @staticmethod
    def read(data) -> "ToggleDialogPin":
        flags = Int.read(data)
        pinned = True if flags & 1 else False
        peer = data.getobj()
        return ToggleDialogPin(pinned=pinned, peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.pinned is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class ReorderPinnedDialogs(TL):
    ID = 0x3b1adf37

    def __init__(cls, folder_id: int, order: List[TL], force: bool = None):
        cls.force = force
        cls.folder_id = folder_id
        cls.order = order

    @staticmethod
    def read(data) -> "ReorderPinnedDialogs":
        flags = Int.read(data)
        force = True if flags & 1 else False
        folder_id = Int.read(data)
        order = data.getobj()
        return ReorderPinnedDialogs(force=force, folder_id=folder_id, order=order)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.force is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.folder_id))
        data.write(Vector().getvalue(cls.order))
        return data.getvalue()


class GetPinnedDialogs(TL):
    ID = 0xd6b94df2

    def __init__(cls, folder_id: int):
        cls.folder_id = folder_id

    @staticmethod
    def read(data) -> "GetPinnedDialogs":
        folder_id = Int.read(data)
        return GetPinnedDialogs(folder_id=folder_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.folder_id))
        return data.getvalue()


class SetBotShippingResults(TL):
    ID = 0xe5f672fa

    def __init__(cls, query_id: int, error: str = None, shipping_options: List[TL] = None):
        cls.query_id = query_id
        cls.error = error
        cls.shipping_options = shipping_options

    @staticmethod
    def read(data) -> "SetBotShippingResults":
        flags = Int.read(data)
        query_id = Long.read(data)
        error = String.read(data) if flags & 1 else None
        shipping_options = data.getobj() if flags & 2 else []
        return SetBotShippingResults(query_id=query_id, error=error, shipping_options=shipping_options)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.error is not None else 0
        flags |= 2 if cls.shipping_options is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.query_id))
        
        if cls.error is not None:
            data.write(String.getvalue(cls.error))
        
        if cls.shipping_options is not None:
            data.write(Vector().getvalue(cls.shipping_options))
        return data.getvalue()


class SetBotPrecheckoutResults(TL):
    ID = 0x9c2dd95

    def __init__(cls, query_id: int, success: bool = None, error: str = None):
        cls.success = success
        cls.query_id = query_id
        cls.error = error

    @staticmethod
    def read(data) -> "SetBotPrecheckoutResults":
        flags = Int.read(data)
        success = True if flags & 2 else False
        query_id = Long.read(data)
        error = String.read(data) if flags & 1 else None
        return SetBotPrecheckoutResults(success=success, query_id=query_id, error=error)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.success is not None else 0
        flags |= 1 if cls.error is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.query_id))
        
        if cls.error is not None:
            data.write(String.getvalue(cls.error))
        return data.getvalue()


class UploadMedia(TL):
    ID = 0x519bc2b1

    def __init__(cls, peer: TL, media: TL):
        cls.peer = peer
        cls.media = media

    @staticmethod
    def read(data) -> "UploadMedia":
        peer = data.getobj()
        media = data.getobj()
        return UploadMedia(peer=peer, media=media)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(cls.media.getvalue())
        return data.getvalue()


class SendScreenshotNotification(TL):
    ID = 0xc97df020

    def __init__(cls, peer: TL, reply_to_msg_id: int, random_id: int):
        cls.peer = peer
        cls.reply_to_msg_id = reply_to_msg_id
        cls.random_id = random_id

    @staticmethod
    def read(data) -> "SendScreenshotNotification":
        peer = data.getobj()
        reply_to_msg_id = Int.read(data)
        random_id = Long.read(data)
        return SendScreenshotNotification(peer=peer, reply_to_msg_id=reply_to_msg_id, random_id=random_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.reply_to_msg_id))
        data.write(Long.getvalue(cls.random_id))
        return data.getvalue()


class GetFavedStickers(TL):
    ID = 0x21ce0b0e

    def __init__(cls, hash: int):
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetFavedStickers":
        hash = Int.read(data)
        return GetFavedStickers(hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class FaveSticker(TL):
    ID = 0xb9ffc55b

    def __init__(cls, id: TL, unfave: bool):
        cls.id = id
        cls.unfave = unfave

    @staticmethod
    def read(data) -> "FaveSticker":
        id = data.getobj()
        unfave = Bool.read(data)
        return FaveSticker(id=id, unfave=unfave)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.id.getvalue())
        data.write(Bool.getvalue(cls.unfave))
        return data.getvalue()


class GetUnreadMentions(TL):
    ID = 0x46578472

    def __init__(cls, peer: TL, offset_id: int, add_offset: int, limit: int, max_id: int, min_id: int):
        cls.peer = peer
        cls.offset_id = offset_id
        cls.add_offset = add_offset
        cls.limit = limit
        cls.max_id = max_id
        cls.min_id = min_id

    @staticmethod
    def read(data) -> "GetUnreadMentions":
        peer = data.getobj()
        offset_id = Int.read(data)
        add_offset = Int.read(data)
        limit = Int.read(data)
        max_id = Int.read(data)
        min_id = Int.read(data)
        return GetUnreadMentions(peer=peer, offset_id=offset_id, add_offset=add_offset, limit=limit, max_id=max_id, min_id=min_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.offset_id))
        data.write(Int.getvalue(cls.add_offset))
        data.write(Int.getvalue(cls.limit))
        data.write(Int.getvalue(cls.max_id))
        data.write(Int.getvalue(cls.min_id))
        return data.getvalue()


class ReadMentions(TL):
    ID = 0xf0189d3

    def __init__(cls, peer: TL):
        cls.peer = peer

    @staticmethod
    def read(data) -> "ReadMentions":
        peer = data.getobj()
        return ReadMentions(peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class GetRecentLocations(TL):
    ID = 0xbbc45b09

    def __init__(cls, peer: TL, limit: int, hash: int):
        cls.peer = peer
        cls.limit = limit
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetRecentLocations":
        peer = data.getobj()
        limit = Int.read(data)
        hash = Int.read(data)
        return GetRecentLocations(peer=peer, limit=limit, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.limit))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class SendMultiMedia(TL):
    ID = 0xcc0110cb

    def __init__(cls, peer: TL, multi_media: List[TL], silent: bool = None, background: bool = None, clear_draft: bool = None, reply_to_msg_id: int = None, schedule_date: int = None):
        cls.silent = silent
        cls.background = background
        cls.clear_draft = clear_draft
        cls.peer = peer
        cls.reply_to_msg_id = reply_to_msg_id
        cls.multi_media = multi_media
        cls.schedule_date = schedule_date

    @staticmethod
    def read(data) -> "SendMultiMedia":
        flags = Int.read(data)
        silent = True if flags & 32 else False
        background = True if flags & 64 else False
        clear_draft = True if flags & 128 else False
        peer = data.getobj()
        reply_to_msg_id = Int.read(data) if flags & 1 else None
        multi_media = data.getobj()
        schedule_date = Int.read(data) if flags & 1024 else None
        return SendMultiMedia(silent=silent, background=background, clear_draft=clear_draft, peer=peer, reply_to_msg_id=reply_to_msg_id, multi_media=multi_media, schedule_date=schedule_date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 32 if cls.silent is not None else 0
        flags |= 64 if cls.background is not None else 0
        flags |= 128 if cls.clear_draft is not None else 0
        flags |= 1 if cls.reply_to_msg_id is not None else 0
        flags |= 1024 if cls.schedule_date is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        
        if cls.reply_to_msg_id is not None:
            data.write(Int.getvalue(cls.reply_to_msg_id))
        data.write(Vector().getvalue(cls.multi_media))
        
        if cls.schedule_date is not None:
            data.write(Int.getvalue(cls.schedule_date))
        return data.getvalue()


class UploadEncryptedFile(TL):
    ID = 0x5057c497

    def __init__(cls, peer: TL, file: TL):
        cls.peer = peer
        cls.file = file

    @staticmethod
    def read(data) -> "UploadEncryptedFile":
        peer = data.getobj()
        file = data.getobj()
        return UploadEncryptedFile(peer=peer, file=file)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(cls.file.getvalue())
        return data.getvalue()


class SearchStickerSets(TL):
    ID = 0xc2b7d08b

    def __init__(cls, q: str, hash: int, exclude_featured: bool = None):
        cls.exclude_featured = exclude_featured
        cls.q = q
        cls.hash = hash

    @staticmethod
    def read(data) -> "SearchStickerSets":
        flags = Int.read(data)
        exclude_featured = True if flags & 1 else False
        q = String.read(data)
        hash = Int.read(data)
        return SearchStickerSets(exclude_featured=exclude_featured, q=q, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.exclude_featured is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.q))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class GetSplitRanges(TL):
    ID = 0x1cff7e08

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetSplitRanges":
        
        return GetSplitRanges()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class MarkDialogUnread(TL):
    ID = 0xc286d98f

    def __init__(cls, peer: TL, unread: bool = None):
        cls.unread = unread
        cls.peer = peer

    @staticmethod
    def read(data) -> "MarkDialogUnread":
        flags = Int.read(data)
        unread = True if flags & 1 else False
        peer = data.getobj()
        return MarkDialogUnread(unread=unread, peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.unread is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class GetDialogUnreadMarks(TL):
    ID = 0x22e24e22

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetDialogUnreadMarks":
        
        return GetDialogUnreadMarks()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ClearAllDrafts(TL):
    ID = 0x7e58ee9c

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ClearAllDrafts":
        
        return ClearAllDrafts()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UpdatePinnedMessage(TL):
    ID = 0xd2aaf7ec

    def __init__(cls, peer: TL, id: int, silent: bool = None, unpin: bool = None, pm_oneside: bool = None):
        cls.silent = silent
        cls.unpin = unpin
        cls.pm_oneside = pm_oneside
        cls.peer = peer
        cls.id = id

    @staticmethod
    def read(data) -> "UpdatePinnedMessage":
        flags = Int.read(data)
        silent = True if flags & 1 else False
        unpin = True if flags & 2 else False
        pm_oneside = True if flags & 4 else False
        peer = data.getobj()
        id = Int.read(data)
        return UpdatePinnedMessage(silent=silent, unpin=unpin, pm_oneside=pm_oneside, peer=peer, id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.silent is not None else 0
        flags |= 2 if cls.unpin is not None else 0
        flags |= 4 if cls.pm_oneside is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.id))
        return data.getvalue()


class SendVote(TL):
    ID = 0x10ea6184

    def __init__(cls, peer: TL, msg_id: int, options: List[bytes]):
        cls.peer = peer
        cls.msg_id = msg_id
        cls.options = options

    @staticmethod
    def read(data) -> "SendVote":
        peer = data.getobj()
        msg_id = Int.read(data)
        options = data.getobj(Bytes)
        return SendVote(peer=peer, msg_id=msg_id, options=options)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        data.write(Vector().getvalue(cls.options, Bytes))
        return data.getvalue()


class GetPollResults(TL):
    ID = 0x73bb643b

    def __init__(cls, peer: TL, msg_id: int):
        cls.peer = peer
        cls.msg_id = msg_id

    @staticmethod
    def read(data) -> "GetPollResults":
        peer = data.getobj()
        msg_id = Int.read(data)
        return GetPollResults(peer=peer, msg_id=msg_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        return data.getvalue()


class GetOnlines(TL):
    ID = 0x6e2be050

    def __init__(cls, peer: TL):
        cls.peer = peer

    @staticmethod
    def read(data) -> "GetOnlines":
        peer = data.getobj()
        return GetOnlines(peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class GetStatsURL(TL):
    ID = 0x812c2ae6

    def __init__(cls, peer: TL, params: str, dark: bool = None):
        cls.dark = dark
        cls.peer = peer
        cls.params = params

    @staticmethod
    def read(data) -> "GetStatsURL":
        flags = Int.read(data)
        dark = True if flags & 1 else False
        peer = data.getobj()
        params = String.read(data)
        return GetStatsURL(dark=dark, peer=peer, params=params)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.dark is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(String.getvalue(cls.params))
        return data.getvalue()


class EditChatAbout(TL):
    ID = 0xdef60797

    def __init__(cls, peer: TL, about: str):
        cls.peer = peer
        cls.about = about

    @staticmethod
    def read(data) -> "EditChatAbout":
        peer = data.getobj()
        about = String.read(data)
        return EditChatAbout(peer=peer, about=about)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(String.getvalue(cls.about))
        return data.getvalue()


class EditChatDefaultBannedRights(TL):
    ID = 0xa5866b41

    def __init__(cls, peer: TL, banned_rights: TL):
        cls.peer = peer
        cls.banned_rights = banned_rights

    @staticmethod
    def read(data) -> "EditChatDefaultBannedRights":
        peer = data.getobj()
        banned_rights = data.getobj()
        return EditChatDefaultBannedRights(peer=peer, banned_rights=banned_rights)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(cls.banned_rights.getvalue())
        return data.getvalue()


class GetEmojiKeywords(TL):
    ID = 0x35a0e062

    def __init__(cls, lang_code: str):
        cls.lang_code = lang_code

    @staticmethod
    def read(data) -> "GetEmojiKeywords":
        lang_code = String.read(data)
        return GetEmojiKeywords(lang_code=lang_code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.lang_code))
        return data.getvalue()


class GetEmojiKeywordsDifference(TL):
    ID = 0x1508b6af

    def __init__(cls, lang_code: str, from_version: int):
        cls.lang_code = lang_code
        cls.from_version = from_version

    @staticmethod
    def read(data) -> "GetEmojiKeywordsDifference":
        lang_code = String.read(data)
        from_version = Int.read(data)
        return GetEmojiKeywordsDifference(lang_code=lang_code, from_version=from_version)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.lang_code))
        data.write(Int.getvalue(cls.from_version))
        return data.getvalue()


class GetEmojiKeywordsLanguages(TL):
    ID = 0x4e9963b2

    def __init__(cls, lang_codes: List[str]):
        cls.lang_codes = lang_codes

    @staticmethod
    def read(data) -> "GetEmojiKeywordsLanguages":
        lang_codes = data.getobj(String)
        return GetEmojiKeywordsLanguages(lang_codes=lang_codes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.lang_codes, String))
        return data.getvalue()


class GetEmojiURL(TL):
    ID = 0xd5b10c26

    def __init__(cls, lang_code: str):
        cls.lang_code = lang_code

    @staticmethod
    def read(data) -> "GetEmojiURL":
        lang_code = String.read(data)
        return GetEmojiURL(lang_code=lang_code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.lang_code))
        return data.getvalue()


class GetSearchCounters(TL):
    ID = 0x732eef00

    def __init__(cls, peer: TL, filters: List[TL]):
        cls.peer = peer
        cls.filters = filters

    @staticmethod
    def read(data) -> "GetSearchCounters":
        peer = data.getobj()
        filters = data.getobj()
        return GetSearchCounters(peer=peer, filters=filters)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Vector().getvalue(cls.filters))
        return data.getvalue()


class RequestUrlAuth(TL):
    ID = 0xe33f5613

    def __init__(cls, peer: TL, msg_id: int, button_id: int):
        cls.peer = peer
        cls.msg_id = msg_id
        cls.button_id = button_id

    @staticmethod
    def read(data) -> "RequestUrlAuth":
        peer = data.getobj()
        msg_id = Int.read(data)
        button_id = Int.read(data)
        return RequestUrlAuth(peer=peer, msg_id=msg_id, button_id=button_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        data.write(Int.getvalue(cls.button_id))
        return data.getvalue()


class AcceptUrlAuth(TL):
    ID = 0xf729ea98

    def __init__(cls, peer: TL, msg_id: int, button_id: int, write_allowed: bool = None):
        cls.write_allowed = write_allowed
        cls.peer = peer
        cls.msg_id = msg_id
        cls.button_id = button_id

    @staticmethod
    def read(data) -> "AcceptUrlAuth":
        flags = Int.read(data)
        write_allowed = True if flags & 1 else False
        peer = data.getobj()
        msg_id = Int.read(data)
        button_id = Int.read(data)
        return AcceptUrlAuth(write_allowed=write_allowed, peer=peer, msg_id=msg_id, button_id=button_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.write_allowed is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        data.write(Int.getvalue(cls.button_id))
        return data.getvalue()


class HidePeerSettingsBar(TL):
    ID = 0x4facb138

    def __init__(cls, peer: TL):
        cls.peer = peer

    @staticmethod
    def read(data) -> "HidePeerSettingsBar":
        peer = data.getobj()
        return HidePeerSettingsBar(peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class GetScheduledHistory(TL):
    ID = 0xe2c2685b

    def __init__(cls, peer: TL, hash: int):
        cls.peer = peer
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetScheduledHistory":
        peer = data.getobj()
        hash = Int.read(data)
        return GetScheduledHistory(peer=peer, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class GetScheduledMessages(TL):
    ID = 0xbdbb0464

    def __init__(cls, peer: TL, id: List[int]):
        cls.peer = peer
        cls.id = id

    @staticmethod
    def read(data) -> "GetScheduledMessages":
        peer = data.getobj()
        id = data.getobj(Int)
        return GetScheduledMessages(peer=peer, id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Vector().getvalue(cls.id, Int))
        return data.getvalue()


class SendScheduledMessages(TL):
    ID = 0xbd38850a

    def __init__(cls, peer: TL, id: List[int]):
        cls.peer = peer
        cls.id = id

    @staticmethod
    def read(data) -> "SendScheduledMessages":
        peer = data.getobj()
        id = data.getobj(Int)
        return SendScheduledMessages(peer=peer, id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Vector().getvalue(cls.id, Int))
        return data.getvalue()


class DeleteScheduledMessages(TL):
    ID = 0x59ae2b16

    def __init__(cls, peer: TL, id: List[int]):
        cls.peer = peer
        cls.id = id

    @staticmethod
    def read(data) -> "DeleteScheduledMessages":
        peer = data.getobj()
        id = data.getobj(Int)
        return DeleteScheduledMessages(peer=peer, id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Vector().getvalue(cls.id, Int))
        return data.getvalue()


class GetPollVotes(TL):
    ID = 0xb86e380e

    def __init__(cls, peer: TL, id: int, limit: int, option: bytes = None, offset: str = None):
        cls.peer = peer
        cls.id = id
        cls.option = option
        cls.offset = offset
        cls.limit = limit

    @staticmethod
    def read(data) -> "GetPollVotes":
        flags = Int.read(data)
        peer = data.getobj()
        id = Int.read(data)
        option = Bytes.read(data) if flags & 1 else None
        offset = String.read(data) if flags & 2 else None
        limit = Int.read(data)
        return GetPollVotes(peer=peer, id=id, option=option, offset=offset, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.option is not None else 0
        flags |= 2 if cls.offset is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.id))
        
        if cls.option is not None:
            data.write(Bytes.getvalue(cls.option))
        
        if cls.offset is not None:
            data.write(String.getvalue(cls.offset))
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()


class ToggleStickerSets(TL):
    ID = 0xb5052fea

    def __init__(cls, stickersets: List[TL], uninstall: bool = None, archive: bool = None, unarchive: bool = None):
        cls.uninstall = uninstall
        cls.archive = archive
        cls.unarchive = unarchive
        cls.stickersets = stickersets

    @staticmethod
    def read(data) -> "ToggleStickerSets":
        flags = Int.read(data)
        uninstall = True if flags & 1 else False
        archive = True if flags & 2 else False
        unarchive = True if flags & 4 else False
        stickersets = data.getobj()
        return ToggleStickerSets(uninstall=uninstall, archive=archive, unarchive=unarchive, stickersets=stickersets)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.uninstall is not None else 0
        flags |= 2 if cls.archive is not None else 0
        flags |= 4 if cls.unarchive is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Vector().getvalue(cls.stickersets))
        return data.getvalue()


class GetDialogFilters(TL):
    ID = 0xf19ed96d

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetDialogFilters":
        
        return GetDialogFilters()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GetSuggestedDialogFilters(TL):
    ID = 0xa29cd42c

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetSuggestedDialogFilters":
        
        return GetSuggestedDialogFilters()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UpdateDialogFilter(TL):
    ID = 0x1ad4a04a

    def __init__(cls, id: int, filter: TL = None):
        cls.id = id
        cls.filter = filter

    @staticmethod
    def read(data) -> "UpdateDialogFilter":
        flags = Int.read(data)
        id = Int.read(data)
        filter = data.getobj() if flags & 1 else None
        return UpdateDialogFilter(id=id, filter=filter)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.filter is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        
        if cls.filter is not None:
            data.write(cls.filter.getvalue())
        return data.getvalue()


class UpdateDialogFiltersOrder(TL):
    ID = 0xc563c1e4

    def __init__(cls, order: List[int]):
        cls.order = order

    @staticmethod
    def read(data) -> "UpdateDialogFiltersOrder":
        order = data.getobj(Int)
        return UpdateDialogFiltersOrder(order=order)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.order, Int))
        return data.getvalue()


class GetOldFeaturedStickers(TL):
    ID = 0x5fe7025b

    def __init__(cls, offset: int, limit: int, hash: int):
        cls.offset = offset
        cls.limit = limit
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetOldFeaturedStickers":
        offset = Int.read(data)
        limit = Int.read(data)
        hash = Int.read(data)
        return GetOldFeaturedStickers(offset=offset, limit=limit, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.limit))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class GetReplies(TL):
    ID = 0x24b581ba

    def __init__(cls, peer: TL, msg_id: int, offset_id: int, offset_date: int, add_offset: int, limit: int, max_id: int, min_id: int, hash: int):
        cls.peer = peer
        cls.msg_id = msg_id
        cls.offset_id = offset_id
        cls.offset_date = offset_date
        cls.add_offset = add_offset
        cls.limit = limit
        cls.max_id = max_id
        cls.min_id = min_id
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetReplies":
        peer = data.getobj()
        msg_id = Int.read(data)
        offset_id = Int.read(data)
        offset_date = Int.read(data)
        add_offset = Int.read(data)
        limit = Int.read(data)
        max_id = Int.read(data)
        min_id = Int.read(data)
        hash = Int.read(data)
        return GetReplies(peer=peer, msg_id=msg_id, offset_id=offset_id, offset_date=offset_date, add_offset=add_offset, limit=limit, max_id=max_id, min_id=min_id, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        data.write(Int.getvalue(cls.offset_id))
        data.write(Int.getvalue(cls.offset_date))
        data.write(Int.getvalue(cls.add_offset))
        data.write(Int.getvalue(cls.limit))
        data.write(Int.getvalue(cls.max_id))
        data.write(Int.getvalue(cls.min_id))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class GetDiscussionMessage(TL):
    ID = 0x446972fd

    def __init__(cls, peer: TL, msg_id: int):
        cls.peer = peer
        cls.msg_id = msg_id

    @staticmethod
    def read(data) -> "GetDiscussionMessage":
        peer = data.getobj()
        msg_id = Int.read(data)
        return GetDiscussionMessage(peer=peer, msg_id=msg_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        return data.getvalue()


class ReadDiscussion(TL):
    ID = 0xf731a9f4

    def __init__(cls, peer: TL, msg_id: int, read_max_id: int):
        cls.peer = peer
        cls.msg_id = msg_id
        cls.read_max_id = read_max_id

    @staticmethod
    def read(data) -> "ReadDiscussion":
        peer = data.getobj()
        msg_id = Int.read(data)
        read_max_id = Int.read(data)
        return ReadDiscussion(peer=peer, msg_id=msg_id, read_max_id=read_max_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        data.write(Int.getvalue(cls.read_max_id))
        return data.getvalue()


class UnpinAllMessages(TL):
    ID = 0xf025bc8b

    def __init__(cls, peer: TL):
        cls.peer = peer

    @staticmethod
    def read(data) -> "UnpinAllMessages":
        peer = data.getobj()
        return UnpinAllMessages(peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class DeleteChat(TL):
    ID = 0x83247d11

    def __init__(cls, chat_id: int):
        cls.chat_id = chat_id

    @staticmethod
    def read(data) -> "DeleteChat":
        chat_id = Int.read(data)
        return DeleteChat(chat_id=chat_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        return data.getvalue()


class DeletePhoneCallHistory(TL):
    ID = 0xf9cbe409

    def __init__(cls, revoke: bool = None):
        cls.revoke = revoke

    @staticmethod
    def read(data) -> "DeletePhoneCallHistory":
        flags = Int.read(data)
        revoke = True if flags & 1 else False
        return DeletePhoneCallHistory(revoke=revoke)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.revoke is not None else 0
        data.write(Int.getvalue(flags))
        return data.getvalue()


class CheckHistoryImport(TL):
    ID = 0x43fe19f3

    def __init__(cls, import_head: str):
        cls.import_head = import_head

    @staticmethod
    def read(data) -> "CheckHistoryImport":
        import_head = String.read(data)
        return CheckHistoryImport(import_head=import_head)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.import_head))
        return data.getvalue()


class InitHistoryImport(TL):
    ID = 0x34090c3b

    def __init__(cls, peer: TL, file: TL, media_count: int):
        cls.peer = peer
        cls.file = file
        cls.media_count = media_count

    @staticmethod
    def read(data) -> "InitHistoryImport":
        peer = data.getobj()
        file = data.getobj()
        media_count = Int.read(data)
        return InitHistoryImport(peer=peer, file=file, media_count=media_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(cls.file.getvalue())
        data.write(Int.getvalue(cls.media_count))
        return data.getvalue()


class UploadImportedMedia(TL):
    ID = 0x2a862092

    def __init__(cls, peer: TL, import_id: int, file_name: str, media: TL):
        cls.peer = peer
        cls.import_id = import_id
        cls.file_name = file_name
        cls.media = media

    @staticmethod
    def read(data) -> "UploadImportedMedia":
        peer = data.getobj()
        import_id = Long.read(data)
        file_name = String.read(data)
        media = data.getobj()
        return UploadImportedMedia(peer=peer, import_id=import_id, file_name=file_name, media=media)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Long.getvalue(cls.import_id))
        data.write(String.getvalue(cls.file_name))
        data.write(cls.media.getvalue())
        return data.getvalue()


class StartHistoryImport(TL):
    ID = 0xb43df344

    def __init__(cls, peer: TL, import_id: int):
        cls.peer = peer
        cls.import_id = import_id

    @staticmethod
    def read(data) -> "StartHistoryImport":
        peer = data.getobj()
        import_id = Long.read(data)
        return StartHistoryImport(peer=peer, import_id=import_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Long.getvalue(cls.import_id))
        return data.getvalue()


class GetExportedChatInvites(TL):
    ID = 0xa2b5a3f6

    def __init__(cls, peer: TL, admin_id: TL, limit: int, revoked: bool = None, offset_date: int = None, offset_link: str = None):
        cls.revoked = revoked
        cls.peer = peer
        cls.admin_id = admin_id
        cls.offset_date = offset_date
        cls.offset_link = offset_link
        cls.limit = limit

    @staticmethod
    def read(data) -> "GetExportedChatInvites":
        flags = Int.read(data)
        revoked = True if flags & 8 else False
        peer = data.getobj()
        admin_id = data.getobj()
        offset_date = Int.read(data) if flags & 4 else None
        offset_link = String.read(data) if flags & 4 else None
        limit = Int.read(data)
        return GetExportedChatInvites(revoked=revoked, peer=peer, admin_id=admin_id, offset_date=offset_date, offset_link=offset_link, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 8 if cls.revoked is not None else 0
        flags |= 4 if cls.offset_date is not None else 0
        flags |= 4 if cls.offset_link is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(cls.admin_id.getvalue())
        
        if cls.offset_date is not None:
            data.write(Int.getvalue(cls.offset_date))
        
        if cls.offset_link is not None:
            data.write(String.getvalue(cls.offset_link))
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()


class EditExportedChatInvite(TL):
    ID = 0x2e4ffbe

    def __init__(cls, peer: TL, link: str, revoked: bool = None, expire_date: int = None, usage_limit: int = None):
        cls.revoked = revoked
        cls.peer = peer
        cls.link = link
        cls.expire_date = expire_date
        cls.usage_limit = usage_limit

    @staticmethod
    def read(data) -> "EditExportedChatInvite":
        flags = Int.read(data)
        revoked = True if flags & 4 else False
        peer = data.getobj()
        link = String.read(data)
        expire_date = Int.read(data) if flags & 1 else None
        usage_limit = Int.read(data) if flags & 2 else None
        return EditExportedChatInvite(revoked=revoked, peer=peer, link=link, expire_date=expire_date, usage_limit=usage_limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 4 if cls.revoked is not None else 0
        flags |= 1 if cls.expire_date is not None else 0
        flags |= 2 if cls.usage_limit is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(String.getvalue(cls.link))
        
        if cls.expire_date is not None:
            data.write(Int.getvalue(cls.expire_date))
        
        if cls.usage_limit is not None:
            data.write(Int.getvalue(cls.usage_limit))
        return data.getvalue()


class DeleteRevokedExportedChatInvites(TL):
    ID = 0x56987bd5

    def __init__(cls, peer: TL, admin_id: TL):
        cls.peer = peer
        cls.admin_id = admin_id

    @staticmethod
    def read(data) -> "DeleteRevokedExportedChatInvites":
        peer = data.getobj()
        admin_id = data.getobj()
        return DeleteRevokedExportedChatInvites(peer=peer, admin_id=admin_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(cls.admin_id.getvalue())
        return data.getvalue()


class DeleteExportedChatInvite(TL):
    ID = 0xd464a42b

    def __init__(cls, peer: TL, link: str):
        cls.peer = peer
        cls.link = link

    @staticmethod
    def read(data) -> "DeleteExportedChatInvite":
        peer = data.getobj()
        link = String.read(data)
        return DeleteExportedChatInvite(peer=peer, link=link)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(String.getvalue(cls.link))
        return data.getvalue()


class GetAdminsWithInvites(TL):
    ID = 0x3920e6ef

    def __init__(cls, peer: TL):
        cls.peer = peer

    @staticmethod
    def read(data) -> "GetAdminsWithInvites":
        peer = data.getobj()
        return GetAdminsWithInvites(peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class GetChatInviteImporters(TL):
    ID = 0x26fb7289

    def __init__(cls, peer: TL, link: str, offset_date: int, offset_user: TL, limit: int):
        cls.peer = peer
        cls.link = link
        cls.offset_date = offset_date
        cls.offset_user = offset_user
        cls.limit = limit

    @staticmethod
    def read(data) -> "GetChatInviteImporters":
        peer = data.getobj()
        link = String.read(data)
        offset_date = Int.read(data)
        offset_user = data.getobj()
        limit = Int.read(data)
        return GetChatInviteImporters(peer=peer, link=link, offset_date=offset_date, offset_user=offset_user, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(String.getvalue(cls.link))
        data.write(Int.getvalue(cls.offset_date))
        data.write(cls.offset_user.getvalue())
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()


class SetHistoryTTL(TL):
    ID = 0xb80e5fe4

    def __init__(cls, peer: TL, period: int):
        cls.peer = peer
        cls.period = period

    @staticmethod
    def read(data) -> "SetHistoryTTL":
        peer = data.getobj()
        period = Int.read(data)
        return SetHistoryTTL(peer=peer, period=period)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.period))
        return data.getvalue()
