from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class Dialogs(TL):
    ID = 0x15ba6c40

    def __init__(cls, dialogs: List[TL], messages: List[TL], chats: List[TL], users: List[TL]):
        cls.dialogs = dialogs
        cls.messages = messages
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "Dialogs":
        dialogs = data.getobj()
        messages = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return Dialogs(dialogs=dialogs, messages=messages, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.dialogs))
        data.write(Vector().getvalue(cls.messages))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class DialogsSlice(TL):
    ID = 0x71e094f3

    def __init__(cls, count: int, dialogs: List[TL], messages: List[TL], chats: List[TL], users: List[TL]):
        cls.count = count
        cls.dialogs = dialogs
        cls.messages = messages
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "DialogsSlice":
        count = Int.read(data)
        dialogs = data.getobj()
        messages = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return DialogsSlice(count=count, dialogs=dialogs, messages=messages, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.count))
        data.write(Vector().getvalue(cls.dialogs))
        data.write(Vector().getvalue(cls.messages))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class DialogsNotModified(TL):
    ID = 0xf0e3e596

    def __init__(cls, count: int):
        cls.count = count

    @staticmethod
    def read(data) -> "DialogsNotModified":
        count = Int.read(data)
        return DialogsNotModified(count=count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.count))
        return data.getvalue()


class Messages(TL):
    ID = 0x8c718e87

    def __init__(cls, messages: List[TL], chats: List[TL], users: List[TL]):
        cls.messages = messages
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "Messages":
        messages = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return Messages(messages=messages, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.messages))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class MessagesSlice(TL):
    ID = 0x3a54685e

    def __init__(cls, count: int, messages: List[TL], chats: List[TL], users: List[TL], inexact: bool = None, next_rate: int = None, offset_id_offset: int = None):
        cls.inexact = inexact
        cls.count = count
        cls.next_rate = next_rate
        cls.offset_id_offset = offset_id_offset
        cls.messages = messages
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "MessagesSlice":
        flags = Int.read(data)
        inexact = True if flags & 2 else False
        count = Int.read(data)
        next_rate = Int.read(data) if flags & 1 else None
        offset_id_offset = Int.read(data) if flags & 4 else None
        messages = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return MessagesSlice(inexact=inexact, count=count, next_rate=next_rate, offset_id_offset=offset_id_offset, messages=messages, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.inexact is not None else 0
        flags |= 1 if cls.next_rate is not None else 0
        flags |= 4 if cls.offset_id_offset is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.count))
        
        if cls.next_rate is not None:
            data.write(Int.getvalue(cls.next_rate))
        
        if cls.offset_id_offset is not None:
            data.write(Int.getvalue(cls.offset_id_offset))
        data.write(Vector().getvalue(cls.messages))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class ChannelMessages(TL):
    ID = 0x64479808

    def __init__(cls, pts: int, count: int, messages: List[TL], chats: List[TL], users: List[TL], inexact: bool = None, offset_id_offset: int = None):
        cls.inexact = inexact
        cls.pts = pts
        cls.count = count
        cls.offset_id_offset = offset_id_offset
        cls.messages = messages
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "ChannelMessages":
        flags = Int.read(data)
        inexact = True if flags & 2 else False
        pts = Int.read(data)
        count = Int.read(data)
        offset_id_offset = Int.read(data) if flags & 4 else None
        messages = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return ChannelMessages(inexact=inexact, pts=pts, count=count, offset_id_offset=offset_id_offset, messages=messages, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.inexact is not None else 0
        flags |= 4 if cls.offset_id_offset is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.count))
        
        if cls.offset_id_offset is not None:
            data.write(Int.getvalue(cls.offset_id_offset))
        data.write(Vector().getvalue(cls.messages))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class MessagesNotModified(TL):
    ID = 0x74535f21

    def __init__(cls, count: int):
        cls.count = count

    @staticmethod
    def read(data) -> "MessagesNotModified":
        count = Int.read(data)
        return MessagesNotModified(count=count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.count))
        return data.getvalue()


class Chats(TL):
    ID = 0x64ff9fd5

    def __init__(cls, chats: List[TL]):
        cls.chats = chats

    @staticmethod
    def read(data) -> "Chats":
        chats = data.getobj()
        return Chats(chats=chats)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.chats))
        return data.getvalue()


class ChatsSlice(TL):
    ID = 0x9cd81144

    def __init__(cls, count: int, chats: List[TL]):
        cls.count = count
        cls.chats = chats

    @staticmethod
    def read(data) -> "ChatsSlice":
        count = Int.read(data)
        chats = data.getobj()
        return ChatsSlice(count=count, chats=chats)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.count))
        data.write(Vector().getvalue(cls.chats))
        return data.getvalue()


class ChatFull(TL):
    ID = 0xe5d7d19c

    def __init__(cls, full_chat: TL, chats: List[TL], users: List[TL]):
        cls.full_chat = full_chat
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "ChatFull":
        full_chat = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return ChatFull(full_chat=full_chat, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.full_chat.getvalue())
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class AffectedHistory(TL):
    ID = 0xb45c69d1

    def __init__(cls, pts: int, pts_count: int, offset: int):
        cls.pts = pts
        cls.pts_count = pts_count
        cls.offset = offset

    @staticmethod
    def read(data) -> "AffectedHistory":
        pts = Int.read(data)
        pts_count = Int.read(data)
        offset = Int.read(data)
        return AffectedHistory(pts=pts, pts_count=pts_count, offset=offset)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        data.write(Int.getvalue(cls.offset))
        return data.getvalue()


class DhConfigNotModified(TL):
    ID = 0xc0e24635

    def __init__(cls, random: bytes):
        cls.random = random

    @staticmethod
    def read(data) -> "DhConfigNotModified":
        random = Bytes.read(data)
        return DhConfigNotModified(random=random)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.random))
        return data.getvalue()


class DhConfig(TL):
    ID = 0x2c221edd

    def __init__(cls, g: int, p: bytes, version: int, random: bytes):
        cls.g = g
        cls.p = p
        cls.version = version
        cls.random = random

    @staticmethod
    def read(data) -> "DhConfig":
        g = Int.read(data)
        p = Bytes.read(data)
        version = Int.read(data)
        random = Bytes.read(data)
        return DhConfig(g=g, p=p, version=version, random=random)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.g))
        data.write(Bytes.getvalue(cls.p))
        data.write(Int.getvalue(cls.version))
        data.write(Bytes.getvalue(cls.random))
        return data.getvalue()


class SentEncryptedMessage(TL):
    ID = 0x560f8935

    def __init__(cls, date: int):
        cls.date = date

    @staticmethod
    def read(data) -> "SentEncryptedMessage":
        date = Int.read(data)
        return SentEncryptedMessage(date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class SentEncryptedFile(TL):
    ID = 0x9493ff32

    def __init__(cls, date: int, file: TL):
        cls.date = date
        cls.file = file

    @staticmethod
    def read(data) -> "SentEncryptedFile":
        date = Int.read(data)
        file = data.getobj()
        return SentEncryptedFile(date=date, file=file)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.date))
        data.write(cls.file.getvalue())
        return data.getvalue()


class StickersNotModified(TL):
    ID = 0xf1749a22

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "StickersNotModified":
        
        return StickersNotModified()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class Stickers(TL):
    ID = 0xe4599bbd

    def __init__(cls, hash: int, stickers: List[TL]):
        cls.hash = hash
        cls.stickers = stickers

    @staticmethod
    def read(data) -> "Stickers":
        hash = Int.read(data)
        stickers = data.getobj()
        return Stickers(hash=hash, stickers=stickers)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        data.write(Vector().getvalue(cls.stickers))
        return data.getvalue()


class AllStickersNotModified(TL):
    ID = 0xe86602c3

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "AllStickersNotModified":
        
        return AllStickersNotModified()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class AllStickers(TL):
    ID = 0xedfd405f

    def __init__(cls, hash: int, sets: List[TL]):
        cls.hash = hash
        cls.sets = sets

    @staticmethod
    def read(data) -> "AllStickers":
        hash = Int.read(data)
        sets = data.getobj()
        return AllStickers(hash=hash, sets=sets)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        data.write(Vector().getvalue(cls.sets))
        return data.getvalue()


class AffectedMessages(TL):
    ID = 0x84d19185

    def __init__(cls, pts: int, pts_count: int):
        cls.pts = pts
        cls.pts_count = pts_count

    @staticmethod
    def read(data) -> "AffectedMessages":
        pts = Int.read(data)
        pts_count = Int.read(data)
        return AffectedMessages(pts=pts, pts_count=pts_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        return data.getvalue()


class StickerSet(TL):
    ID = 0xb60a24a6

    def __init__(cls, set: TL, packs: List[TL], documents: List[TL]):
        cls.set = set
        cls.packs = packs
        cls.documents = documents

    @staticmethod
    def read(data) -> "StickerSet":
        set = data.getobj()
        packs = data.getobj()
        documents = data.getobj()
        return StickerSet(set=set, packs=packs, documents=documents)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.set.getvalue())
        data.write(Vector().getvalue(cls.packs))
        data.write(Vector().getvalue(cls.documents))
        return data.getvalue()


class SavedGifsNotModified(TL):
    ID = 0xe8025ca2

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SavedGifsNotModified":
        
        return SavedGifsNotModified()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SavedGifs(TL):
    ID = 0x2e0709a5

    def __init__(cls, hash: int, gifs: List[TL]):
        cls.hash = hash
        cls.gifs = gifs

    @staticmethod
    def read(data) -> "SavedGifs":
        hash = Int.read(data)
        gifs = data.getobj()
        return SavedGifs(hash=hash, gifs=gifs)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        data.write(Vector().getvalue(cls.gifs))
        return data.getvalue()


class BotResults(TL):
    ID = 0x947ca848

    def __init__(cls, query_id: int, results: List[TL], cache_time: int, users: List[TL], gallery: bool = None, next_offset: str = None, switch_pm: TL = None):
        cls.gallery = gallery
        cls.query_id = query_id
        cls.next_offset = next_offset
        cls.switch_pm = switch_pm
        cls.results = results
        cls.cache_time = cache_time
        cls.users = users

    @staticmethod
    def read(data) -> "BotResults":
        flags = Int.read(data)
        gallery = True if flags & 1 else False
        query_id = Long.read(data)
        next_offset = String.read(data) if flags & 2 else None
        switch_pm = data.getobj() if flags & 4 else None
        results = data.getobj()
        cache_time = Int.read(data)
        users = data.getobj()
        return BotResults(gallery=gallery, query_id=query_id, next_offset=next_offset, switch_pm=switch_pm, results=results, cache_time=cache_time, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.gallery is not None else 0
        flags |= 2 if cls.next_offset is not None else 0
        flags |= 4 if cls.switch_pm is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.query_id))
        
        if cls.next_offset is not None:
            data.write(String.getvalue(cls.next_offset))
        
        if cls.switch_pm is not None:
            data.write(cls.switch_pm.getvalue())
        data.write(Vector().getvalue(cls.results))
        data.write(Int.getvalue(cls.cache_time))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class BotCallbackAnswer(TL):
    ID = 0x36585ea4

    def __init__(cls, cache_time: int, alert: bool = None, has_url: bool = None, native_ui: bool = None, message: str = None, url: str = None):
        cls.alert = alert
        cls.has_url = has_url
        cls.native_ui = native_ui
        cls.message = message
        cls.url = url
        cls.cache_time = cache_time

    @staticmethod
    def read(data) -> "BotCallbackAnswer":
        flags = Int.read(data)
        alert = True if flags & 2 else False
        has_url = True if flags & 8 else False
        native_ui = True if flags & 16 else False
        message = String.read(data) if flags & 1 else None
        url = String.read(data) if flags & 4 else None
        cache_time = Int.read(data)
        return BotCallbackAnswer(alert=alert, has_url=has_url, native_ui=native_ui, message=message, url=url, cache_time=cache_time)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.alert is not None else 0
        flags |= 8 if cls.has_url is not None else 0
        flags |= 16 if cls.native_ui is not None else 0
        flags |= 1 if cls.message is not None else 0
        flags |= 4 if cls.url is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.message is not None:
            data.write(String.getvalue(cls.message))
        
        if cls.url is not None:
            data.write(String.getvalue(cls.url))
        data.write(Int.getvalue(cls.cache_time))
        return data.getvalue()


class MessageEditData(TL):
    ID = 0x26b5dde6

    def __init__(cls, caption: bool = None):
        cls.caption = caption

    @staticmethod
    def read(data) -> "MessageEditData":
        flags = Int.read(data)
        caption = True if flags & 1 else False
        return MessageEditData(caption=caption)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.caption is not None else 0
        data.write(Int.getvalue(flags))
        return data.getvalue()


class PeerDialogs(TL):
    ID = 0x3371c354

    def __init__(cls, dialogs: List[TL], messages: List[TL], chats: List[TL], users: List[TL], state: TL):
        cls.dialogs = dialogs
        cls.messages = messages
        cls.chats = chats
        cls.users = users
        cls.state = state

    @staticmethod
    def read(data) -> "PeerDialogs":
        dialogs = data.getobj()
        messages = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        state = data.getobj()
        return PeerDialogs(dialogs=dialogs, messages=messages, chats=chats, users=users, state=state)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.dialogs))
        data.write(Vector().getvalue(cls.messages))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        data.write(cls.state.getvalue())
        return data.getvalue()


class FeaturedStickersNotModified(TL):
    ID = 0xc6dc0c66

    def __init__(cls, count: int):
        cls.count = count

    @staticmethod
    def read(data) -> "FeaturedStickersNotModified":
        count = Int.read(data)
        return FeaturedStickersNotModified(count=count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.count))
        return data.getvalue()


class FeaturedStickers(TL):
    ID = 0xb6abc341

    def __init__(cls, hash: int, count: int, sets: List[TL], unread: List[int]):
        cls.hash = hash
        cls.count = count
        cls.sets = sets
        cls.unread = unread

    @staticmethod
    def read(data) -> "FeaturedStickers":
        hash = Int.read(data)
        count = Int.read(data)
        sets = data.getobj()
        unread = data.getobj(Long)
        return FeaturedStickers(hash=hash, count=count, sets=sets, unread=unread)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        data.write(Int.getvalue(cls.count))
        data.write(Vector().getvalue(cls.sets))
        data.write(Vector().getvalue(cls.unread, Long))
        return data.getvalue()


class RecentStickersNotModified(TL):
    ID = 0xb17f890

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "RecentStickersNotModified":
        
        return RecentStickersNotModified()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class RecentStickers(TL):
    ID = 0x22f3afb3

    def __init__(cls, hash: int, packs: List[TL], stickers: List[TL], dates: List[int]):
        cls.hash = hash
        cls.packs = packs
        cls.stickers = stickers
        cls.dates = dates

    @staticmethod
    def read(data) -> "RecentStickers":
        hash = Int.read(data)
        packs = data.getobj()
        stickers = data.getobj()
        dates = data.getobj(Int)
        return RecentStickers(hash=hash, packs=packs, stickers=stickers, dates=dates)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        data.write(Vector().getvalue(cls.packs))
        data.write(Vector().getvalue(cls.stickers))
        data.write(Vector().getvalue(cls.dates, Int))
        return data.getvalue()


class ArchivedStickers(TL):
    ID = 0x4fcba9c8

    def __init__(cls, count: int, sets: List[TL]):
        cls.count = count
        cls.sets = sets

    @staticmethod
    def read(data) -> "ArchivedStickers":
        count = Int.read(data)
        sets = data.getobj()
        return ArchivedStickers(count=count, sets=sets)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.count))
        data.write(Vector().getvalue(cls.sets))
        return data.getvalue()


class StickerSetInstallResultSuccess(TL):
    ID = 0x38641628

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "StickerSetInstallResultSuccess":
        
        return StickerSetInstallResultSuccess()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class StickerSetInstallResultArchive(TL):
    ID = 0x35e410a8

    def __init__(cls, sets: List[TL]):
        cls.sets = sets

    @staticmethod
    def read(data) -> "StickerSetInstallResultArchive":
        sets = data.getobj()
        return StickerSetInstallResultArchive(sets=sets)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.sets))
        return data.getvalue()


class HighScores(TL):
    ID = 0x9a3bfd99

    def __init__(cls, scores: List[TL], users: List[TL]):
        cls.scores = scores
        cls.users = users

    @staticmethod
    def read(data) -> "HighScores":
        scores = data.getobj()
        users = data.getobj()
        return HighScores(scores=scores, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.scores))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class FavedStickersNotModified(TL):
    ID = 0x9e8fa6d3

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "FavedStickersNotModified":
        
        return FavedStickersNotModified()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class FavedStickers(TL):
    ID = 0xf37f2f16

    def __init__(cls, hash: int, packs: List[TL], stickers: List[TL]):
        cls.hash = hash
        cls.packs = packs
        cls.stickers = stickers

    @staticmethod
    def read(data) -> "FavedStickers":
        hash = Int.read(data)
        packs = data.getobj()
        stickers = data.getobj()
        return FavedStickers(hash=hash, packs=packs, stickers=stickers)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        data.write(Vector().getvalue(cls.packs))
        data.write(Vector().getvalue(cls.stickers))
        return data.getvalue()


class FoundStickerSetsNotModified(TL):
    ID = 0xd54b65d

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "FoundStickerSetsNotModified":
        
        return FoundStickerSetsNotModified()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class FoundStickerSets(TL):
    ID = 0x5108d648

    def __init__(cls, hash: int, sets: List[TL]):
        cls.hash = hash
        cls.sets = sets

    @staticmethod
    def read(data) -> "FoundStickerSets":
        hash = Int.read(data)
        sets = data.getobj()
        return FoundStickerSets(hash=hash, sets=sets)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.hash))
        data.write(Vector().getvalue(cls.sets))
        return data.getvalue()


class SearchCounter(TL):
    ID = 0xe844ebff

    def __init__(cls, filter: TL, count: int, inexact: bool = None):
        cls.inexact = inexact
        cls.filter = filter
        cls.count = count

    @staticmethod
    def read(data) -> "SearchCounter":
        flags = Int.read(data)
        inexact = True if flags & 2 else False
        filter = data.getobj()
        count = Int.read(data)
        return SearchCounter(inexact=inexact, filter=filter, count=count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.inexact is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.filter.getvalue())
        data.write(Int.getvalue(cls.count))
        return data.getvalue()


class InactiveChats(TL):
    ID = 0xa927fec5

    def __init__(cls, dates: List[int], chats: List[TL], users: List[TL]):
        cls.dates = dates
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "InactiveChats":
        dates = data.getobj(Int)
        chats = data.getobj()
        users = data.getobj()
        return InactiveChats(dates=dates, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.dates, Int))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class VotesList(TL):
    ID = 0x823f649

    def __init__(cls, count: int, votes: List[TL], users: List[TL], next_offset: str = None):
        cls.count = count
        cls.votes = votes
        cls.users = users
        cls.next_offset = next_offset

    @staticmethod
    def read(data) -> "VotesList":
        flags = Int.read(data)
        count = Int.read(data)
        votes = data.getobj()
        users = data.getobj()
        next_offset = String.read(data) if flags & 1 else None
        return VotesList(count=count, votes=votes, users=users, next_offset=next_offset)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.next_offset is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.count))
        data.write(Vector().getvalue(cls.votes))
        data.write(Vector().getvalue(cls.users))
        
        if cls.next_offset is not None:
            data.write(String.getvalue(cls.next_offset))
        return data.getvalue()


class MessageViews(TL):
    ID = 0xb6c4f543

    def __init__(cls, views: List[TL], chats: List[TL], users: List[TL]):
        cls.views = views
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "MessageViews":
        views = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return MessageViews(views=views, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.views))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class DiscussionMessage(TL):
    ID = 0xf5dd8f9d

    def __init__(cls, messages: List[TL], chats: List[TL], users: List[TL], max_id: int = None, read_inbox_max_id: int = None, read_outbox_max_id: int = None):
        cls.messages = messages
        cls.max_id = max_id
        cls.read_inbox_max_id = read_inbox_max_id
        cls.read_outbox_max_id = read_outbox_max_id
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "DiscussionMessage":
        flags = Int.read(data)
        messages = data.getobj()
        max_id = Int.read(data) if flags & 1 else None
        read_inbox_max_id = Int.read(data) if flags & 2 else None
        read_outbox_max_id = Int.read(data) if flags & 4 else None
        chats = data.getobj()
        users = data.getobj()
        return DiscussionMessage(messages=messages, max_id=max_id, read_inbox_max_id=read_inbox_max_id, read_outbox_max_id=read_outbox_max_id, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.max_id is not None else 0
        flags |= 2 if cls.read_inbox_max_id is not None else 0
        flags |= 4 if cls.read_outbox_max_id is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Vector().getvalue(cls.messages))
        
        if cls.max_id is not None:
            data.write(Int.getvalue(cls.max_id))
        
        if cls.read_inbox_max_id is not None:
            data.write(Int.getvalue(cls.read_inbox_max_id))
        
        if cls.read_outbox_max_id is not None:
            data.write(Int.getvalue(cls.read_outbox_max_id))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class HistoryImport(TL):
    ID = 0x1662af0b

    def __init__(cls, id: int):
        cls.id = id

    @staticmethod
    def read(data) -> "HistoryImport":
        id = Long.read(data)
        return HistoryImport(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        return data.getvalue()


class HistoryImportParsed(TL):
    ID = 0x5e0fb7b9

    def __init__(cls, pm: bool = None, group: bool = None, title: str = None):
        cls.pm = pm
        cls.group = group
        cls.title = title

    @staticmethod
    def read(data) -> "HistoryImportParsed":
        flags = Int.read(data)
        pm = True if flags & 1 else False
        group = True if flags & 2 else False
        title = String.read(data) if flags & 4 else None
        return HistoryImportParsed(pm=pm, group=group, title=title)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.pm is not None else 0
        flags |= 2 if cls.group is not None else 0
        flags |= 4 if cls.title is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.title is not None:
            data.write(String.getvalue(cls.title))
        return data.getvalue()


class AffectedFoundMessages(TL):
    ID = 0xef8d3e6c

    def __init__(cls, pts: int, pts_count: int, offset: int, messages: List[int]):
        cls.pts = pts
        cls.pts_count = pts_count
        cls.offset = offset
        cls.messages = messages

    @staticmethod
    def read(data) -> "AffectedFoundMessages":
        pts = Int.read(data)
        pts_count = Int.read(data)
        offset = Int.read(data)
        messages = data.getobj(Int)
        return AffectedFoundMessages(pts=pts, pts_count=pts_count, offset=offset, messages=messages)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        data.write(Int.getvalue(cls.offset))
        data.write(Vector().getvalue(cls.messages, Int))
        return data.getvalue()


class ExportedChatInvites(TL):
    ID = 0xbdc62dcc

    def __init__(cls, count: int, invites: List[TL], users: List[TL]):
        cls.count = count
        cls.invites = invites
        cls.users = users

    @staticmethod
    def read(data) -> "ExportedChatInvites":
        count = Int.read(data)
        invites = data.getobj()
        users = data.getobj()
        return ExportedChatInvites(count=count, invites=invites, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.count))
        data.write(Vector().getvalue(cls.invites))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class ExportedChatInvite(TL):
    ID = 0x1871be50

    def __init__(cls, invite: TL, users: List[TL]):
        cls.invite = invite
        cls.users = users

    @staticmethod
    def read(data) -> "ExportedChatInvite":
        invite = data.getobj()
        users = data.getobj()
        return ExportedChatInvite(invite=invite, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.invite.getvalue())
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class ExportedChatInviteReplaced(TL):
    ID = 0x222600ef

    def __init__(cls, invite: TL, new_invite: TL, users: List[TL]):
        cls.invite = invite
        cls.new_invite = new_invite
        cls.users = users

    @staticmethod
    def read(data) -> "ExportedChatInviteReplaced":
        invite = data.getobj()
        new_invite = data.getobj()
        users = data.getobj()
        return ExportedChatInviteReplaced(invite=invite, new_invite=new_invite, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.invite.getvalue())
        data.write(cls.new_invite.getvalue())
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class ChatInviteImporters(TL):
    ID = 0x81b6b00a

    def __init__(cls, count: int, importers: List[TL], users: List[TL]):
        cls.count = count
        cls.importers = importers
        cls.users = users

    @staticmethod
    def read(data) -> "ChatInviteImporters":
        count = Int.read(data)
        importers = data.getobj()
        users = data.getobj()
        return ChatInviteImporters(count=count, importers=importers, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.count))
        data.write(Vector().getvalue(cls.importers))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class ChatAdminsWithInvites(TL):
    ID = 0xb69b72d7

    def __init__(cls, admins: List[TL], users: List[TL]):
        cls.admins = admins
        cls.users = users

    @staticmethod
    def read(data) -> "ChatAdminsWithInvites":
        admins = data.getobj()
        users = data.getobj()
        return ChatAdminsWithInvites(admins=admins, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.admins))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()
