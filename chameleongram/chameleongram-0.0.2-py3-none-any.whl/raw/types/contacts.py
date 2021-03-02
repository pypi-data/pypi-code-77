from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class ContactsNotModified(TL):
    ID = 0xb74ba9d2

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ContactsNotModified":
        
        return ContactsNotModified()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class Contacts(TL):
    ID = 0xeae87e42

    def __init__(cls, contacts: List[TL], saved_count: int, users: List[TL]):
        cls.contacts = contacts
        cls.saved_count = saved_count
        cls.users = users

    @staticmethod
    def read(data) -> "Contacts":
        contacts = data.getobj()
        saved_count = Int.read(data)
        users = data.getobj()
        return Contacts(contacts=contacts, saved_count=saved_count, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.contacts))
        data.write(Int.getvalue(cls.saved_count))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class ImportedContacts(TL):
    ID = 0x77d01c3b

    def __init__(cls, imported: List[TL], popular_invites: List[TL], retry_contacts: List[int], users: List[TL]):
        cls.imported = imported
        cls.popular_invites = popular_invites
        cls.retry_contacts = retry_contacts
        cls.users = users

    @staticmethod
    def read(data) -> "ImportedContacts":
        imported = data.getobj()
        popular_invites = data.getobj()
        retry_contacts = data.getobj(Long)
        users = data.getobj()
        return ImportedContacts(imported=imported, popular_invites=popular_invites, retry_contacts=retry_contacts, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.imported))
        data.write(Vector().getvalue(cls.popular_invites))
        data.write(Vector().getvalue(cls.retry_contacts, Long))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class Blocked(TL):
    ID = 0xade1591

    def __init__(cls, blocked: List[TL], chats: List[TL], users: List[TL]):
        cls.blocked = blocked
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "Blocked":
        blocked = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return Blocked(blocked=blocked, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.blocked))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class BlockedSlice(TL):
    ID = 0xe1664194

    def __init__(cls, count: int, blocked: List[TL], chats: List[TL], users: List[TL]):
        cls.count = count
        cls.blocked = blocked
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "BlockedSlice":
        count = Int.read(data)
        blocked = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return BlockedSlice(count=count, blocked=blocked, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.count))
        data.write(Vector().getvalue(cls.blocked))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class Found(TL):
    ID = 0xb3134d9d

    def __init__(cls, my_results: List[TL], results: List[TL], chats: List[TL], users: List[TL]):
        cls.my_results = my_results
        cls.results = results
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "Found":
        my_results = data.getobj()
        results = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return Found(my_results=my_results, results=results, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.my_results))
        data.write(Vector().getvalue(cls.results))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class ResolvedPeer(TL):
    ID = 0x7f077ad9

    def __init__(cls, peer: TL, chats: List[TL], users: List[TL]):
        cls.peer = peer
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "ResolvedPeer":
        peer = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return ResolvedPeer(peer=peer, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class TopPeersNotModified(TL):
    ID = 0xde266ef5

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "TopPeersNotModified":
        
        return TopPeersNotModified()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class TopPeers(TL):
    ID = 0x70b772a8

    def __init__(cls, categories: List[TL], chats: List[TL], users: List[TL]):
        cls.categories = categories
        cls.chats = chats
        cls.users = users

    @staticmethod
    def read(data) -> "TopPeers":
        categories = data.getobj()
        chats = data.getobj()
        users = data.getobj()
        return TopPeers(categories=categories, chats=chats, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.categories))
        data.write(Vector().getvalue(cls.chats))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class TopPeersDisabled(TL):
    ID = 0xb52c939d

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "TopPeersDisabled":
        
        return TopPeersDisabled()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()
