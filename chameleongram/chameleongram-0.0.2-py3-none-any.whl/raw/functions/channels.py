from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class ReadHistory(TL):
    ID = 0xcc104937

    def __init__(cls, channel: TL, max_id: int):
        cls.channel = channel
        cls.max_id = max_id

    @staticmethod
    def read(data) -> "ReadHistory":
        channel = data.getobj()
        max_id = Int.read(data)
        return ReadHistory(channel=channel, max_id=max_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(Int.getvalue(cls.max_id))
        return data.getvalue()


class DeleteMessages(TL):
    ID = 0x84c1fd4e

    def __init__(cls, channel: TL, id: List[int]):
        cls.channel = channel
        cls.id = id

    @staticmethod
    def read(data) -> "DeleteMessages":
        channel = data.getobj()
        id = data.getobj(Int)
        return DeleteMessages(channel=channel, id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(Vector().getvalue(cls.id, Int))
        return data.getvalue()


class DeleteUserHistory(TL):
    ID = 0xd10dd71b

    def __init__(cls, channel: TL, user_id: TL):
        cls.channel = channel
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "DeleteUserHistory":
        channel = data.getobj()
        user_id = data.getobj()
        return DeleteUserHistory(channel=channel, user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(cls.user_id.getvalue())
        return data.getvalue()


class ReportSpam(TL):
    ID = 0xfe087810

    def __init__(cls, channel: TL, user_id: TL, id: List[int]):
        cls.channel = channel
        cls.user_id = user_id
        cls.id = id

    @staticmethod
    def read(data) -> "ReportSpam":
        channel = data.getobj()
        user_id = data.getobj()
        id = data.getobj(Int)
        return ReportSpam(channel=channel, user_id=user_id, id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(cls.user_id.getvalue())
        data.write(Vector().getvalue(cls.id, Int))
        return data.getvalue()


class GetMessages(TL):
    ID = 0xad8c9a23

    def __init__(cls, channel: TL, id: List[TL]):
        cls.channel = channel
        cls.id = id

    @staticmethod
    def read(data) -> "GetMessages":
        channel = data.getobj()
        id = data.getobj()
        return GetMessages(channel=channel, id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(Vector().getvalue(cls.id))
        return data.getvalue()


class GetParticipants(TL):
    ID = 0x123e05e9

    def __init__(cls, channel: TL, filter: TL, offset: int, limit: int, hash: int):
        cls.channel = channel
        cls.filter = filter
        cls.offset = offset
        cls.limit = limit
        cls.hash = hash

    @staticmethod
    def read(data) -> "GetParticipants":
        channel = data.getobj()
        filter = data.getobj()
        offset = Int.read(data)
        limit = Int.read(data)
        hash = Int.read(data)
        return GetParticipants(channel=channel, filter=filter, offset=offset, limit=limit, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(cls.filter.getvalue())
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.limit))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class GetParticipant(TL):
    ID = 0x546dd7a6

    def __init__(cls, channel: TL, user_id: TL):
        cls.channel = channel
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "GetParticipant":
        channel = data.getobj()
        user_id = data.getobj()
        return GetParticipant(channel=channel, user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(cls.user_id.getvalue())
        return data.getvalue()


class GetChannels(TL):
    ID = 0xa7f6bbb

    def __init__(cls, id: List[TL]):
        cls.id = id

    @staticmethod
    def read(data) -> "GetChannels":
        id = data.getobj()
        return GetChannels(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.id))
        return data.getvalue()


class GetFullChannel(TL):
    ID = 0x8736a09

    def __init__(cls, channel: TL):
        cls.channel = channel

    @staticmethod
    def read(data) -> "GetFullChannel":
        channel = data.getobj()
        return GetFullChannel(channel=channel)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        return data.getvalue()


class CreateChannel(TL):
    ID = 0x3d5fb10f

    def __init__(cls, title: str, about: str, broadcast: bool = None, megagroup: bool = None, for_import: bool = None, geo_point: TL = None, address: str = None):
        cls.broadcast = broadcast
        cls.megagroup = megagroup
        cls.for_import = for_import
        cls.title = title
        cls.about = about
        cls.geo_point = geo_point
        cls.address = address

    @staticmethod
    def read(data) -> "CreateChannel":
        flags = Int.read(data)
        broadcast = True if flags & 1 else False
        megagroup = True if flags & 2 else False
        for_import = True if flags & 8 else False
        title = String.read(data)
        about = String.read(data)
        geo_point = data.getobj() if flags & 4 else None
        address = String.read(data) if flags & 4 else None
        return CreateChannel(broadcast=broadcast, megagroup=megagroup, for_import=for_import, title=title, about=about, geo_point=geo_point, address=address)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.broadcast is not None else 0
        flags |= 2 if cls.megagroup is not None else 0
        flags |= 8 if cls.for_import is not None else 0
        flags |= 4 if cls.geo_point is not None else 0
        flags |= 4 if cls.address is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.title))
        data.write(String.getvalue(cls.about))
        
        if cls.geo_point is not None:
            data.write(cls.geo_point.getvalue())
        
        if cls.address is not None:
            data.write(String.getvalue(cls.address))
        return data.getvalue()


class EditAdmin(TL):
    ID = 0xd33c8902

    def __init__(cls, channel: TL, user_id: TL, admin_rights: TL, rank: str):
        cls.channel = channel
        cls.user_id = user_id
        cls.admin_rights = admin_rights
        cls.rank = rank

    @staticmethod
    def read(data) -> "EditAdmin":
        channel = data.getobj()
        user_id = data.getobj()
        admin_rights = data.getobj()
        rank = String.read(data)
        return EditAdmin(channel=channel, user_id=user_id, admin_rights=admin_rights, rank=rank)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(cls.user_id.getvalue())
        data.write(cls.admin_rights.getvalue())
        data.write(String.getvalue(cls.rank))
        return data.getvalue()


class EditTitle(TL):
    ID = 0x566decd0

    def __init__(cls, channel: TL, title: str):
        cls.channel = channel
        cls.title = title

    @staticmethod
    def read(data) -> "EditTitle":
        channel = data.getobj()
        title = String.read(data)
        return EditTitle(channel=channel, title=title)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(String.getvalue(cls.title))
        return data.getvalue()


class EditPhoto(TL):
    ID = 0xf12e57c9

    def __init__(cls, channel: TL, photo: TL):
        cls.channel = channel
        cls.photo = photo

    @staticmethod
    def read(data) -> "EditPhoto":
        channel = data.getobj()
        photo = data.getobj()
        return EditPhoto(channel=channel, photo=photo)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(cls.photo.getvalue())
        return data.getvalue()


class CheckUsername(TL):
    ID = 0x10e6bd2c

    def __init__(cls, channel: TL, username: str):
        cls.channel = channel
        cls.username = username

    @staticmethod
    def read(data) -> "CheckUsername":
        channel = data.getobj()
        username = String.read(data)
        return CheckUsername(channel=channel, username=username)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(String.getvalue(cls.username))
        return data.getvalue()


class UpdateUsername(TL):
    ID = 0x3514b3de

    def __init__(cls, channel: TL, username: str):
        cls.channel = channel
        cls.username = username

    @staticmethod
    def read(data) -> "UpdateUsername":
        channel = data.getobj()
        username = String.read(data)
        return UpdateUsername(channel=channel, username=username)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(String.getvalue(cls.username))
        return data.getvalue()


class JoinChannel(TL):
    ID = 0x24b524c5

    def __init__(cls, channel: TL):
        cls.channel = channel

    @staticmethod
    def read(data) -> "JoinChannel":
        channel = data.getobj()
        return JoinChannel(channel=channel)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        return data.getvalue()


class LeaveChannel(TL):
    ID = 0xf836aa95

    def __init__(cls, channel: TL):
        cls.channel = channel

    @staticmethod
    def read(data) -> "LeaveChannel":
        channel = data.getobj()
        return LeaveChannel(channel=channel)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        return data.getvalue()


class InviteToChannel(TL):
    ID = 0x199f3a6c

    def __init__(cls, channel: TL, users: List[TL]):
        cls.channel = channel
        cls.users = users

    @staticmethod
    def read(data) -> "InviteToChannel":
        channel = data.getobj()
        users = data.getobj()
        return InviteToChannel(channel=channel, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class DeleteChannel(TL):
    ID = 0xc0111fe3

    def __init__(cls, channel: TL):
        cls.channel = channel

    @staticmethod
    def read(data) -> "DeleteChannel":
        channel = data.getobj()
        return DeleteChannel(channel=channel)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        return data.getvalue()


class ExportMessageLink(TL):
    ID = 0xe63fadeb

    def __init__(cls, channel: TL, id: int, grouped: bool = None, thread: bool = None):
        cls.grouped = grouped
        cls.thread = thread
        cls.channel = channel
        cls.id = id

    @staticmethod
    def read(data) -> "ExportMessageLink":
        flags = Int.read(data)
        grouped = True if flags & 1 else False
        thread = True if flags & 2 else False
        channel = data.getobj()
        id = Int.read(data)
        return ExportMessageLink(grouped=grouped, thread=thread, channel=channel, id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.grouped is not None else 0
        flags |= 2 if cls.thread is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.channel.getvalue())
        data.write(Int.getvalue(cls.id))
        return data.getvalue()


class ToggleSignatures(TL):
    ID = 0x1f69b606

    def __init__(cls, channel: TL, enabled: bool):
        cls.channel = channel
        cls.enabled = enabled

    @staticmethod
    def read(data) -> "ToggleSignatures":
        channel = data.getobj()
        enabled = Bool.read(data)
        return ToggleSignatures(channel=channel, enabled=enabled)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(Bool.getvalue(cls.enabled))
        return data.getvalue()


class GetAdminedPublicChannels(TL):
    ID = 0xf8b036af

    def __init__(cls, by_location: bool = None, check_limit: bool = None):
        cls.by_location = by_location
        cls.check_limit = check_limit

    @staticmethod
    def read(data) -> "GetAdminedPublicChannels":
        flags = Int.read(data)
        by_location = True if flags & 1 else False
        check_limit = True if flags & 2 else False
        return GetAdminedPublicChannels(by_location=by_location, check_limit=check_limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.by_location is not None else 0
        flags |= 2 if cls.check_limit is not None else 0
        data.write(Int.getvalue(flags))
        return data.getvalue()


class EditBanned(TL):
    ID = 0x72796912

    def __init__(cls, channel: TL, user_id: TL, banned_rights: TL):
        cls.channel = channel
        cls.user_id = user_id
        cls.banned_rights = banned_rights

    @staticmethod
    def read(data) -> "EditBanned":
        channel = data.getobj()
        user_id = data.getobj()
        banned_rights = data.getobj()
        return EditBanned(channel=channel, user_id=user_id, banned_rights=banned_rights)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(cls.user_id.getvalue())
        data.write(cls.banned_rights.getvalue())
        return data.getvalue()


class GetAdminLog(TL):
    ID = 0x33ddf480

    def __init__(cls, channel: TL, q: str, max_id: int, min_id: int, limit: int, events_filter: TL = None, admins: List[TL] = None):
        cls.channel = channel
        cls.q = q
        cls.events_filter = events_filter
        cls.admins = admins
        cls.max_id = max_id
        cls.min_id = min_id
        cls.limit = limit

    @staticmethod
    def read(data) -> "GetAdminLog":
        flags = Int.read(data)
        channel = data.getobj()
        q = String.read(data)
        events_filter = data.getobj() if flags & 1 else None
        admins = data.getobj() if flags & 2 else []
        max_id = Long.read(data)
        min_id = Long.read(data)
        limit = Int.read(data)
        return GetAdminLog(channel=channel, q=q, events_filter=events_filter, admins=admins, max_id=max_id, min_id=min_id, limit=limit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.events_filter is not None else 0
        flags |= 2 if cls.admins is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.channel.getvalue())
        data.write(String.getvalue(cls.q))
        
        if cls.events_filter is not None:
            data.write(cls.events_filter.getvalue())
        
        if cls.admins is not None:
            data.write(Vector().getvalue(cls.admins))
        data.write(Long.getvalue(cls.max_id))
        data.write(Long.getvalue(cls.min_id))
        data.write(Int.getvalue(cls.limit))
        return data.getvalue()


class SetStickers(TL):
    ID = 0xea8ca4f9

    def __init__(cls, channel: TL, stickerset: TL):
        cls.channel = channel
        cls.stickerset = stickerset

    @staticmethod
    def read(data) -> "SetStickers":
        channel = data.getobj()
        stickerset = data.getobj()
        return SetStickers(channel=channel, stickerset=stickerset)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(cls.stickerset.getvalue())
        return data.getvalue()


class ReadMessageContents(TL):
    ID = 0xeab5dc38

    def __init__(cls, channel: TL, id: List[int]):
        cls.channel = channel
        cls.id = id

    @staticmethod
    def read(data) -> "ReadMessageContents":
        channel = data.getobj()
        id = data.getobj(Int)
        return ReadMessageContents(channel=channel, id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(Vector().getvalue(cls.id, Int))
        return data.getvalue()


class DeleteHistory(TL):
    ID = 0xaf369d42

    def __init__(cls, channel: TL, max_id: int):
        cls.channel = channel
        cls.max_id = max_id

    @staticmethod
    def read(data) -> "DeleteHistory":
        channel = data.getobj()
        max_id = Int.read(data)
        return DeleteHistory(channel=channel, max_id=max_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(Int.getvalue(cls.max_id))
        return data.getvalue()


class TogglePreHistoryHidden(TL):
    ID = 0xeabbb94c

    def __init__(cls, channel: TL, enabled: bool):
        cls.channel = channel
        cls.enabled = enabled

    @staticmethod
    def read(data) -> "TogglePreHistoryHidden":
        channel = data.getobj()
        enabled = Bool.read(data)
        return TogglePreHistoryHidden(channel=channel, enabled=enabled)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(Bool.getvalue(cls.enabled))
        return data.getvalue()


class GetLeftChannels(TL):
    ID = 0x8341ecc0

    def __init__(cls, offset: int):
        cls.offset = offset

    @staticmethod
    def read(data) -> "GetLeftChannels":
        offset = Int.read(data)
        return GetLeftChannels(offset=offset)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        return data.getvalue()


class GetGroupsForDiscussion(TL):
    ID = 0xf5dad378

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetGroupsForDiscussion":
        
        return GetGroupsForDiscussion()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SetDiscussionGroup(TL):
    ID = 0x40582bb2

    def __init__(cls, broadcast: TL, group: TL):
        cls.broadcast = broadcast
        cls.group = group

    @staticmethod
    def read(data) -> "SetDiscussionGroup":
        broadcast = data.getobj()
        group = data.getobj()
        return SetDiscussionGroup(broadcast=broadcast, group=group)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.broadcast.getvalue())
        data.write(cls.group.getvalue())
        return data.getvalue()


class EditCreator(TL):
    ID = 0x8f38cd1f

    def __init__(cls, channel: TL, user_id: TL, password: TL):
        cls.channel = channel
        cls.user_id = user_id
        cls.password = password

    @staticmethod
    def read(data) -> "EditCreator":
        channel = data.getobj()
        user_id = data.getobj()
        password = data.getobj()
        return EditCreator(channel=channel, user_id=user_id, password=password)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(cls.user_id.getvalue())
        data.write(cls.password.getvalue())
        return data.getvalue()


class EditLocation(TL):
    ID = 0x58e63f6d

    def __init__(cls, channel: TL, geo_point: TL, address: str):
        cls.channel = channel
        cls.geo_point = geo_point
        cls.address = address

    @staticmethod
    def read(data) -> "EditLocation":
        channel = data.getobj()
        geo_point = data.getobj()
        address = String.read(data)
        return EditLocation(channel=channel, geo_point=geo_point, address=address)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(cls.geo_point.getvalue())
        data.write(String.getvalue(cls.address))
        return data.getvalue()


class ToggleSlowMode(TL):
    ID = 0xedd49ef0

    def __init__(cls, channel: TL, seconds: int):
        cls.channel = channel
        cls.seconds = seconds

    @staticmethod
    def read(data) -> "ToggleSlowMode":
        channel = data.getobj()
        seconds = Int.read(data)
        return ToggleSlowMode(channel=channel, seconds=seconds)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        data.write(Int.getvalue(cls.seconds))
        return data.getvalue()


class GetInactiveChannels(TL):
    ID = 0x11e831ee

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetInactiveChannels":
        
        return GetInactiveChannels()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ConvertToGigagroup(TL):
    ID = 0xb290c69

    def __init__(cls, channel: TL):
        cls.channel = channel

    @staticmethod
    def read(data) -> "ConvertToGigagroup":
        channel = data.getobj()
        return ConvertToGigagroup(channel=channel)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        return data.getvalue()
