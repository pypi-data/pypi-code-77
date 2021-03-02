from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO
from .storage import FileUnknown, FilePartial, FileJpeg, FileGif, FilePng, FilePdf, FileMp3, FileMov, FileMp4, FileWebp
from .auth import SentCode, Authorization, AuthorizationSignUpRequired, ExportedAuthorization, PasswordRecovery, CodeTypeSms, CodeTypeCall, CodeTypeFlashCall, SentCodeTypeApp, SentCodeTypeSms, SentCodeTypeCall, SentCodeTypeFlashCall, LoginToken, LoginTokenMigrateTo, LoginTokenSuccess
from .contacts import ContactsNotModified, Contacts, ImportedContacts, Blocked, BlockedSlice, Found, ResolvedPeer, TopPeersNotModified, TopPeers, TopPeersDisabled
from .messages import Dialogs, DialogsSlice, DialogsNotModified, Messages, MessagesSlice, ChannelMessages, MessagesNotModified, Chats, ChatsSlice, ChatFull, AffectedHistory, DhConfigNotModified, DhConfig, SentEncryptedMessage, SentEncryptedFile, StickersNotModified, Stickers, AllStickersNotModified, AllStickers, AffectedMessages, StickerSet, SavedGifsNotModified, SavedGifs, BotResults, BotCallbackAnswer, MessageEditData, PeerDialogs, FeaturedStickersNotModified, FeaturedStickers, RecentStickersNotModified, RecentStickers, ArchivedStickers, StickerSetInstallResultSuccess, StickerSetInstallResultArchive, HighScores, FavedStickersNotModified, FavedStickers, FoundStickerSetsNotModified, FoundStickerSets, SearchCounter, InactiveChats, VotesList, MessageViews, DiscussionMessage, HistoryImport, HistoryImportParsed, AffectedFoundMessages, ExportedChatInvites, ExportedChatInvite, ExportedChatInviteReplaced, ChatInviteImporters, ChatAdminsWithInvites
from .updates import State, DifferenceEmpty, Difference, DifferenceSlice, DifferenceTooLong, ChannelDifferenceEmpty, ChannelDifferenceTooLong, ChannelDifference
from .photos import Photos, PhotosSlice, Photo
from .upload import File, FileCdnRedirect, WebFile, CdnFileReuploadNeeded, CdnFile
from .help import AppUpdate, NoAppUpdate, InviteText, Support, TermsOfService, RecentMeUrls, TermsOfServiceUpdateEmpty, TermsOfServiceUpdate, DeepLinkInfoEmpty, DeepLinkInfo, PassportConfigNotModified, PassportConfig, SupportName, UserInfoEmpty, UserInfo, PromoDataEmpty, PromoData, CountryCode, Country, CountriesListNotModified, CountriesList
from .account import PrivacyRules, Authorizations, Password, PasswordSettings, PasswordInputSettings, TmpPassword, WebAuthorizations, AuthorizationForm, SentEmailCode, Takeout, WallPapersNotModified, WallPapers, AutoDownloadSettings, ThemesNotModified, Themes, ContentSettings
from .channels import ChannelParticipants, ChannelParticipantsNotModified, ChannelParticipant, AdminLogResults
from .payments import PaymentForm, ValidatedRequestedInfo, PaymentResult, PaymentVerificationNeeded, PaymentReceipt, SavedInfo, BankCardData
from .phone import PhoneCall, GroupCall, GroupParticipants
from .stats import BroadcastStats, MegagroupStats, MessageStats

class InputPeerEmpty(TL):
    ID = 0x7f3b18ea

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputPeerEmpty":
        
        return InputPeerEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPeerSelf(TL):
    ID = 0x7da07ec9

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputPeerSelf":
        
        return InputPeerSelf()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPeerChat(TL):
    ID = 0x179be863

    def __init__(cls, chat_id: int):
        cls.chat_id = chat_id

    @staticmethod
    def read(data) -> "InputPeerChat":
        chat_id = Int.read(data)
        return InputPeerChat(chat_id=chat_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        return data.getvalue()


class InputPeerUser(TL):
    ID = 0x7b8e7de6

    def __init__(cls, user_id: int, access_hash: int):
        cls.user_id = user_id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputPeerUser":
        user_id = Int.read(data)
        access_hash = Long.read(data)
        return InputPeerUser(user_id=user_id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class InputPeerChannel(TL):
    ID = 0x20adaef8

    def __init__(cls, channel_id: int, access_hash: int):
        cls.channel_id = channel_id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputPeerChannel":
        channel_id = Int.read(data)
        access_hash = Long.read(data)
        return InputPeerChannel(channel_id=channel_id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.channel_id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class InputPeerUserFromMessage(TL):
    ID = 0x17bae2e6

    def __init__(cls, peer: TL, msg_id: int, user_id: int):
        cls.peer = peer
        cls.msg_id = msg_id
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "InputPeerUserFromMessage":
        peer = data.getobj()
        msg_id = Int.read(data)
        user_id = Int.read(data)
        return InputPeerUserFromMessage(peer=peer, msg_id=msg_id, user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        data.write(Int.getvalue(cls.user_id))
        return data.getvalue()


class InputPeerChannelFromMessage(TL):
    ID = 0x9c95f7bb

    def __init__(cls, peer: TL, msg_id: int, channel_id: int):
        cls.peer = peer
        cls.msg_id = msg_id
        cls.channel_id = channel_id

    @staticmethod
    def read(data) -> "InputPeerChannelFromMessage":
        peer = data.getobj()
        msg_id = Int.read(data)
        channel_id = Int.read(data)
        return InputPeerChannelFromMessage(peer=peer, msg_id=msg_id, channel_id=channel_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        data.write(Int.getvalue(cls.channel_id))
        return data.getvalue()


class InputUserEmpty(TL):
    ID = 0xb98886cf

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputUserEmpty":
        
        return InputUserEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputUserSelf(TL):
    ID = 0xf7c1b13f

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputUserSelf":
        
        return InputUserSelf()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputUser(TL):
    ID = 0xd8292816

    def __init__(cls, user_id: int, access_hash: int):
        cls.user_id = user_id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputUser":
        user_id = Int.read(data)
        access_hash = Long.read(data)
        return InputUser(user_id=user_id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class InputUserFromMessage(TL):
    ID = 0x2d117597

    def __init__(cls, peer: TL, msg_id: int, user_id: int):
        cls.peer = peer
        cls.msg_id = msg_id
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "InputUserFromMessage":
        peer = data.getobj()
        msg_id = Int.read(data)
        user_id = Int.read(data)
        return InputUserFromMessage(peer=peer, msg_id=msg_id, user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        data.write(Int.getvalue(cls.user_id))
        return data.getvalue()


class InputPhoneContact(TL):
    ID = 0xf392b7f4

    def __init__(cls, client_id: int, phone: str, first_name: str, last_name: str):
        cls.client_id = client_id
        cls.phone = phone
        cls.first_name = first_name
        cls.last_name = last_name

    @staticmethod
    def read(data) -> "InputPhoneContact":
        client_id = Long.read(data)
        phone = String.read(data)
        first_name = String.read(data)
        last_name = String.read(data)
        return InputPhoneContact(client_id=client_id, phone=phone, first_name=first_name, last_name=last_name)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.client_id))
        data.write(String.getvalue(cls.phone))
        data.write(String.getvalue(cls.first_name))
        data.write(String.getvalue(cls.last_name))
        return data.getvalue()


class InputFile(TL):
    ID = 0xf52ff27f

    def __init__(cls, id: int, parts: int, name: str, md5_checksum: str):
        cls.id = id
        cls.parts = parts
        cls.name = name
        cls.md5_checksum = md5_checksum

    @staticmethod
    def read(data) -> "InputFile":
        id = Long.read(data)
        parts = Int.read(data)
        name = String.read(data)
        md5_checksum = String.read(data)
        return InputFile(id=id, parts=parts, name=name, md5_checksum=md5_checksum)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Int.getvalue(cls.parts))
        data.write(String.getvalue(cls.name))
        data.write(String.getvalue(cls.md5_checksum))
        return data.getvalue()


class InputFileBig(TL):
    ID = 0xfa4f0bb5

    def __init__(cls, id: int, parts: int, name: str):
        cls.id = id
        cls.parts = parts
        cls.name = name

    @staticmethod
    def read(data) -> "InputFileBig":
        id = Long.read(data)
        parts = Int.read(data)
        name = String.read(data)
        return InputFileBig(id=id, parts=parts, name=name)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Int.getvalue(cls.parts))
        data.write(String.getvalue(cls.name))
        return data.getvalue()


class InputMediaEmpty(TL):
    ID = 0x9664f57f

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMediaEmpty":
        
        return InputMediaEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMediaUploadedPhoto(TL):
    ID = 0x1e287d04

    def __init__(cls, file: TL, stickers: List[TL] = None, ttl_seconds: int = None):
        cls.file = file
        cls.stickers = stickers
        cls.ttl_seconds = ttl_seconds

    @staticmethod
    def read(data) -> "InputMediaUploadedPhoto":
        flags = Int.read(data)
        file = data.getobj()
        stickers = data.getobj() if flags & 1 else []
        ttl_seconds = Int.read(data) if flags & 2 else None
        return InputMediaUploadedPhoto(file=file, stickers=stickers, ttl_seconds=ttl_seconds)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.stickers is not None else 0
        flags |= 2 if cls.ttl_seconds is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.file.getvalue())
        
        if cls.stickers is not None:
            data.write(Vector().getvalue(cls.stickers))
        
        if cls.ttl_seconds is not None:
            data.write(Int.getvalue(cls.ttl_seconds))
        return data.getvalue()


class InputMediaPhoto(TL):
    ID = 0xb3ba0635

    def __init__(cls, id: TL, ttl_seconds: int = None):
        cls.id = id
        cls.ttl_seconds = ttl_seconds

    @staticmethod
    def read(data) -> "InputMediaPhoto":
        flags = Int.read(data)
        id = data.getobj()
        ttl_seconds = Int.read(data) if flags & 1 else None
        return InputMediaPhoto(id=id, ttl_seconds=ttl_seconds)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.ttl_seconds is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.id.getvalue())
        
        if cls.ttl_seconds is not None:
            data.write(Int.getvalue(cls.ttl_seconds))
        return data.getvalue()


class InputMediaGeoPoint(TL):
    ID = 0xf9c44144

    def __init__(cls, geo_point: TL):
        cls.geo_point = geo_point

    @staticmethod
    def read(data) -> "InputMediaGeoPoint":
        geo_point = data.getobj()
        return InputMediaGeoPoint(geo_point=geo_point)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.geo_point.getvalue())
        return data.getvalue()


class InputMediaContact(TL):
    ID = 0xf8ab7dfb

    def __init__(cls, phone_number: str, first_name: str, last_name: str, vcard: str):
        cls.phone_number = phone_number
        cls.first_name = first_name
        cls.last_name = last_name
        cls.vcard = vcard

    @staticmethod
    def read(data) -> "InputMediaContact":
        phone_number = String.read(data)
        first_name = String.read(data)
        last_name = String.read(data)
        vcard = String.read(data)
        return InputMediaContact(phone_number=phone_number, first_name=first_name, last_name=last_name, vcard=vcard)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone_number))
        data.write(String.getvalue(cls.first_name))
        data.write(String.getvalue(cls.last_name))
        data.write(String.getvalue(cls.vcard))
        return data.getvalue()


class InputMediaUploadedDocument(TL):
    ID = 0x5b38c6c1

    def __init__(cls, file: TL, mime_type: str, attributes: List[TL], nosound_video: bool = None, force_file: bool = None, thumb: TL = None, stickers: List[TL] = None, ttl_seconds: int = None):
        cls.nosound_video = nosound_video
        cls.force_file = force_file
        cls.file = file
        cls.thumb = thumb
        cls.mime_type = mime_type
        cls.attributes = attributes
        cls.stickers = stickers
        cls.ttl_seconds = ttl_seconds

    @staticmethod
    def read(data) -> "InputMediaUploadedDocument":
        flags = Int.read(data)
        nosound_video = True if flags & 8 else False
        force_file = True if flags & 16 else False
        file = data.getobj()
        thumb = data.getobj() if flags & 4 else None
        mime_type = String.read(data)
        attributes = data.getobj()
        stickers = data.getobj() if flags & 1 else []
        ttl_seconds = Int.read(data) if flags & 2 else None
        return InputMediaUploadedDocument(nosound_video=nosound_video, force_file=force_file, file=file, thumb=thumb, mime_type=mime_type, attributes=attributes, stickers=stickers, ttl_seconds=ttl_seconds)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 8 if cls.nosound_video is not None else 0
        flags |= 16 if cls.force_file is not None else 0
        flags |= 4 if cls.thumb is not None else 0
        flags |= 1 if cls.stickers is not None else 0
        flags |= 2 if cls.ttl_seconds is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.file.getvalue())
        
        if cls.thumb is not None:
            data.write(cls.thumb.getvalue())
        data.write(String.getvalue(cls.mime_type))
        data.write(Vector().getvalue(cls.attributes))
        
        if cls.stickers is not None:
            data.write(Vector().getvalue(cls.stickers))
        
        if cls.ttl_seconds is not None:
            data.write(Int.getvalue(cls.ttl_seconds))
        return data.getvalue()


class InputMediaDocument(TL):
    ID = 0x33473058

    def __init__(cls, id: TL, ttl_seconds: int = None, query: str = None):
        cls.id = id
        cls.ttl_seconds = ttl_seconds
        cls.query = query

    @staticmethod
    def read(data) -> "InputMediaDocument":
        flags = Int.read(data)
        id = data.getobj()
        ttl_seconds = Int.read(data) if flags & 1 else None
        query = String.read(data) if flags & 2 else None
        return InputMediaDocument(id=id, ttl_seconds=ttl_seconds, query=query)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.ttl_seconds is not None else 0
        flags |= 2 if cls.query is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.id.getvalue())
        
        if cls.ttl_seconds is not None:
            data.write(Int.getvalue(cls.ttl_seconds))
        
        if cls.query is not None:
            data.write(String.getvalue(cls.query))
        return data.getvalue()


class InputMediaVenue(TL):
    ID = 0xc13d1c11

    def __init__(cls, geo_point: TL, title: str, address: str, provider: str, venue_id: str, venue_type: str):
        cls.geo_point = geo_point
        cls.title = title
        cls.address = address
        cls.provider = provider
        cls.venue_id = venue_id
        cls.venue_type = venue_type

    @staticmethod
    def read(data) -> "InputMediaVenue":
        geo_point = data.getobj()
        title = String.read(data)
        address = String.read(data)
        provider = String.read(data)
        venue_id = String.read(data)
        venue_type = String.read(data)
        return InputMediaVenue(geo_point=geo_point, title=title, address=address, provider=provider, venue_id=venue_id, venue_type=venue_type)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.geo_point.getvalue())
        data.write(String.getvalue(cls.title))
        data.write(String.getvalue(cls.address))
        data.write(String.getvalue(cls.provider))
        data.write(String.getvalue(cls.venue_id))
        data.write(String.getvalue(cls.venue_type))
        return data.getvalue()


class InputMediaPhotoExternal(TL):
    ID = 0xe5bbfe1a

    def __init__(cls, url: str, ttl_seconds: int = None):
        cls.url = url
        cls.ttl_seconds = ttl_seconds

    @staticmethod
    def read(data) -> "InputMediaPhotoExternal":
        flags = Int.read(data)
        url = String.read(data)
        ttl_seconds = Int.read(data) if flags & 1 else None
        return InputMediaPhotoExternal(url=url, ttl_seconds=ttl_seconds)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.ttl_seconds is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.url))
        
        if cls.ttl_seconds is not None:
            data.write(Int.getvalue(cls.ttl_seconds))
        return data.getvalue()


class InputMediaDocumentExternal(TL):
    ID = 0xfb52dc99

    def __init__(cls, url: str, ttl_seconds: int = None):
        cls.url = url
        cls.ttl_seconds = ttl_seconds

    @staticmethod
    def read(data) -> "InputMediaDocumentExternal":
        flags = Int.read(data)
        url = String.read(data)
        ttl_seconds = Int.read(data) if flags & 1 else None
        return InputMediaDocumentExternal(url=url, ttl_seconds=ttl_seconds)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.ttl_seconds is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.url))
        
        if cls.ttl_seconds is not None:
            data.write(Int.getvalue(cls.ttl_seconds))
        return data.getvalue()


class InputMediaGame(TL):
    ID = 0xd33f43f3

    def __init__(cls, id: TL):
        cls.id = id

    @staticmethod
    def read(data) -> "InputMediaGame":
        id = data.getobj()
        return InputMediaGame(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.id.getvalue())
        return data.getvalue()


class InputMediaInvoice(TL):
    ID = 0xf4e096c3

    def __init__(cls, title: str, description: str, invoice: TL, payload: bytes, provider: str, provider_data: TL, start_param: str, photo: TL = None):
        cls.title = title
        cls.description = description
        cls.photo = photo
        cls.invoice = invoice
        cls.payload = payload
        cls.provider = provider
        cls.provider_data = provider_data
        cls.start_param = start_param

    @staticmethod
    def read(data) -> "InputMediaInvoice":
        flags = Int.read(data)
        title = String.read(data)
        description = String.read(data)
        photo = data.getobj() if flags & 1 else None
        invoice = data.getobj()
        payload = Bytes.read(data)
        provider = String.read(data)
        provider_data = data.getobj()
        start_param = String.read(data)
        return InputMediaInvoice(title=title, description=description, photo=photo, invoice=invoice, payload=payload, provider=provider, provider_data=provider_data, start_param=start_param)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.photo is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.title))
        data.write(String.getvalue(cls.description))
        
        if cls.photo is not None:
            data.write(cls.photo.getvalue())
        data.write(cls.invoice.getvalue())
        data.write(Bytes.getvalue(cls.payload))
        data.write(String.getvalue(cls.provider))
        data.write(cls.provider_data.getvalue())
        data.write(String.getvalue(cls.start_param))
        return data.getvalue()


class InputMediaGeoLive(TL):
    ID = 0x971fa843

    def __init__(cls, geo_point: TL, stopped: bool = None, heading: int = None, period: int = None, proximity_notification_radius: int = None):
        cls.stopped = stopped
        cls.geo_point = geo_point
        cls.heading = heading
        cls.period = period
        cls.proximity_notification_radius = proximity_notification_radius

    @staticmethod
    def read(data) -> "InputMediaGeoLive":
        flags = Int.read(data)
        stopped = True if flags & 1 else False
        geo_point = data.getobj()
        heading = Int.read(data) if flags & 4 else None
        period = Int.read(data) if flags & 2 else None
        proximity_notification_radius = Int.read(data) if flags & 8 else None
        return InputMediaGeoLive(stopped=stopped, geo_point=geo_point, heading=heading, period=period, proximity_notification_radius=proximity_notification_radius)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.stopped is not None else 0
        flags |= 4 if cls.heading is not None else 0
        flags |= 2 if cls.period is not None else 0
        flags |= 8 if cls.proximity_notification_radius is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.geo_point.getvalue())
        
        if cls.heading is not None:
            data.write(Int.getvalue(cls.heading))
        
        if cls.period is not None:
            data.write(Int.getvalue(cls.period))
        
        if cls.proximity_notification_radius is not None:
            data.write(Int.getvalue(cls.proximity_notification_radius))
        return data.getvalue()


class InputMediaPoll(TL):
    ID = 0xf94e5f1

    def __init__(cls, poll: TL, correct_answers: List[bytes] = None, solution: str = None, solution_entities: List[TL] = None):
        cls.poll = poll
        cls.correct_answers = correct_answers
        cls.solution = solution
        cls.solution_entities = solution_entities

    @staticmethod
    def read(data) -> "InputMediaPoll":
        flags = Int.read(data)
        poll = data.getobj()
        correct_answers = Bytes.read(data) if flags & 1 else None
        solution = String.read(data) if flags & 2 else None
        solution_entities = data.getobj() if flags & 2 else []
        return InputMediaPoll(poll=poll, correct_answers=correct_answers, solution=solution, solution_entities=solution_entities)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.correct_answers is not None else 0
        flags |= 2 if cls.solution is not None else 0
        flags |= 2 if cls.solution_entities is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.poll.getvalue())
        
        if cls.correct_answers is not None:
            data.write(Vector().getvalue(cls.correct_answers, Bytes))
        
        if cls.solution is not None:
            data.write(String.getvalue(cls.solution))
        
        if cls.solution_entities is not None:
            data.write(Vector().getvalue(cls.solution_entities))
        return data.getvalue()


class InputMediaDice(TL):
    ID = 0xe66fbf7b

    def __init__(cls, emoticon: str):
        cls.emoticon = emoticon

    @staticmethod
    def read(data) -> "InputMediaDice":
        emoticon = String.read(data)
        return InputMediaDice(emoticon=emoticon)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.emoticon))
        return data.getvalue()


class InputChatPhotoEmpty(TL):
    ID = 0x1ca48f57

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputChatPhotoEmpty":
        
        return InputChatPhotoEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputChatUploadedPhoto(TL):
    ID = 0xc642724e

    def __init__(cls, file: TL = None, video: TL = None, video_start_ts: float = None):
        cls.file = file
        cls.video = video
        cls.video_start_ts = video_start_ts

    @staticmethod
    def read(data) -> "InputChatUploadedPhoto":
        flags = Int.read(data)
        file = data.getobj() if flags & 1 else None
        video = data.getobj() if flags & 2 else None
        video_start_ts = Double.read(data) if flags & 4 else None
        return InputChatUploadedPhoto(file=file, video=video, video_start_ts=video_start_ts)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.file is not None else 0
        flags |= 2 if cls.video is not None else 0
        flags |= 4 if cls.video_start_ts is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.file is not None:
            data.write(cls.file.getvalue())
        
        if cls.video is not None:
            data.write(cls.video.getvalue())
        
        if cls.video_start_ts is not None:
            data.write(Double.getvalue(cls.video_start_ts))
        return data.getvalue()


class InputChatPhoto(TL):
    ID = 0x8953ad37

    def __init__(cls, id: TL):
        cls.id = id

    @staticmethod
    def read(data) -> "InputChatPhoto":
        id = data.getobj()
        return InputChatPhoto(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.id.getvalue())
        return data.getvalue()


class InputGeoPointEmpty(TL):
    ID = 0xe4c123d6

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputGeoPointEmpty":
        
        return InputGeoPointEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputGeoPoint(TL):
    ID = 0x48222faf

    def __init__(cls, lat: float, long: float, accuracy_radius: int = None):
        cls.lat = lat
        cls.long = long
        cls.accuracy_radius = accuracy_radius

    @staticmethod
    def read(data) -> "InputGeoPoint":
        flags = Int.read(data)
        lat = Double.read(data)
        long = Double.read(data)
        accuracy_radius = Int.read(data) if flags & 1 else None
        return InputGeoPoint(lat=lat, long=long, accuracy_radius=accuracy_radius)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.accuracy_radius is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Double.getvalue(cls.lat))
        data.write(Double.getvalue(cls.long))
        
        if cls.accuracy_radius is not None:
            data.write(Int.getvalue(cls.accuracy_radius))
        return data.getvalue()


class InputPhotoEmpty(TL):
    ID = 0x1cd7bf0d

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputPhotoEmpty":
        
        return InputPhotoEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPhoto(TL):
    ID = 0x3bb3b94a

    def __init__(cls, id: int, access_hash: int, file_reference: bytes):
        cls.id = id
        cls.access_hash = access_hash
        cls.file_reference = file_reference

    @staticmethod
    def read(data) -> "InputPhoto":
        id = Long.read(data)
        access_hash = Long.read(data)
        file_reference = Bytes.read(data)
        return InputPhoto(id=id, access_hash=access_hash, file_reference=file_reference)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Bytes.getvalue(cls.file_reference))
        return data.getvalue()


class InputFileLocation(TL):
    ID = 0xdfdaabe1

    def __init__(cls, volume_id: int, local_id: int, secret: int, file_reference: bytes):
        cls.volume_id = volume_id
        cls.local_id = local_id
        cls.secret = secret
        cls.file_reference = file_reference

    @staticmethod
    def read(data) -> "InputFileLocation":
        volume_id = Long.read(data)
        local_id = Int.read(data)
        secret = Long.read(data)
        file_reference = Bytes.read(data)
        return InputFileLocation(volume_id=volume_id, local_id=local_id, secret=secret, file_reference=file_reference)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.volume_id))
        data.write(Int.getvalue(cls.local_id))
        data.write(Long.getvalue(cls.secret))
        data.write(Bytes.getvalue(cls.file_reference))
        return data.getvalue()


class InputEncryptedFileLocation(TL):
    ID = 0xf5235d55

    def __init__(cls, id: int, access_hash: int):
        cls.id = id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputEncryptedFileLocation":
        id = Long.read(data)
        access_hash = Long.read(data)
        return InputEncryptedFileLocation(id=id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class InputDocumentFileLocation(TL):
    ID = 0xbad07584

    def __init__(cls, id: int, access_hash: int, file_reference: bytes, thumb_size: str):
        cls.id = id
        cls.access_hash = access_hash
        cls.file_reference = file_reference
        cls.thumb_size = thumb_size

    @staticmethod
    def read(data) -> "InputDocumentFileLocation":
        id = Long.read(data)
        access_hash = Long.read(data)
        file_reference = Bytes.read(data)
        thumb_size = String.read(data)
        return InputDocumentFileLocation(id=id, access_hash=access_hash, file_reference=file_reference, thumb_size=thumb_size)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Bytes.getvalue(cls.file_reference))
        data.write(String.getvalue(cls.thumb_size))
        return data.getvalue()


class InputSecureFileLocation(TL):
    ID = 0xcbc7ee28

    def __init__(cls, id: int, access_hash: int):
        cls.id = id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputSecureFileLocation":
        id = Long.read(data)
        access_hash = Long.read(data)
        return InputSecureFileLocation(id=id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class InputTakeoutFileLocation(TL):
    ID = 0x29be5899

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputTakeoutFileLocation":
        
        return InputTakeoutFileLocation()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPhotoFileLocation(TL):
    ID = 0x40181ffe

    def __init__(cls, id: int, access_hash: int, file_reference: bytes, thumb_size: str):
        cls.id = id
        cls.access_hash = access_hash
        cls.file_reference = file_reference
        cls.thumb_size = thumb_size

    @staticmethod
    def read(data) -> "InputPhotoFileLocation":
        id = Long.read(data)
        access_hash = Long.read(data)
        file_reference = Bytes.read(data)
        thumb_size = String.read(data)
        return InputPhotoFileLocation(id=id, access_hash=access_hash, file_reference=file_reference, thumb_size=thumb_size)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Bytes.getvalue(cls.file_reference))
        data.write(String.getvalue(cls.thumb_size))
        return data.getvalue()


class InputPhotoLegacyFileLocation(TL):
    ID = 0xd83466f3

    def __init__(cls, id: int, access_hash: int, file_reference: bytes, volume_id: int, local_id: int, secret: int):
        cls.id = id
        cls.access_hash = access_hash
        cls.file_reference = file_reference
        cls.volume_id = volume_id
        cls.local_id = local_id
        cls.secret = secret

    @staticmethod
    def read(data) -> "InputPhotoLegacyFileLocation":
        id = Long.read(data)
        access_hash = Long.read(data)
        file_reference = Bytes.read(data)
        volume_id = Long.read(data)
        local_id = Int.read(data)
        secret = Long.read(data)
        return InputPhotoLegacyFileLocation(id=id, access_hash=access_hash, file_reference=file_reference, volume_id=volume_id, local_id=local_id, secret=secret)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Bytes.getvalue(cls.file_reference))
        data.write(Long.getvalue(cls.volume_id))
        data.write(Int.getvalue(cls.local_id))
        data.write(Long.getvalue(cls.secret))
        return data.getvalue()


class InputPeerPhotoFileLocation(TL):
    ID = 0x27d69997

    def __init__(cls, peer: TL, volume_id: int, local_id: int, big: bool = None):
        cls.big = big
        cls.peer = peer
        cls.volume_id = volume_id
        cls.local_id = local_id

    @staticmethod
    def read(data) -> "InputPeerPhotoFileLocation":
        flags = Int.read(data)
        big = True if flags & 1 else False
        peer = data.getobj()
        volume_id = Long.read(data)
        local_id = Int.read(data)
        return InputPeerPhotoFileLocation(big=big, peer=peer, volume_id=volume_id, local_id=local_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.big is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(Long.getvalue(cls.volume_id))
        data.write(Int.getvalue(cls.local_id))
        return data.getvalue()


class InputStickerSetThumb(TL):
    ID = 0xdbaeae9

    def __init__(cls, stickerset: TL, volume_id: int, local_id: int):
        cls.stickerset = stickerset
        cls.volume_id = volume_id
        cls.local_id = local_id

    @staticmethod
    def read(data) -> "InputStickerSetThumb":
        stickerset = data.getobj()
        volume_id = Long.read(data)
        local_id = Int.read(data)
        return InputStickerSetThumb(stickerset=stickerset, volume_id=volume_id, local_id=local_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.stickerset.getvalue())
        data.write(Long.getvalue(cls.volume_id))
        data.write(Int.getvalue(cls.local_id))
        return data.getvalue()


class PeerUser(TL):
    ID = 0x9db1bc6d

    def __init__(cls, user_id: int):
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "PeerUser":
        user_id = Int.read(data)
        return PeerUser(user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        return data.getvalue()


class PeerChat(TL):
    ID = 0xbad0e5bb

    def __init__(cls, chat_id: int):
        cls.chat_id = chat_id

    @staticmethod
    def read(data) -> "PeerChat":
        chat_id = Int.read(data)
        return PeerChat(chat_id=chat_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        return data.getvalue()


class PeerChannel(TL):
    ID = 0xbddde532

    def __init__(cls, channel_id: int):
        cls.channel_id = channel_id

    @staticmethod
    def read(data) -> "PeerChannel":
        channel_id = Int.read(data)
        return PeerChannel(channel_id=channel_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.channel_id))
        return data.getvalue()


class UserEmpty(TL):
    ID = 0x200250ba

    def __init__(cls, id: int):
        cls.id = id

    @staticmethod
    def read(data) -> "UserEmpty":
        id = Int.read(data)
        return UserEmpty(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.id))
        return data.getvalue()


class User(TL):
    ID = 0x938458c1

    def __init__(cls, id: int, self: bool = None, contact: bool = None, mutual_contact: bool = None, deleted: bool = None, bot: bool = None, bot_chat_history: bool = None, bot_nochats: bool = None, verified: bool = None, restricted: bool = None, min: bool = None, bot_inline_geo: bool = None, support: bool = None, scam: bool = None, apply_min_photo: bool = None, fake: bool = None, access_hash: int = None, first_name: str = None, last_name: str = None, username: str = None, phone: str = None, photo: TL = None, status: TL = None, bot_info_version: int = None, restriction_reason: List[TL] = None, bot_inline_placeholder: str = None, lang_code: str = None):
        cls.self = self
        cls.contact = contact
        cls.mutual_contact = mutual_contact
        cls.deleted = deleted
        cls.bot = bot
        cls.bot_chat_history = bot_chat_history
        cls.bot_nochats = bot_nochats
        cls.verified = verified
        cls.restricted = restricted
        cls.min = min
        cls.bot_inline_geo = bot_inline_geo
        cls.support = support
        cls.scam = scam
        cls.apply_min_photo = apply_min_photo
        cls.fake = fake
        cls.id = id
        cls.access_hash = access_hash
        cls.first_name = first_name
        cls.last_name = last_name
        cls.username = username
        cls.phone = phone
        cls.photo = photo
        cls.status = status
        cls.bot_info_version = bot_info_version
        cls.restriction_reason = restriction_reason
        cls.bot_inline_placeholder = bot_inline_placeholder
        cls.lang_code = lang_code

    @staticmethod
    def read(data) -> "User":
        flags = Int.read(data)
        self = True if flags & 1024 else False
        contact = True if flags & 2048 else False
        mutual_contact = True if flags & 4096 else False
        deleted = True if flags & 8192 else False
        bot = True if flags & 16384 else False
        bot_chat_history = True if flags & 32768 else False
        bot_nochats = True if flags & 65536 else False
        verified = True if flags & 131072 else False
        restricted = True if flags & 262144 else False
        min = True if flags & 1048576 else False
        bot_inline_geo = True if flags & 2097152 else False
        support = True if flags & 8388608 else False
        scam = True if flags & 16777216 else False
        apply_min_photo = True if flags & 33554432 else False
        fake = True if flags & 67108864 else False
        id = Int.read(data)
        access_hash = Long.read(data) if flags & 1 else None
        first_name = String.read(data) if flags & 2 else None
        last_name = String.read(data) if flags & 4 else None
        username = String.read(data) if flags & 8 else None
        phone = String.read(data) if flags & 16 else None
        photo = data.getobj() if flags & 32 else None
        status = data.getobj() if flags & 64 else None
        bot_info_version = Int.read(data) if flags & 16384 else None
        restriction_reason = data.getobj() if flags & 262144 else []
        bot_inline_placeholder = String.read(data) if flags & 524288 else None
        lang_code = String.read(data) if flags & 4194304 else None
        return User(self=self, contact=contact, mutual_contact=mutual_contact, deleted=deleted, bot=bot, bot_chat_history=bot_chat_history, bot_nochats=bot_nochats, verified=verified, restricted=restricted, min=min, bot_inline_geo=bot_inline_geo, support=support, scam=scam, apply_min_photo=apply_min_photo, fake=fake, id=id, access_hash=access_hash, first_name=first_name, last_name=last_name, username=username, phone=phone, photo=photo, status=status, bot_info_version=bot_info_version, restriction_reason=restriction_reason, bot_inline_placeholder=bot_inline_placeholder, lang_code=lang_code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1024 if cls.self is not None else 0
        flags |= 2048 if cls.contact is not None else 0
        flags |= 4096 if cls.mutual_contact is not None else 0
        flags |= 8192 if cls.deleted is not None else 0
        flags |= 16384 if cls.bot is not None else 0
        flags |= 32768 if cls.bot_chat_history is not None else 0
        flags |= 65536 if cls.bot_nochats is not None else 0
        flags |= 131072 if cls.verified is not None else 0
        flags |= 262144 if cls.restricted is not None else 0
        flags |= 1048576 if cls.min is not None else 0
        flags |= 2097152 if cls.bot_inline_geo is not None else 0
        flags |= 8388608 if cls.support is not None else 0
        flags |= 16777216 if cls.scam is not None else 0
        flags |= 33554432 if cls.apply_min_photo is not None else 0
        flags |= 67108864 if cls.fake is not None else 0
        flags |= 1 if cls.access_hash is not None else 0
        flags |= 2 if cls.first_name is not None else 0
        flags |= 4 if cls.last_name is not None else 0
        flags |= 8 if cls.username is not None else 0
        flags |= 16 if cls.phone is not None else 0
        flags |= 32 if cls.photo is not None else 0
        flags |= 64 if cls.status is not None else 0
        flags |= 16384 if cls.bot_info_version is not None else 0
        flags |= 262144 if cls.restriction_reason is not None else 0
        flags |= 524288 if cls.bot_inline_placeholder is not None else 0
        flags |= 4194304 if cls.lang_code is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        
        if cls.access_hash is not None:
            data.write(Long.getvalue(cls.access_hash))
        
        if cls.first_name is not None:
            data.write(String.getvalue(cls.first_name))
        
        if cls.last_name is not None:
            data.write(String.getvalue(cls.last_name))
        
        if cls.username is not None:
            data.write(String.getvalue(cls.username))
        
        if cls.phone is not None:
            data.write(String.getvalue(cls.phone))
        
        if cls.photo is not None:
            data.write(cls.photo.getvalue())
        
        if cls.status is not None:
            data.write(cls.status.getvalue())
        
        if cls.bot_info_version is not None:
            data.write(Int.getvalue(cls.bot_info_version))
        
        if cls.restriction_reason is not None:
            data.write(Vector().getvalue(cls.restriction_reason))
        
        if cls.bot_inline_placeholder is not None:
            data.write(String.getvalue(cls.bot_inline_placeholder))
        
        if cls.lang_code is not None:
            data.write(String.getvalue(cls.lang_code))
        return data.getvalue()


class UserProfilePhotoEmpty(TL):
    ID = 0x4f11bae1

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UserProfilePhotoEmpty":
        
        return UserProfilePhotoEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UserProfilePhoto(TL):
    ID = 0x69d3ab26

    def __init__(cls, photo_id: int, photo_small: TL, photo_big: TL, dc_id: int, has_video: bool = None):
        cls.has_video = has_video
        cls.photo_id = photo_id
        cls.photo_small = photo_small
        cls.photo_big = photo_big
        cls.dc_id = dc_id

    @staticmethod
    def read(data) -> "UserProfilePhoto":
        flags = Int.read(data)
        has_video = True if flags & 1 else False
        photo_id = Long.read(data)
        photo_small = data.getobj()
        photo_big = data.getobj()
        dc_id = Int.read(data)
        return UserProfilePhoto(has_video=has_video, photo_id=photo_id, photo_small=photo_small, photo_big=photo_big, dc_id=dc_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.has_video is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.photo_id))
        data.write(cls.photo_small.getvalue())
        data.write(cls.photo_big.getvalue())
        data.write(Int.getvalue(cls.dc_id))
        return data.getvalue()


class UserStatusEmpty(TL):
    ID = 0x9d05049

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UserStatusEmpty":
        
        return UserStatusEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UserStatusOnline(TL):
    ID = 0xedb93949

    def __init__(cls, expires: int):
        cls.expires = expires

    @staticmethod
    def read(data) -> "UserStatusOnline":
        expires = Int.read(data)
        return UserStatusOnline(expires=expires)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.expires))
        return data.getvalue()


class UserStatusOffline(TL):
    ID = 0x8c703f

    def __init__(cls, was_online: int):
        cls.was_online = was_online

    @staticmethod
    def read(data) -> "UserStatusOffline":
        was_online = Int.read(data)
        return UserStatusOffline(was_online=was_online)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.was_online))
        return data.getvalue()


class UserStatusRecently(TL):
    ID = 0xe26f42f1

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UserStatusRecently":
        
        return UserStatusRecently()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UserStatusLastWeek(TL):
    ID = 0x7bf09fc

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UserStatusLastWeek":
        
        return UserStatusLastWeek()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UserStatusLastMonth(TL):
    ID = 0x77ebc742

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UserStatusLastMonth":
        
        return UserStatusLastMonth()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ChatEmpty(TL):
    ID = 0x9ba2d800

    def __init__(cls, id: int):
        cls.id = id

    @staticmethod
    def read(data) -> "ChatEmpty":
        id = Int.read(data)
        return ChatEmpty(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.id))
        return data.getvalue()


class Chat(TL):
    ID = 0x3bda1bde

    def __init__(cls, id: int, title: str, photo: TL, participants_count: int, date: int, version: int, creator: bool = None, kicked: bool = None, left: bool = None, deactivated: bool = None, call_active: bool = None, call_not_empty: bool = None, migrated_to: TL = None, admin_rights: TL = None, default_banned_rights: TL = None):
        cls.creator = creator
        cls.kicked = kicked
        cls.left = left
        cls.deactivated = deactivated
        cls.call_active = call_active
        cls.call_not_empty = call_not_empty
        cls.id = id
        cls.title = title
        cls.photo = photo
        cls.participants_count = participants_count
        cls.date = date
        cls.version = version
        cls.migrated_to = migrated_to
        cls.admin_rights = admin_rights
        cls.default_banned_rights = default_banned_rights

    @staticmethod
    def read(data) -> "Chat":
        flags = Int.read(data)
        creator = True if flags & 1 else False
        kicked = True if flags & 2 else False
        left = True if flags & 4 else False
        deactivated = True if flags & 32 else False
        call_active = True if flags & 8388608 else False
        call_not_empty = True if flags & 16777216 else False
        id = Int.read(data)
        title = String.read(data)
        photo = data.getobj()
        participants_count = Int.read(data)
        date = Int.read(data)
        version = Int.read(data)
        migrated_to = data.getobj() if flags & 64 else None
        admin_rights = data.getobj() if flags & 16384 else None
        default_banned_rights = data.getobj() if flags & 262144 else None
        return Chat(creator=creator, kicked=kicked, left=left, deactivated=deactivated, call_active=call_active, call_not_empty=call_not_empty, id=id, title=title, photo=photo, participants_count=participants_count, date=date, version=version, migrated_to=migrated_to, admin_rights=admin_rights, default_banned_rights=default_banned_rights)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.creator is not None else 0
        flags |= 2 if cls.kicked is not None else 0
        flags |= 4 if cls.left is not None else 0
        flags |= 32 if cls.deactivated is not None else 0
        flags |= 8388608 if cls.call_active is not None else 0
        flags |= 16777216 if cls.call_not_empty is not None else 0
        flags |= 64 if cls.migrated_to is not None else 0
        flags |= 16384 if cls.admin_rights is not None else 0
        flags |= 262144 if cls.default_banned_rights is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        data.write(String.getvalue(cls.title))
        data.write(cls.photo.getvalue())
        data.write(Int.getvalue(cls.participants_count))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.version))
        
        if cls.migrated_to is not None:
            data.write(cls.migrated_to.getvalue())
        
        if cls.admin_rights is not None:
            data.write(cls.admin_rights.getvalue())
        
        if cls.default_banned_rights is not None:
            data.write(cls.default_banned_rights.getvalue())
        return data.getvalue()


class ChatForbidden(TL):
    ID = 0x7328bdb

    def __init__(cls, id: int, title: str):
        cls.id = id
        cls.title = title

    @staticmethod
    def read(data) -> "ChatForbidden":
        id = Int.read(data)
        title = String.read(data)
        return ChatForbidden(id=id, title=title)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.id))
        data.write(String.getvalue(cls.title))
        return data.getvalue()


class Channel(TL):
    ID = 0xd31a961e

    def __init__(cls, id: int, title: str, photo: TL, date: int, version: int, creator: bool = None, left: bool = None, broadcast: bool = None, verified: bool = None, megagroup: bool = None, restricted: bool = None, signatures: bool = None, min: bool = None, scam: bool = None, has_link: bool = None, has_geo: bool = None, slowmode_enabled: bool = None, call_active: bool = None, call_not_empty: bool = None, fake: bool = None, gigagroup: bool = None, access_hash: int = None, username: str = None, restriction_reason: List[TL] = None, admin_rights: TL = None, banned_rights: TL = None, default_banned_rights: TL = None, participants_count: int = None):
        cls.creator = creator
        cls.left = left
        cls.broadcast = broadcast
        cls.verified = verified
        cls.megagroup = megagroup
        cls.restricted = restricted
        cls.signatures = signatures
        cls.min = min
        cls.scam = scam
        cls.has_link = has_link
        cls.has_geo = has_geo
        cls.slowmode_enabled = slowmode_enabled
        cls.call_active = call_active
        cls.call_not_empty = call_not_empty
        cls.fake = fake
        cls.gigagroup = gigagroup
        cls.id = id
        cls.access_hash = access_hash
        cls.title = title
        cls.username = username
        cls.photo = photo
        cls.date = date
        cls.version = version
        cls.restriction_reason = restriction_reason
        cls.admin_rights = admin_rights
        cls.banned_rights = banned_rights
        cls.default_banned_rights = default_banned_rights
        cls.participants_count = participants_count

    @staticmethod
    def read(data) -> "Channel":
        flags = Int.read(data)
        creator = True if flags & 1 else False
        left = True if flags & 4 else False
        broadcast = True if flags & 32 else False
        verified = True if flags & 128 else False
        megagroup = True if flags & 256 else False
        restricted = True if flags & 512 else False
        signatures = True if flags & 2048 else False
        min = True if flags & 4096 else False
        scam = True if flags & 524288 else False
        has_link = True if flags & 1048576 else False
        has_geo = True if flags & 2097152 else False
        slowmode_enabled = True if flags & 4194304 else False
        call_active = True if flags & 8388608 else False
        call_not_empty = True if flags & 16777216 else False
        fake = True if flags & 33554432 else False
        gigagroup = True if flags & 67108864 else False
        id = Int.read(data)
        access_hash = Long.read(data) if flags & 8192 else None
        title = String.read(data)
        username = String.read(data) if flags & 64 else None
        photo = data.getobj()
        date = Int.read(data)
        version = Int.read(data)
        restriction_reason = data.getobj() if flags & 512 else []
        admin_rights = data.getobj() if flags & 16384 else None
        banned_rights = data.getobj() if flags & 32768 else None
        default_banned_rights = data.getobj() if flags & 262144 else None
        participants_count = Int.read(data) if flags & 131072 else None
        return Channel(creator=creator, left=left, broadcast=broadcast, verified=verified, megagroup=megagroup, restricted=restricted, signatures=signatures, min=min, scam=scam, has_link=has_link, has_geo=has_geo, slowmode_enabled=slowmode_enabled, call_active=call_active, call_not_empty=call_not_empty, fake=fake, gigagroup=gigagroup, id=id, access_hash=access_hash, title=title, username=username, photo=photo, date=date, version=version, restriction_reason=restriction_reason, admin_rights=admin_rights, banned_rights=banned_rights, default_banned_rights=default_banned_rights, participants_count=participants_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.creator is not None else 0
        flags |= 4 if cls.left is not None else 0
        flags |= 32 if cls.broadcast is not None else 0
        flags |= 128 if cls.verified is not None else 0
        flags |= 256 if cls.megagroup is not None else 0
        flags |= 512 if cls.restricted is not None else 0
        flags |= 2048 if cls.signatures is not None else 0
        flags |= 4096 if cls.min is not None else 0
        flags |= 524288 if cls.scam is not None else 0
        flags |= 1048576 if cls.has_link is not None else 0
        flags |= 2097152 if cls.has_geo is not None else 0
        flags |= 4194304 if cls.slowmode_enabled is not None else 0
        flags |= 8388608 if cls.call_active is not None else 0
        flags |= 16777216 if cls.call_not_empty is not None else 0
        flags |= 33554432 if cls.fake is not None else 0
        flags |= 67108864 if cls.gigagroup is not None else 0
        flags |= 8192 if cls.access_hash is not None else 0
        flags |= 64 if cls.username is not None else 0
        flags |= 512 if cls.restriction_reason is not None else 0
        flags |= 16384 if cls.admin_rights is not None else 0
        flags |= 32768 if cls.banned_rights is not None else 0
        flags |= 262144 if cls.default_banned_rights is not None else 0
        flags |= 131072 if cls.participants_count is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        
        if cls.access_hash is not None:
            data.write(Long.getvalue(cls.access_hash))
        data.write(String.getvalue(cls.title))
        
        if cls.username is not None:
            data.write(String.getvalue(cls.username))
        data.write(cls.photo.getvalue())
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.version))
        
        if cls.restriction_reason is not None:
            data.write(Vector().getvalue(cls.restriction_reason))
        
        if cls.admin_rights is not None:
            data.write(cls.admin_rights.getvalue())
        
        if cls.banned_rights is not None:
            data.write(cls.banned_rights.getvalue())
        
        if cls.default_banned_rights is not None:
            data.write(cls.default_banned_rights.getvalue())
        
        if cls.participants_count is not None:
            data.write(Int.getvalue(cls.participants_count))
        return data.getvalue()


class ChannelForbidden(TL):
    ID = 0x289da732

    def __init__(cls, id: int, access_hash: int, title: str, broadcast: bool = None, megagroup: bool = None, until_date: int = None):
        cls.broadcast = broadcast
        cls.megagroup = megagroup
        cls.id = id
        cls.access_hash = access_hash
        cls.title = title
        cls.until_date = until_date

    @staticmethod
    def read(data) -> "ChannelForbidden":
        flags = Int.read(data)
        broadcast = True if flags & 32 else False
        megagroup = True if flags & 256 else False
        id = Int.read(data)
        access_hash = Long.read(data)
        title = String.read(data)
        until_date = Int.read(data) if flags & 65536 else None
        return ChannelForbidden(broadcast=broadcast, megagroup=megagroup, id=id, access_hash=access_hash, title=title, until_date=until_date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 32 if cls.broadcast is not None else 0
        flags |= 256 if cls.megagroup is not None else 0
        flags |= 65536 if cls.until_date is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(String.getvalue(cls.title))
        
        if cls.until_date is not None:
            data.write(Int.getvalue(cls.until_date))
        return data.getvalue()


class ChatFull(TL):
    ID = 0xf06c4018

    def __init__(cls, id: int, about: str, participants: TL, notify_settings: TL, can_set_username: bool = None, has_scheduled: bool = None, chat_photo: TL = None, exported_invite: TL = None, bot_info: List[TL] = None, pinned_msg_id: int = None, folder_id: int = None, call: TL = None, ttl_period: int = None):
        cls.can_set_username = can_set_username
        cls.has_scheduled = has_scheduled
        cls.id = id
        cls.about = about
        cls.participants = participants
        cls.chat_photo = chat_photo
        cls.notify_settings = notify_settings
        cls.exported_invite = exported_invite
        cls.bot_info = bot_info
        cls.pinned_msg_id = pinned_msg_id
        cls.folder_id = folder_id
        cls.call = call
        cls.ttl_period = ttl_period

    @staticmethod
    def read(data) -> "ChatFull":
        flags = Int.read(data)
        can_set_username = True if flags & 128 else False
        has_scheduled = True if flags & 256 else False
        id = Int.read(data)
        about = String.read(data)
        participants = data.getobj()
        chat_photo = data.getobj() if flags & 4 else None
        notify_settings = data.getobj()
        exported_invite = data.getobj() if flags & 8192 else None
        bot_info = data.getobj() if flags & 8 else []
        pinned_msg_id = Int.read(data) if flags & 64 else None
        folder_id = Int.read(data) if flags & 2048 else None
        call = data.getobj() if flags & 4096 else None
        ttl_period = Int.read(data) if flags & 16384 else None
        return ChatFull(can_set_username=can_set_username, has_scheduled=has_scheduled, id=id, about=about, participants=participants, chat_photo=chat_photo, notify_settings=notify_settings, exported_invite=exported_invite, bot_info=bot_info, pinned_msg_id=pinned_msg_id, folder_id=folder_id, call=call, ttl_period=ttl_period)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 128 if cls.can_set_username is not None else 0
        flags |= 256 if cls.has_scheduled is not None else 0
        flags |= 4 if cls.chat_photo is not None else 0
        flags |= 8192 if cls.exported_invite is not None else 0
        flags |= 8 if cls.bot_info is not None else 0
        flags |= 64 if cls.pinned_msg_id is not None else 0
        flags |= 2048 if cls.folder_id is not None else 0
        flags |= 4096 if cls.call is not None else 0
        flags |= 16384 if cls.ttl_period is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        data.write(String.getvalue(cls.about))
        data.write(cls.participants.getvalue())
        
        if cls.chat_photo is not None:
            data.write(cls.chat_photo.getvalue())
        data.write(cls.notify_settings.getvalue())
        
        if cls.exported_invite is not None:
            data.write(cls.exported_invite.getvalue())
        
        if cls.bot_info is not None:
            data.write(Vector().getvalue(cls.bot_info))
        
        if cls.pinned_msg_id is not None:
            data.write(Int.getvalue(cls.pinned_msg_id))
        
        if cls.folder_id is not None:
            data.write(Int.getvalue(cls.folder_id))
        
        if cls.call is not None:
            data.write(cls.call.getvalue())
        
        if cls.ttl_period is not None:
            data.write(Int.getvalue(cls.ttl_period))
        return data.getvalue()


class ChannelFull(TL):
    ID = 0x2548c037

    def __init__(cls, id: int, about: str, read_inbox_max_id: int, read_outbox_max_id: int, unread_count: int, chat_photo: TL, notify_settings: TL, bot_info: List[TL], pts: int, can_view_participants: bool = None, can_set_username: bool = None, can_set_stickers: bool = None, hidden_prehistory: bool = None, can_set_location: bool = None, has_scheduled: bool = None, can_view_stats: bool = None, blocked: bool = None, participants_count: int = None, admins_count: int = None, kicked_count: int = None, banned_count: int = None, online_count: int = None, exported_invite: TL = None, migrated_from_chat_id: int = None, migrated_from_max_id: int = None, pinned_msg_id: int = None, stickerset: TL = None, available_min_id: int = None, folder_id: int = None, linked_chat_id: int = None, location: TL = None, slowmode_seconds: int = None, slowmode_next_send_date: int = None, stats_dc: int = None, call: TL = None, ttl_period: int = None, pending_suggestions: List[str] = None):
        cls.can_view_participants = can_view_participants
        cls.can_set_username = can_set_username
        cls.can_set_stickers = can_set_stickers
        cls.hidden_prehistory = hidden_prehistory
        cls.can_set_location = can_set_location
        cls.has_scheduled = has_scheduled
        cls.can_view_stats = can_view_stats
        cls.blocked = blocked
        cls.id = id
        cls.about = about
        cls.participants_count = participants_count
        cls.admins_count = admins_count
        cls.kicked_count = kicked_count
        cls.banned_count = banned_count
        cls.online_count = online_count
        cls.read_inbox_max_id = read_inbox_max_id
        cls.read_outbox_max_id = read_outbox_max_id
        cls.unread_count = unread_count
        cls.chat_photo = chat_photo
        cls.notify_settings = notify_settings
        cls.exported_invite = exported_invite
        cls.bot_info = bot_info
        cls.migrated_from_chat_id = migrated_from_chat_id
        cls.migrated_from_max_id = migrated_from_max_id
        cls.pinned_msg_id = pinned_msg_id
        cls.stickerset = stickerset
        cls.available_min_id = available_min_id
        cls.folder_id = folder_id
        cls.linked_chat_id = linked_chat_id
        cls.location = location
        cls.slowmode_seconds = slowmode_seconds
        cls.slowmode_next_send_date = slowmode_next_send_date
        cls.stats_dc = stats_dc
        cls.pts = pts
        cls.call = call
        cls.ttl_period = ttl_period
        cls.pending_suggestions = pending_suggestions

    @staticmethod
    def read(data) -> "ChannelFull":
        flags = Int.read(data)
        can_view_participants = True if flags & 8 else False
        can_set_username = True if flags & 64 else False
        can_set_stickers = True if flags & 128 else False
        hidden_prehistory = True if flags & 1024 else False
        can_set_location = True if flags & 65536 else False
        has_scheduled = True if flags & 524288 else False
        can_view_stats = True if flags & 1048576 else False
        blocked = True if flags & 4194304 else False
        id = Int.read(data)
        about = String.read(data)
        participants_count = Int.read(data) if flags & 1 else None
        admins_count = Int.read(data) if flags & 2 else None
        kicked_count = Int.read(data) if flags & 4 else None
        banned_count = Int.read(data) if flags & 4 else None
        online_count = Int.read(data) if flags & 8192 else None
        read_inbox_max_id = Int.read(data)
        read_outbox_max_id = Int.read(data)
        unread_count = Int.read(data)
        chat_photo = data.getobj()
        notify_settings = data.getobj()
        exported_invite = data.getobj() if flags & 8388608 else None
        bot_info = data.getobj()
        migrated_from_chat_id = Int.read(data) if flags & 16 else None
        migrated_from_max_id = Int.read(data) if flags & 16 else None
        pinned_msg_id = Int.read(data) if flags & 32 else None
        stickerset = data.getobj() if flags & 256 else None
        available_min_id = Int.read(data) if flags & 512 else None
        folder_id = Int.read(data) if flags & 2048 else None
        linked_chat_id = Int.read(data) if flags & 16384 else None
        location = data.getobj() if flags & 32768 else None
        slowmode_seconds = Int.read(data) if flags & 131072 else None
        slowmode_next_send_date = Int.read(data) if flags & 262144 else None
        stats_dc = Int.read(data) if flags & 4096 else None
        pts = Int.read(data)
        call = data.getobj() if flags & 2097152 else None
        ttl_period = Int.read(data) if flags & 16777216 else None
        pending_suggestions = String.read(data) if flags & 33554432 else None
        return ChannelFull(can_view_participants=can_view_participants, can_set_username=can_set_username, can_set_stickers=can_set_stickers, hidden_prehistory=hidden_prehistory, can_set_location=can_set_location, has_scheduled=has_scheduled, can_view_stats=can_view_stats, blocked=blocked, id=id, about=about, participants_count=participants_count, admins_count=admins_count, kicked_count=kicked_count, banned_count=banned_count, online_count=online_count, read_inbox_max_id=read_inbox_max_id, read_outbox_max_id=read_outbox_max_id, unread_count=unread_count, chat_photo=chat_photo, notify_settings=notify_settings, exported_invite=exported_invite, bot_info=bot_info, migrated_from_chat_id=migrated_from_chat_id, migrated_from_max_id=migrated_from_max_id, pinned_msg_id=pinned_msg_id, stickerset=stickerset, available_min_id=available_min_id, folder_id=folder_id, linked_chat_id=linked_chat_id, location=location, slowmode_seconds=slowmode_seconds, slowmode_next_send_date=slowmode_next_send_date, stats_dc=stats_dc, pts=pts, call=call, ttl_period=ttl_period, pending_suggestions=pending_suggestions)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 8 if cls.can_view_participants is not None else 0
        flags |= 64 if cls.can_set_username is not None else 0
        flags |= 128 if cls.can_set_stickers is not None else 0
        flags |= 1024 if cls.hidden_prehistory is not None else 0
        flags |= 65536 if cls.can_set_location is not None else 0
        flags |= 524288 if cls.has_scheduled is not None else 0
        flags |= 1048576 if cls.can_view_stats is not None else 0
        flags |= 4194304 if cls.blocked is not None else 0
        flags |= 1 if cls.participants_count is not None else 0
        flags |= 2 if cls.admins_count is not None else 0
        flags |= 4 if cls.kicked_count is not None else 0
        flags |= 4 if cls.banned_count is not None else 0
        flags |= 8192 if cls.online_count is not None else 0
        flags |= 8388608 if cls.exported_invite is not None else 0
        flags |= 16 if cls.migrated_from_chat_id is not None else 0
        flags |= 16 if cls.migrated_from_max_id is not None else 0
        flags |= 32 if cls.pinned_msg_id is not None else 0
        flags |= 256 if cls.stickerset is not None else 0
        flags |= 512 if cls.available_min_id is not None else 0
        flags |= 2048 if cls.folder_id is not None else 0
        flags |= 16384 if cls.linked_chat_id is not None else 0
        flags |= 32768 if cls.location is not None else 0
        flags |= 131072 if cls.slowmode_seconds is not None else 0
        flags |= 262144 if cls.slowmode_next_send_date is not None else 0
        flags |= 4096 if cls.stats_dc is not None else 0
        flags |= 2097152 if cls.call is not None else 0
        flags |= 16777216 if cls.ttl_period is not None else 0
        flags |= 33554432 if cls.pending_suggestions is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        data.write(String.getvalue(cls.about))
        
        if cls.participants_count is not None:
            data.write(Int.getvalue(cls.participants_count))
        
        if cls.admins_count is not None:
            data.write(Int.getvalue(cls.admins_count))
        
        if cls.kicked_count is not None:
            data.write(Int.getvalue(cls.kicked_count))
        
        if cls.banned_count is not None:
            data.write(Int.getvalue(cls.banned_count))
        
        if cls.online_count is not None:
            data.write(Int.getvalue(cls.online_count))
        data.write(Int.getvalue(cls.read_inbox_max_id))
        data.write(Int.getvalue(cls.read_outbox_max_id))
        data.write(Int.getvalue(cls.unread_count))
        data.write(cls.chat_photo.getvalue())
        data.write(cls.notify_settings.getvalue())
        
        if cls.exported_invite is not None:
            data.write(cls.exported_invite.getvalue())
        data.write(Vector().getvalue(cls.bot_info))
        
        if cls.migrated_from_chat_id is not None:
            data.write(Int.getvalue(cls.migrated_from_chat_id))
        
        if cls.migrated_from_max_id is not None:
            data.write(Int.getvalue(cls.migrated_from_max_id))
        
        if cls.pinned_msg_id is not None:
            data.write(Int.getvalue(cls.pinned_msg_id))
        
        if cls.stickerset is not None:
            data.write(cls.stickerset.getvalue())
        
        if cls.available_min_id is not None:
            data.write(Int.getvalue(cls.available_min_id))
        
        if cls.folder_id is not None:
            data.write(Int.getvalue(cls.folder_id))
        
        if cls.linked_chat_id is not None:
            data.write(Int.getvalue(cls.linked_chat_id))
        
        if cls.location is not None:
            data.write(cls.location.getvalue())
        
        if cls.slowmode_seconds is not None:
            data.write(Int.getvalue(cls.slowmode_seconds))
        
        if cls.slowmode_next_send_date is not None:
            data.write(Int.getvalue(cls.slowmode_next_send_date))
        
        if cls.stats_dc is not None:
            data.write(Int.getvalue(cls.stats_dc))
        data.write(Int.getvalue(cls.pts))
        
        if cls.call is not None:
            data.write(cls.call.getvalue())
        
        if cls.ttl_period is not None:
            data.write(Int.getvalue(cls.ttl_period))
        
        if cls.pending_suggestions is not None:
            data.write(Vector().getvalue(cls.pending_suggestions, String))
        return data.getvalue()


class ChatParticipant(TL):
    ID = 0xc8d7493e

    def __init__(cls, user_id: int, inviter_id: int, date: int):
        cls.user_id = user_id
        cls.inviter_id = inviter_id
        cls.date = date

    @staticmethod
    def read(data) -> "ChatParticipant":
        user_id = Int.read(data)
        inviter_id = Int.read(data)
        date = Int.read(data)
        return ChatParticipant(user_id=user_id, inviter_id=inviter_id, date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Int.getvalue(cls.inviter_id))
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class ChatParticipantCreator(TL):
    ID = 0xda13538a

    def __init__(cls, user_id: int):
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "ChatParticipantCreator":
        user_id = Int.read(data)
        return ChatParticipantCreator(user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        return data.getvalue()


class ChatParticipantAdmin(TL):
    ID = 0xe2d6e436

    def __init__(cls, user_id: int, inviter_id: int, date: int):
        cls.user_id = user_id
        cls.inviter_id = inviter_id
        cls.date = date

    @staticmethod
    def read(data) -> "ChatParticipantAdmin":
        user_id = Int.read(data)
        inviter_id = Int.read(data)
        date = Int.read(data)
        return ChatParticipantAdmin(user_id=user_id, inviter_id=inviter_id, date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Int.getvalue(cls.inviter_id))
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class ChatParticipantsForbidden(TL):
    ID = 0xfc900c2b

    def __init__(cls, chat_id: int, self_participant: TL = None):
        cls.chat_id = chat_id
        cls.self_participant = self_participant

    @staticmethod
    def read(data) -> "ChatParticipantsForbidden":
        flags = Int.read(data)
        chat_id = Int.read(data)
        self_participant = data.getobj() if flags & 1 else None
        return ChatParticipantsForbidden(chat_id=chat_id, self_participant=self_participant)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.self_participant is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.chat_id))
        
        if cls.self_participant is not None:
            data.write(cls.self_participant.getvalue())
        return data.getvalue()


class ChatParticipants(TL):
    ID = 0x3f460fed

    def __init__(cls, chat_id: int, participants: List[TL], version: int):
        cls.chat_id = chat_id
        cls.participants = participants
        cls.version = version

    @staticmethod
    def read(data) -> "ChatParticipants":
        chat_id = Int.read(data)
        participants = data.getobj()
        version = Int.read(data)
        return ChatParticipants(chat_id=chat_id, participants=participants, version=version)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        data.write(Vector().getvalue(cls.participants))
        data.write(Int.getvalue(cls.version))
        return data.getvalue()


class ChatPhotoEmpty(TL):
    ID = 0x37c1011c

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ChatPhotoEmpty":
        
        return ChatPhotoEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ChatPhoto(TL):
    ID = 0xd20b9f3c

    def __init__(cls, photo_small: TL, photo_big: TL, dc_id: int, has_video: bool = None):
        cls.has_video = has_video
        cls.photo_small = photo_small
        cls.photo_big = photo_big
        cls.dc_id = dc_id

    @staticmethod
    def read(data) -> "ChatPhoto":
        flags = Int.read(data)
        has_video = True if flags & 1 else False
        photo_small = data.getobj()
        photo_big = data.getobj()
        dc_id = Int.read(data)
        return ChatPhoto(has_video=has_video, photo_small=photo_small, photo_big=photo_big, dc_id=dc_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.has_video is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.photo_small.getvalue())
        data.write(cls.photo_big.getvalue())
        data.write(Int.getvalue(cls.dc_id))
        return data.getvalue()


class MessageEmpty(TL):
    ID = 0x90a6ca84

    def __init__(cls, id: int, peer_id: TL = None):
        cls.id = id
        cls.peer_id = peer_id

    @staticmethod
    def read(data) -> "MessageEmpty":
        flags = Int.read(data)
        id = Int.read(data)
        peer_id = data.getobj() if flags & 1 else None
        return MessageEmpty(id=id, peer_id=peer_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.peer_id is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        
        if cls.peer_id is not None:
            data.write(cls.peer_id.getvalue())
        return data.getvalue()


class Message(TL):
    ID = 0xbce383d2

    def __init__(cls, id: int, peer_id: TL, date: int, message: str, out: bool = None, mentioned: bool = None, media_unread: bool = None, silent: bool = None, post: bool = None, from_scheduled: bool = None, legacy: bool = None, edit_hide: bool = None, pinned: bool = None, from_id: TL = None, fwd_from: TL = None, via_bot_id: int = None, reply_to: TL = None, media: TL = None, reply_markup: TL = None, entities: List[TL] = None, views: int = None, forwards: int = None, replies: TL = None, edit_date: int = None, post_author: str = None, grouped_id: int = None, restriction_reason: List[TL] = None, ttl_period: int = None):
        cls.out = out
        cls.mentioned = mentioned
        cls.media_unread = media_unread
        cls.silent = silent
        cls.post = post
        cls.from_scheduled = from_scheduled
        cls.legacy = legacy
        cls.edit_hide = edit_hide
        cls.pinned = pinned
        cls.id = id
        cls.from_id = from_id
        cls.peer_id = peer_id
        cls.fwd_from = fwd_from
        cls.via_bot_id = via_bot_id
        cls.reply_to = reply_to
        cls.date = date
        cls.message = message
        cls.media = media
        cls.reply_markup = reply_markup
        cls.entities = entities
        cls.views = views
        cls.forwards = forwards
        cls.replies = replies
        cls.edit_date = edit_date
        cls.post_author = post_author
        cls.grouped_id = grouped_id
        cls.restriction_reason = restriction_reason
        cls.ttl_period = ttl_period

    @staticmethod
    def read(data) -> "Message":
        flags = Int.read(data)
        out = True if flags & 2 else False
        mentioned = True if flags & 16 else False
        media_unread = True if flags & 32 else False
        silent = True if flags & 8192 else False
        post = True if flags & 16384 else False
        from_scheduled = True if flags & 262144 else False
        legacy = True if flags & 524288 else False
        edit_hide = True if flags & 2097152 else False
        pinned = True if flags & 16777216 else False
        id = Int.read(data)
        from_id = data.getobj() if flags & 256 else None
        peer_id = data.getobj()
        fwd_from = data.getobj() if flags & 4 else None
        via_bot_id = Int.read(data) if flags & 2048 else None
        reply_to = data.getobj() if flags & 8 else None
        date = Int.read(data)
        message = String.read(data)
        media = data.getobj() if flags & 512 else None
        reply_markup = data.getobj() if flags & 64 else None
        entities = data.getobj() if flags & 128 else []
        views = Int.read(data) if flags & 1024 else None
        forwards = Int.read(data) if flags & 1024 else None
        replies = data.getobj() if flags & 8388608 else None
        edit_date = Int.read(data) if flags & 32768 else None
        post_author = String.read(data) if flags & 65536 else None
        grouped_id = Long.read(data) if flags & 131072 else None
        restriction_reason = data.getobj() if flags & 4194304 else []
        ttl_period = Int.read(data) if flags & 33554432 else None
        return Message(out=out, mentioned=mentioned, media_unread=media_unread, silent=silent, post=post, from_scheduled=from_scheduled, legacy=legacy, edit_hide=edit_hide, pinned=pinned, id=id, from_id=from_id, peer_id=peer_id, fwd_from=fwd_from, via_bot_id=via_bot_id, reply_to=reply_to, date=date, message=message, media=media, reply_markup=reply_markup, entities=entities, views=views, forwards=forwards, replies=replies, edit_date=edit_date, post_author=post_author, grouped_id=grouped_id, restriction_reason=restriction_reason, ttl_period=ttl_period)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.out is not None else 0
        flags |= 16 if cls.mentioned is not None else 0
        flags |= 32 if cls.media_unread is not None else 0
        flags |= 8192 if cls.silent is not None else 0
        flags |= 16384 if cls.post is not None else 0
        flags |= 262144 if cls.from_scheduled is not None else 0
        flags |= 524288 if cls.legacy is not None else 0
        flags |= 2097152 if cls.edit_hide is not None else 0
        flags |= 16777216 if cls.pinned is not None else 0
        flags |= 256 if cls.from_id is not None else 0
        flags |= 4 if cls.fwd_from is not None else 0
        flags |= 2048 if cls.via_bot_id is not None else 0
        flags |= 8 if cls.reply_to is not None else 0
        flags |= 512 if cls.media is not None else 0
        flags |= 64 if cls.reply_markup is not None else 0
        flags |= 128 if cls.entities is not None else 0
        flags |= 1024 if cls.views is not None else 0
        flags |= 1024 if cls.forwards is not None else 0
        flags |= 8388608 if cls.replies is not None else 0
        flags |= 32768 if cls.edit_date is not None else 0
        flags |= 65536 if cls.post_author is not None else 0
        flags |= 131072 if cls.grouped_id is not None else 0
        flags |= 4194304 if cls.restriction_reason is not None else 0
        flags |= 33554432 if cls.ttl_period is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        
        if cls.from_id is not None:
            data.write(cls.from_id.getvalue())
        data.write(cls.peer_id.getvalue())
        
        if cls.fwd_from is not None:
            data.write(cls.fwd_from.getvalue())
        
        if cls.via_bot_id is not None:
            data.write(Int.getvalue(cls.via_bot_id))
        
        if cls.reply_to is not None:
            data.write(cls.reply_to.getvalue())
        data.write(Int.getvalue(cls.date))
        data.write(String.getvalue(cls.message))
        
        if cls.media is not None:
            data.write(cls.media.getvalue())
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        
        if cls.views is not None:
            data.write(Int.getvalue(cls.views))
        
        if cls.forwards is not None:
            data.write(Int.getvalue(cls.forwards))
        
        if cls.replies is not None:
            data.write(cls.replies.getvalue())
        
        if cls.edit_date is not None:
            data.write(Int.getvalue(cls.edit_date))
        
        if cls.post_author is not None:
            data.write(String.getvalue(cls.post_author))
        
        if cls.grouped_id is not None:
            data.write(Long.getvalue(cls.grouped_id))
        
        if cls.restriction_reason is not None:
            data.write(Vector().getvalue(cls.restriction_reason))
        
        if cls.ttl_period is not None:
            data.write(Int.getvalue(cls.ttl_period))
        return data.getvalue()


class MessageService(TL):
    ID = 0x2b085862

    def __init__(cls, id: int, peer_id: TL, date: int, action: TL, out: bool = None, mentioned: bool = None, media_unread: bool = None, silent: bool = None, post: bool = None, legacy: bool = None, from_id: TL = None, reply_to: TL = None, ttl_period: int = None):
        cls.out = out
        cls.mentioned = mentioned
        cls.media_unread = media_unread
        cls.silent = silent
        cls.post = post
        cls.legacy = legacy
        cls.id = id
        cls.from_id = from_id
        cls.peer_id = peer_id
        cls.reply_to = reply_to
        cls.date = date
        cls.action = action
        cls.ttl_period = ttl_period

    @staticmethod
    def read(data) -> "MessageService":
        flags = Int.read(data)
        out = True if flags & 2 else False
        mentioned = True if flags & 16 else False
        media_unread = True if flags & 32 else False
        silent = True if flags & 8192 else False
        post = True if flags & 16384 else False
        legacy = True if flags & 524288 else False
        id = Int.read(data)
        from_id = data.getobj() if flags & 256 else None
        peer_id = data.getobj()
        reply_to = data.getobj() if flags & 8 else None
        date = Int.read(data)
        action = data.getobj()
        ttl_period = Int.read(data) if flags & 33554432 else None
        return MessageService(out=out, mentioned=mentioned, media_unread=media_unread, silent=silent, post=post, legacy=legacy, id=id, from_id=from_id, peer_id=peer_id, reply_to=reply_to, date=date, action=action, ttl_period=ttl_period)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.out is not None else 0
        flags |= 16 if cls.mentioned is not None else 0
        flags |= 32 if cls.media_unread is not None else 0
        flags |= 8192 if cls.silent is not None else 0
        flags |= 16384 if cls.post is not None else 0
        flags |= 524288 if cls.legacy is not None else 0
        flags |= 256 if cls.from_id is not None else 0
        flags |= 8 if cls.reply_to is not None else 0
        flags |= 33554432 if cls.ttl_period is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        
        if cls.from_id is not None:
            data.write(cls.from_id.getvalue())
        data.write(cls.peer_id.getvalue())
        
        if cls.reply_to is not None:
            data.write(cls.reply_to.getvalue())
        data.write(Int.getvalue(cls.date))
        data.write(cls.action.getvalue())
        
        if cls.ttl_period is not None:
            data.write(Int.getvalue(cls.ttl_period))
        return data.getvalue()


class MessageMediaEmpty(TL):
    ID = 0x3ded6320

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "MessageMediaEmpty":
        
        return MessageMediaEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class MessageMediaPhoto(TL):
    ID = 0x695150d7

    def __init__(cls, photo: TL = None, ttl_seconds: int = None):
        cls.photo = photo
        cls.ttl_seconds = ttl_seconds

    @staticmethod
    def read(data) -> "MessageMediaPhoto":
        flags = Int.read(data)
        photo = data.getobj() if flags & 1 else None
        ttl_seconds = Int.read(data) if flags & 4 else None
        return MessageMediaPhoto(photo=photo, ttl_seconds=ttl_seconds)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.photo is not None else 0
        flags |= 4 if cls.ttl_seconds is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.photo is not None:
            data.write(cls.photo.getvalue())
        
        if cls.ttl_seconds is not None:
            data.write(Int.getvalue(cls.ttl_seconds))
        return data.getvalue()


class MessageMediaGeo(TL):
    ID = 0x56e0d474

    def __init__(cls, geo: TL):
        cls.geo = geo

    @staticmethod
    def read(data) -> "MessageMediaGeo":
        geo = data.getobj()
        return MessageMediaGeo(geo=geo)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.geo.getvalue())
        return data.getvalue()


class MessageMediaContact(TL):
    ID = 0xcbf24940

    def __init__(cls, phone_number: str, first_name: str, last_name: str, vcard: str, user_id: int):
        cls.phone_number = phone_number
        cls.first_name = first_name
        cls.last_name = last_name
        cls.vcard = vcard
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "MessageMediaContact":
        phone_number = String.read(data)
        first_name = String.read(data)
        last_name = String.read(data)
        vcard = String.read(data)
        user_id = Int.read(data)
        return MessageMediaContact(phone_number=phone_number, first_name=first_name, last_name=last_name, vcard=vcard, user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone_number))
        data.write(String.getvalue(cls.first_name))
        data.write(String.getvalue(cls.last_name))
        data.write(String.getvalue(cls.vcard))
        data.write(Int.getvalue(cls.user_id))
        return data.getvalue()


class MessageMediaUnsupported(TL):
    ID = 0x9f84f49e

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "MessageMediaUnsupported":
        
        return MessageMediaUnsupported()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class MessageMediaDocument(TL):
    ID = 0x9cb070d7

    def __init__(cls, document: TL = None, ttl_seconds: int = None):
        cls.document = document
        cls.ttl_seconds = ttl_seconds

    @staticmethod
    def read(data) -> "MessageMediaDocument":
        flags = Int.read(data)
        document = data.getobj() if flags & 1 else None
        ttl_seconds = Int.read(data) if flags & 4 else None
        return MessageMediaDocument(document=document, ttl_seconds=ttl_seconds)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.document is not None else 0
        flags |= 4 if cls.ttl_seconds is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.document is not None:
            data.write(cls.document.getvalue())
        
        if cls.ttl_seconds is not None:
            data.write(Int.getvalue(cls.ttl_seconds))
        return data.getvalue()


class MessageMediaWebPage(TL):
    ID = 0xa32dd600

    def __init__(cls, webpage: TL):
        cls.webpage = webpage

    @staticmethod
    def read(data) -> "MessageMediaWebPage":
        webpage = data.getobj()
        return MessageMediaWebPage(webpage=webpage)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.webpage.getvalue())
        return data.getvalue()


class MessageMediaVenue(TL):
    ID = 0x2ec0533f

    def __init__(cls, geo: TL, title: str, address: str, provider: str, venue_id: str, venue_type: str):
        cls.geo = geo
        cls.title = title
        cls.address = address
        cls.provider = provider
        cls.venue_id = venue_id
        cls.venue_type = venue_type

    @staticmethod
    def read(data) -> "MessageMediaVenue":
        geo = data.getobj()
        title = String.read(data)
        address = String.read(data)
        provider = String.read(data)
        venue_id = String.read(data)
        venue_type = String.read(data)
        return MessageMediaVenue(geo=geo, title=title, address=address, provider=provider, venue_id=venue_id, venue_type=venue_type)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.geo.getvalue())
        data.write(String.getvalue(cls.title))
        data.write(String.getvalue(cls.address))
        data.write(String.getvalue(cls.provider))
        data.write(String.getvalue(cls.venue_id))
        data.write(String.getvalue(cls.venue_type))
        return data.getvalue()


class MessageMediaGame(TL):
    ID = 0xfdb19008

    def __init__(cls, game: TL):
        cls.game = game

    @staticmethod
    def read(data) -> "MessageMediaGame":
        game = data.getobj()
        return MessageMediaGame(game=game)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.game.getvalue())
        return data.getvalue()


class MessageMediaInvoice(TL):
    ID = 0x84551347

    def __init__(cls, title: str, description: str, currency: str, total_amount: int, start_param: str, shipping_address_requested: bool = None, test: bool = None, photo: TL = None, receipt_msg_id: int = None):
        cls.shipping_address_requested = shipping_address_requested
        cls.test = test
        cls.title = title
        cls.description = description
        cls.photo = photo
        cls.receipt_msg_id = receipt_msg_id
        cls.currency = currency
        cls.total_amount = total_amount
        cls.start_param = start_param

    @staticmethod
    def read(data) -> "MessageMediaInvoice":
        flags = Int.read(data)
        shipping_address_requested = True if flags & 2 else False
        test = True if flags & 8 else False
        title = String.read(data)
        description = String.read(data)
        photo = data.getobj() if flags & 1 else None
        receipt_msg_id = Int.read(data) if flags & 4 else None
        currency = String.read(data)
        total_amount = Long.read(data)
        start_param = String.read(data)
        return MessageMediaInvoice(shipping_address_requested=shipping_address_requested, test=test, title=title, description=description, photo=photo, receipt_msg_id=receipt_msg_id, currency=currency, total_amount=total_amount, start_param=start_param)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.shipping_address_requested is not None else 0
        flags |= 8 if cls.test is not None else 0
        flags |= 1 if cls.photo is not None else 0
        flags |= 4 if cls.receipt_msg_id is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.title))
        data.write(String.getvalue(cls.description))
        
        if cls.photo is not None:
            data.write(cls.photo.getvalue())
        
        if cls.receipt_msg_id is not None:
            data.write(Int.getvalue(cls.receipt_msg_id))
        data.write(String.getvalue(cls.currency))
        data.write(Long.getvalue(cls.total_amount))
        data.write(String.getvalue(cls.start_param))
        return data.getvalue()


class MessageMediaGeoLive(TL):
    ID = 0xb940c666

    def __init__(cls, geo: TL, period: int, heading: int = None, proximity_notification_radius: int = None):
        cls.geo = geo
        cls.heading = heading
        cls.period = period
        cls.proximity_notification_radius = proximity_notification_radius

    @staticmethod
    def read(data) -> "MessageMediaGeoLive":
        flags = Int.read(data)
        geo = data.getobj()
        heading = Int.read(data) if flags & 1 else None
        period = Int.read(data)
        proximity_notification_radius = Int.read(data) if flags & 2 else None
        return MessageMediaGeoLive(geo=geo, heading=heading, period=period, proximity_notification_radius=proximity_notification_radius)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.heading is not None else 0
        flags |= 2 if cls.proximity_notification_radius is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.geo.getvalue())
        
        if cls.heading is not None:
            data.write(Int.getvalue(cls.heading))
        data.write(Int.getvalue(cls.period))
        
        if cls.proximity_notification_radius is not None:
            data.write(Int.getvalue(cls.proximity_notification_radius))
        return data.getvalue()


class MessageMediaPoll(TL):
    ID = 0x4bd6e798

    def __init__(cls, poll: TL, results: TL):
        cls.poll = poll
        cls.results = results

    @staticmethod
    def read(data) -> "MessageMediaPoll":
        poll = data.getobj()
        results = data.getobj()
        return MessageMediaPoll(poll=poll, results=results)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.poll.getvalue())
        data.write(cls.results.getvalue())
        return data.getvalue()


class MessageMediaDice(TL):
    ID = 0x3f7ee58b

    def __init__(cls, value: int, emoticon: str):
        cls.value = value
        cls.emoticon = emoticon

    @staticmethod
    def read(data) -> "MessageMediaDice":
        value = Int.read(data)
        emoticon = String.read(data)
        return MessageMediaDice(value=value, emoticon=emoticon)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.value))
        data.write(String.getvalue(cls.emoticon))
        return data.getvalue()


class MessageActionEmpty(TL):
    ID = 0xb6aef7b0

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "MessageActionEmpty":
        
        return MessageActionEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class MessageActionChatCreate(TL):
    ID = 0xa6638b9a

    def __init__(cls, title: str, users: List[int]):
        cls.title = title
        cls.users = users

    @staticmethod
    def read(data) -> "MessageActionChatCreate":
        title = String.read(data)
        users = data.getobj(Int)
        return MessageActionChatCreate(title=title, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.title))
        data.write(Vector().getvalue(cls.users, Int))
        return data.getvalue()


class MessageActionChatEditTitle(TL):
    ID = 0xb5a1ce5a

    def __init__(cls, title: str):
        cls.title = title

    @staticmethod
    def read(data) -> "MessageActionChatEditTitle":
        title = String.read(data)
        return MessageActionChatEditTitle(title=title)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.title))
        return data.getvalue()


class MessageActionChatEditPhoto(TL):
    ID = 0x7fcb13a8

    def __init__(cls, photo: TL):
        cls.photo = photo

    @staticmethod
    def read(data) -> "MessageActionChatEditPhoto":
        photo = data.getobj()
        return MessageActionChatEditPhoto(photo=photo)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.photo.getvalue())
        return data.getvalue()


class MessageActionChatDeletePhoto(TL):
    ID = 0x95e3fbef

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "MessageActionChatDeletePhoto":
        
        return MessageActionChatDeletePhoto()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class MessageActionChatAddUser(TL):
    ID = 0x488a7337

    def __init__(cls, users: List[int]):
        cls.users = users

    @staticmethod
    def read(data) -> "MessageActionChatAddUser":
        users = data.getobj(Int)
        return MessageActionChatAddUser(users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.users, Int))
        return data.getvalue()


class MessageActionChatDeleteUser(TL):
    ID = 0xb2ae9b0c

    def __init__(cls, user_id: int):
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "MessageActionChatDeleteUser":
        user_id = Int.read(data)
        return MessageActionChatDeleteUser(user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        return data.getvalue()


class MessageActionChatJoinedByLink(TL):
    ID = 0xf89cf5e8

    def __init__(cls, inviter_id: int):
        cls.inviter_id = inviter_id

    @staticmethod
    def read(data) -> "MessageActionChatJoinedByLink":
        inviter_id = Int.read(data)
        return MessageActionChatJoinedByLink(inviter_id=inviter_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.inviter_id))
        return data.getvalue()


class MessageActionChannelCreate(TL):
    ID = 0x95d2ac92

    def __init__(cls, title: str):
        cls.title = title

    @staticmethod
    def read(data) -> "MessageActionChannelCreate":
        title = String.read(data)
        return MessageActionChannelCreate(title=title)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.title))
        return data.getvalue()


class MessageActionChatMigrateTo(TL):
    ID = 0x51bdb021

    def __init__(cls, channel_id: int):
        cls.channel_id = channel_id

    @staticmethod
    def read(data) -> "MessageActionChatMigrateTo":
        channel_id = Int.read(data)
        return MessageActionChatMigrateTo(channel_id=channel_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.channel_id))
        return data.getvalue()


class MessageActionChannelMigrateFrom(TL):
    ID = 0xb055eaee

    def __init__(cls, title: str, chat_id: int):
        cls.title = title
        cls.chat_id = chat_id

    @staticmethod
    def read(data) -> "MessageActionChannelMigrateFrom":
        title = String.read(data)
        chat_id = Int.read(data)
        return MessageActionChannelMigrateFrom(title=title, chat_id=chat_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.title))
        data.write(Int.getvalue(cls.chat_id))
        return data.getvalue()


class MessageActionPinMessage(TL):
    ID = 0x94bd38ed

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "MessageActionPinMessage":
        
        return MessageActionPinMessage()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class MessageActionHistoryClear(TL):
    ID = 0x9fbab604

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "MessageActionHistoryClear":
        
        return MessageActionHistoryClear()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class MessageActionGameScore(TL):
    ID = 0x92a72876

    def __init__(cls, game_id: int, score: int):
        cls.game_id = game_id
        cls.score = score

    @staticmethod
    def read(data) -> "MessageActionGameScore":
        game_id = Long.read(data)
        score = Int.read(data)
        return MessageActionGameScore(game_id=game_id, score=score)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.game_id))
        data.write(Int.getvalue(cls.score))
        return data.getvalue()


class MessageActionPaymentSentMe(TL):
    ID = 0x8f31b327

    def __init__(cls, currency: str, total_amount: int, payload: bytes, charge: TL, info: TL = None, shipping_option_id: str = None):
        cls.currency = currency
        cls.total_amount = total_amount
        cls.payload = payload
        cls.info = info
        cls.shipping_option_id = shipping_option_id
        cls.charge = charge

    @staticmethod
    def read(data) -> "MessageActionPaymentSentMe":
        flags = Int.read(data)
        currency = String.read(data)
        total_amount = Long.read(data)
        payload = Bytes.read(data)
        info = data.getobj() if flags & 1 else None
        shipping_option_id = String.read(data) if flags & 2 else None
        charge = data.getobj()
        return MessageActionPaymentSentMe(currency=currency, total_amount=total_amount, payload=payload, info=info, shipping_option_id=shipping_option_id, charge=charge)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.info is not None else 0
        flags |= 2 if cls.shipping_option_id is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.currency))
        data.write(Long.getvalue(cls.total_amount))
        data.write(Bytes.getvalue(cls.payload))
        
        if cls.info is not None:
            data.write(cls.info.getvalue())
        
        if cls.shipping_option_id is not None:
            data.write(String.getvalue(cls.shipping_option_id))
        data.write(cls.charge.getvalue())
        return data.getvalue()


class MessageActionPaymentSent(TL):
    ID = 0x40699cd0

    def __init__(cls, currency: str, total_amount: int):
        cls.currency = currency
        cls.total_amount = total_amount

    @staticmethod
    def read(data) -> "MessageActionPaymentSent":
        currency = String.read(data)
        total_amount = Long.read(data)
        return MessageActionPaymentSent(currency=currency, total_amount=total_amount)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.currency))
        data.write(Long.getvalue(cls.total_amount))
        return data.getvalue()


class MessageActionPhoneCall(TL):
    ID = 0x80e11a7f

    def __init__(cls, call_id: int, video: bool = None, reason: TL = None, duration: int = None):
        cls.video = video
        cls.call_id = call_id
        cls.reason = reason
        cls.duration = duration

    @staticmethod
    def read(data) -> "MessageActionPhoneCall":
        flags = Int.read(data)
        video = True if flags & 4 else False
        call_id = Long.read(data)
        reason = data.getobj() if flags & 1 else None
        duration = Int.read(data) if flags & 2 else None
        return MessageActionPhoneCall(video=video, call_id=call_id, reason=reason, duration=duration)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 4 if cls.video is not None else 0
        flags |= 1 if cls.reason is not None else 0
        flags |= 2 if cls.duration is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.call_id))
        
        if cls.reason is not None:
            data.write(cls.reason.getvalue())
        
        if cls.duration is not None:
            data.write(Int.getvalue(cls.duration))
        return data.getvalue()


class MessageActionScreenshotTaken(TL):
    ID = 0x4792929b

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "MessageActionScreenshotTaken":
        
        return MessageActionScreenshotTaken()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class MessageActionCustomAction(TL):
    ID = 0xfae69f56

    def __init__(cls, message: str):
        cls.message = message

    @staticmethod
    def read(data) -> "MessageActionCustomAction":
        message = String.read(data)
        return MessageActionCustomAction(message=message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.message))
        return data.getvalue()


class MessageActionBotAllowed(TL):
    ID = 0xabe9affe

    def __init__(cls, domain: str):
        cls.domain = domain

    @staticmethod
    def read(data) -> "MessageActionBotAllowed":
        domain = String.read(data)
        return MessageActionBotAllowed(domain=domain)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.domain))
        return data.getvalue()


class MessageActionSecureValuesSentMe(TL):
    ID = 0x1b287353

    def __init__(cls, values: List[TL], credentials: TL):
        cls.values = values
        cls.credentials = credentials

    @staticmethod
    def read(data) -> "MessageActionSecureValuesSentMe":
        values = data.getobj()
        credentials = data.getobj()
        return MessageActionSecureValuesSentMe(values=values, credentials=credentials)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.values))
        data.write(cls.credentials.getvalue())
        return data.getvalue()


class MessageActionSecureValuesSent(TL):
    ID = 0xd95c6154

    def __init__(cls, types: List[TL]):
        cls.types = types

    @staticmethod
    def read(data) -> "MessageActionSecureValuesSent":
        types = data.getobj()
        return MessageActionSecureValuesSent(types=types)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.types))
        return data.getvalue()


class MessageActionContactSignUp(TL):
    ID = 0xf3f25f76

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "MessageActionContactSignUp":
        
        return MessageActionContactSignUp()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class MessageActionGeoProximityReached(TL):
    ID = 0x98e0d697

    def __init__(cls, from_id: TL, to_id: TL, distance: int):
        cls.from_id = from_id
        cls.to_id = to_id
        cls.distance = distance

    @staticmethod
    def read(data) -> "MessageActionGeoProximityReached":
        from_id = data.getobj()
        to_id = data.getobj()
        distance = Int.read(data)
        return MessageActionGeoProximityReached(from_id=from_id, to_id=to_id, distance=distance)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.from_id.getvalue())
        data.write(cls.to_id.getvalue())
        data.write(Int.getvalue(cls.distance))
        return data.getvalue()


class MessageActionGroupCall(TL):
    ID = 0x7a0d7f42

    def __init__(cls, call: TL, duration: int = None):
        cls.call = call
        cls.duration = duration

    @staticmethod
    def read(data) -> "MessageActionGroupCall":
        flags = Int.read(data)
        call = data.getobj()
        duration = Int.read(data) if flags & 1 else None
        return MessageActionGroupCall(call=call, duration=duration)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.duration is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.call.getvalue())
        
        if cls.duration is not None:
            data.write(Int.getvalue(cls.duration))
        return data.getvalue()


class MessageActionInviteToGroupCall(TL):
    ID = 0x76b9f11a

    def __init__(cls, call: TL, users: List[int]):
        cls.call = call
        cls.users = users

    @staticmethod
    def read(data) -> "MessageActionInviteToGroupCall":
        call = data.getobj()
        users = data.getobj(Int)
        return MessageActionInviteToGroupCall(call=call, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.call.getvalue())
        data.write(Vector().getvalue(cls.users, Int))
        return data.getvalue()


class MessageActionSetMessagesTTL(TL):
    ID = 0xaa1afbfd

    def __init__(cls, period: int):
        cls.period = period

    @staticmethod
    def read(data) -> "MessageActionSetMessagesTTL":
        period = Int.read(data)
        return MessageActionSetMessagesTTL(period=period)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.period))
        return data.getvalue()


class Dialog(TL):
    ID = 0x2c171f72

    def __init__(cls, peer: TL, top_message: int, read_inbox_max_id: int, read_outbox_max_id: int, unread_count: int, unread_mentions_count: int, notify_settings: TL, pinned: bool = None, unread_mark: bool = None, pts: int = None, draft: TL = None, folder_id: int = None):
        cls.pinned = pinned
        cls.unread_mark = unread_mark
        cls.peer = peer
        cls.top_message = top_message
        cls.read_inbox_max_id = read_inbox_max_id
        cls.read_outbox_max_id = read_outbox_max_id
        cls.unread_count = unread_count
        cls.unread_mentions_count = unread_mentions_count
        cls.notify_settings = notify_settings
        cls.pts = pts
        cls.draft = draft
        cls.folder_id = folder_id

    @staticmethod
    def read(data) -> "Dialog":
        flags = Int.read(data)
        pinned = True if flags & 4 else False
        unread_mark = True if flags & 8 else False
        peer = data.getobj()
        top_message = Int.read(data)
        read_inbox_max_id = Int.read(data)
        read_outbox_max_id = Int.read(data)
        unread_count = Int.read(data)
        unread_mentions_count = Int.read(data)
        notify_settings = data.getobj()
        pts = Int.read(data) if flags & 1 else None
        draft = data.getobj() if flags & 2 else None
        folder_id = Int.read(data) if flags & 16 else None
        return Dialog(pinned=pinned, unread_mark=unread_mark, peer=peer, top_message=top_message, read_inbox_max_id=read_inbox_max_id, read_outbox_max_id=read_outbox_max_id, unread_count=unread_count, unread_mentions_count=unread_mentions_count, notify_settings=notify_settings, pts=pts, draft=draft, folder_id=folder_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 4 if cls.pinned is not None else 0
        flags |= 8 if cls.unread_mark is not None else 0
        flags |= 1 if cls.pts is not None else 0
        flags |= 2 if cls.draft is not None else 0
        flags |= 16 if cls.folder_id is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.top_message))
        data.write(Int.getvalue(cls.read_inbox_max_id))
        data.write(Int.getvalue(cls.read_outbox_max_id))
        data.write(Int.getvalue(cls.unread_count))
        data.write(Int.getvalue(cls.unread_mentions_count))
        data.write(cls.notify_settings.getvalue())
        
        if cls.pts is not None:
            data.write(Int.getvalue(cls.pts))
        
        if cls.draft is not None:
            data.write(cls.draft.getvalue())
        
        if cls.folder_id is not None:
            data.write(Int.getvalue(cls.folder_id))
        return data.getvalue()


class DialogFolder(TL):
    ID = 0x71bd134c

    def __init__(cls, folder: TL, peer: TL, top_message: int, unread_muted_peers_count: int, unread_unmuted_peers_count: int, unread_muted_messages_count: int, unread_unmuted_messages_count: int, pinned: bool = None):
        cls.pinned = pinned
        cls.folder = folder
        cls.peer = peer
        cls.top_message = top_message
        cls.unread_muted_peers_count = unread_muted_peers_count
        cls.unread_unmuted_peers_count = unread_unmuted_peers_count
        cls.unread_muted_messages_count = unread_muted_messages_count
        cls.unread_unmuted_messages_count = unread_unmuted_messages_count

    @staticmethod
    def read(data) -> "DialogFolder":
        flags = Int.read(data)
        pinned = True if flags & 4 else False
        folder = data.getobj()
        peer = data.getobj()
        top_message = Int.read(data)
        unread_muted_peers_count = Int.read(data)
        unread_unmuted_peers_count = Int.read(data)
        unread_muted_messages_count = Int.read(data)
        unread_unmuted_messages_count = Int.read(data)
        return DialogFolder(pinned=pinned, folder=folder, peer=peer, top_message=top_message, unread_muted_peers_count=unread_muted_peers_count, unread_unmuted_peers_count=unread_unmuted_peers_count, unread_muted_messages_count=unread_muted_messages_count, unread_unmuted_messages_count=unread_unmuted_messages_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 4 if cls.pinned is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.folder.getvalue())
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.top_message))
        data.write(Int.getvalue(cls.unread_muted_peers_count))
        data.write(Int.getvalue(cls.unread_unmuted_peers_count))
        data.write(Int.getvalue(cls.unread_muted_messages_count))
        data.write(Int.getvalue(cls.unread_unmuted_messages_count))
        return data.getvalue()


class PhotoEmpty(TL):
    ID = 0x2331b22d

    def __init__(cls, id: int):
        cls.id = id

    @staticmethod
    def read(data) -> "PhotoEmpty":
        id = Long.read(data)
        return PhotoEmpty(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        return data.getvalue()


class Photo(TL):
    ID = 0xfb197a65

    def __init__(cls, id: int, access_hash: int, file_reference: bytes, date: int, sizes: List[TL], dc_id: int, has_stickers: bool = None, video_sizes: List[TL] = None):
        cls.has_stickers = has_stickers
        cls.id = id
        cls.access_hash = access_hash
        cls.file_reference = file_reference
        cls.date = date
        cls.sizes = sizes
        cls.video_sizes = video_sizes
        cls.dc_id = dc_id

    @staticmethod
    def read(data) -> "Photo":
        flags = Int.read(data)
        has_stickers = True if flags & 1 else False
        id = Long.read(data)
        access_hash = Long.read(data)
        file_reference = Bytes.read(data)
        date = Int.read(data)
        sizes = data.getobj()
        video_sizes = data.getobj() if flags & 2 else []
        dc_id = Int.read(data)
        return Photo(has_stickers=has_stickers, id=id, access_hash=access_hash, file_reference=file_reference, date=date, sizes=sizes, video_sizes=video_sizes, dc_id=dc_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.has_stickers is not None else 0
        flags |= 2 if cls.video_sizes is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Bytes.getvalue(cls.file_reference))
        data.write(Int.getvalue(cls.date))
        data.write(Vector().getvalue(cls.sizes))
        
        if cls.video_sizes is not None:
            data.write(Vector().getvalue(cls.video_sizes))
        data.write(Int.getvalue(cls.dc_id))
        return data.getvalue()


class PhotoSizeEmpty(TL):
    ID = 0xe17e23c

    def __init__(cls, type: str):
        cls.type = type

    @staticmethod
    def read(data) -> "PhotoSizeEmpty":
        type = String.read(data)
        return PhotoSizeEmpty(type=type)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.type))
        return data.getvalue()


class PhotoSize(TL):
    ID = 0x77bfb61b

    def __init__(cls, type: str, location: TL, w: int, h: int, size: int):
        cls.type = type
        cls.location = location
        cls.w = w
        cls.h = h
        cls.size = size

    @staticmethod
    def read(data) -> "PhotoSize":
        type = String.read(data)
        location = data.getobj()
        w = Int.read(data)
        h = Int.read(data)
        size = Int.read(data)
        return PhotoSize(type=type, location=location, w=w, h=h, size=size)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.type))
        data.write(cls.location.getvalue())
        data.write(Int.getvalue(cls.w))
        data.write(Int.getvalue(cls.h))
        data.write(Int.getvalue(cls.size))
        return data.getvalue()


class PhotoCachedSize(TL):
    ID = 0xe9a734fa

    def __init__(cls, type: str, location: TL, w: int, h: int, bytes: bytes):
        cls.type = type
        cls.location = location
        cls.w = w
        cls.h = h
        cls.bytes = bytes

    @staticmethod
    def read(data) -> "PhotoCachedSize":
        type = String.read(data)
        location = data.getobj()
        w = Int.read(data)
        h = Int.read(data)
        bytes = Bytes.read(data)
        return PhotoCachedSize(type=type, location=location, w=w, h=h, bytes=bytes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.type))
        data.write(cls.location.getvalue())
        data.write(Int.getvalue(cls.w))
        data.write(Int.getvalue(cls.h))
        data.write(Bytes.getvalue(cls.bytes))
        return data.getvalue()


class PhotoStrippedSize(TL):
    ID = 0xe0b0bc2e

    def __init__(cls, type: str, bytes: bytes):
        cls.type = type
        cls.bytes = bytes

    @staticmethod
    def read(data) -> "PhotoStrippedSize":
        type = String.read(data)
        bytes = Bytes.read(data)
        return PhotoStrippedSize(type=type, bytes=bytes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.type))
        data.write(Bytes.getvalue(cls.bytes))
        return data.getvalue()


class PhotoSizeProgressive(TL):
    ID = 0x5aa86a51

    def __init__(cls, type: str, location: TL, w: int, h: int, sizes: List[int]):
        cls.type = type
        cls.location = location
        cls.w = w
        cls.h = h
        cls.sizes = sizes

    @staticmethod
    def read(data) -> "PhotoSizeProgressive":
        type = String.read(data)
        location = data.getobj()
        w = Int.read(data)
        h = Int.read(data)
        sizes = data.getobj(Int)
        return PhotoSizeProgressive(type=type, location=location, w=w, h=h, sizes=sizes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.type))
        data.write(cls.location.getvalue())
        data.write(Int.getvalue(cls.w))
        data.write(Int.getvalue(cls.h))
        data.write(Vector().getvalue(cls.sizes, Int))
        return data.getvalue()


class PhotoPathSize(TL):
    ID = 0xd8214d41

    def __init__(cls, type: str, bytes: bytes):
        cls.type = type
        cls.bytes = bytes

    @staticmethod
    def read(data) -> "PhotoPathSize":
        type = String.read(data)
        bytes = Bytes.read(data)
        return PhotoPathSize(type=type, bytes=bytes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.type))
        data.write(Bytes.getvalue(cls.bytes))
        return data.getvalue()


class GeoPointEmpty(TL):
    ID = 0x1117dd5f

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GeoPointEmpty":
        
        return GeoPointEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class GeoPoint(TL):
    ID = 0xb2a2f663

    def __init__(cls, long: float, lat: float, access_hash: int, accuracy_radius: int = None):
        cls.long = long
        cls.lat = lat
        cls.access_hash = access_hash
        cls.accuracy_radius = accuracy_radius

    @staticmethod
    def read(data) -> "GeoPoint":
        flags = Int.read(data)
        long = Double.read(data)
        lat = Double.read(data)
        access_hash = Long.read(data)
        accuracy_radius = Int.read(data) if flags & 1 else None
        return GeoPoint(long=long, lat=lat, access_hash=access_hash, accuracy_radius=accuracy_radius)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.accuracy_radius is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Double.getvalue(cls.long))
        data.write(Double.getvalue(cls.lat))
        data.write(Long.getvalue(cls.access_hash))
        
        if cls.accuracy_radius is not None:
            data.write(Int.getvalue(cls.accuracy_radius))
        return data.getvalue()


class InputNotifyPeer(TL):
    ID = 0xb8bc5b0c

    def __init__(cls, peer: TL):
        cls.peer = peer

    @staticmethod
    def read(data) -> "InputNotifyPeer":
        peer = data.getobj()
        return InputNotifyPeer(peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class InputNotifyUsers(TL):
    ID = 0x193b4417

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputNotifyUsers":
        
        return InputNotifyUsers()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputNotifyChats(TL):
    ID = 0x4a95e84e

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputNotifyChats":
        
        return InputNotifyChats()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputNotifyBroadcasts(TL):
    ID = 0xb1db7c7e

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputNotifyBroadcasts":
        
        return InputNotifyBroadcasts()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPeerNotifySettings(TL):
    ID = 0x9c3d198e

    def __init__(cls, show_previews: bool = None, silent: bool = None, mute_until: int = None, sound: str = None):
        cls.show_previews = show_previews
        cls.silent = silent
        cls.mute_until = mute_until
        cls.sound = sound

    @staticmethod
    def read(data) -> "InputPeerNotifySettings":
        flags = Int.read(data)
        show_previews = Bool.read(data) if flags & 1 else None
        silent = Bool.read(data) if flags & 2 else None
        mute_until = Int.read(data) if flags & 4 else None
        sound = String.read(data) if flags & 8 else None
        return InputPeerNotifySettings(show_previews=show_previews, silent=silent, mute_until=mute_until, sound=sound)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.show_previews is not None else 0
        flags |= 2 if cls.silent is not None else 0
        flags |= 4 if cls.mute_until is not None else 0
        flags |= 8 if cls.sound is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.mute_until is not None:
            data.write(Int.getvalue(cls.mute_until))
        
        if cls.sound is not None:
            data.write(String.getvalue(cls.sound))
        return data.getvalue()


class PeerNotifySettings(TL):
    ID = 0xaf509d20

    def __init__(cls, show_previews: bool = None, silent: bool = None, mute_until: int = None, sound: str = None):
        cls.show_previews = show_previews
        cls.silent = silent
        cls.mute_until = mute_until
        cls.sound = sound

    @staticmethod
    def read(data) -> "PeerNotifySettings":
        flags = Int.read(data)
        show_previews = Bool.read(data) if flags & 1 else None
        silent = Bool.read(data) if flags & 2 else None
        mute_until = Int.read(data) if flags & 4 else None
        sound = String.read(data) if flags & 8 else None
        return PeerNotifySettings(show_previews=show_previews, silent=silent, mute_until=mute_until, sound=sound)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.show_previews is not None else 0
        flags |= 2 if cls.silent is not None else 0
        flags |= 4 if cls.mute_until is not None else 0
        flags |= 8 if cls.sound is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.mute_until is not None:
            data.write(Int.getvalue(cls.mute_until))
        
        if cls.sound is not None:
            data.write(String.getvalue(cls.sound))
        return data.getvalue()


class PeerSettings(TL):
    ID = 0x733f2961

    def __init__(cls, report_spam: bool = None, add_contact: bool = None, block_contact: bool = None, share_contact: bool = None, need_contacts_exception: bool = None, report_geo: bool = None, autoarchived: bool = None, invite_members: bool = None, geo_distance: int = None):
        cls.report_spam = report_spam
        cls.add_contact = add_contact
        cls.block_contact = block_contact
        cls.share_contact = share_contact
        cls.need_contacts_exception = need_contacts_exception
        cls.report_geo = report_geo
        cls.autoarchived = autoarchived
        cls.invite_members = invite_members
        cls.geo_distance = geo_distance

    @staticmethod
    def read(data) -> "PeerSettings":
        flags = Int.read(data)
        report_spam = True if flags & 1 else False
        add_contact = True if flags & 2 else False
        block_contact = True if flags & 4 else False
        share_contact = True if flags & 8 else False
        need_contacts_exception = True if flags & 16 else False
        report_geo = True if flags & 32 else False
        autoarchived = True if flags & 128 else False
        invite_members = True if flags & 256 else False
        geo_distance = Int.read(data) if flags & 64 else None
        return PeerSettings(report_spam=report_spam, add_contact=add_contact, block_contact=block_contact, share_contact=share_contact, need_contacts_exception=need_contacts_exception, report_geo=report_geo, autoarchived=autoarchived, invite_members=invite_members, geo_distance=geo_distance)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.report_spam is not None else 0
        flags |= 2 if cls.add_contact is not None else 0
        flags |= 4 if cls.block_contact is not None else 0
        flags |= 8 if cls.share_contact is not None else 0
        flags |= 16 if cls.need_contacts_exception is not None else 0
        flags |= 32 if cls.report_geo is not None else 0
        flags |= 128 if cls.autoarchived is not None else 0
        flags |= 256 if cls.invite_members is not None else 0
        flags |= 64 if cls.geo_distance is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.geo_distance is not None:
            data.write(Int.getvalue(cls.geo_distance))
        return data.getvalue()


class WallPaper(TL):
    ID = 0xa437c3ed

    def __init__(cls, id: int, access_hash: int, slug: str, document: TL, creator: bool = None, default: bool = None, pattern: bool = None, dark: bool = None, settings: TL = None):
        cls.id = id
        cls.creator = creator
        cls.default = default
        cls.pattern = pattern
        cls.dark = dark
        cls.access_hash = access_hash
        cls.slug = slug
        cls.document = document
        cls.settings = settings

    @staticmethod
    def read(data) -> "WallPaper":
        id = Long.read(data)
        flags = Int.read(data)
        creator = True if flags & 1 else False
        default = True if flags & 2 else False
        pattern = True if flags & 8 else False
        dark = True if flags & 16 else False
        access_hash = Long.read(data)
        slug = String.read(data)
        document = data.getobj()
        settings = data.getobj() if flags & 4 else None
        return WallPaper(id=id, creator=creator, default=default, pattern=pattern, dark=dark, access_hash=access_hash, slug=slug, document=document, settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.creator is not None else 0
        flags |= 2 if cls.default is not None else 0
        flags |= 8 if cls.pattern is not None else 0
        flags |= 16 if cls.dark is not None else 0
        flags |= 4 if cls.settings is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(String.getvalue(cls.slug))
        data.write(cls.document.getvalue())
        
        if cls.settings is not None:
            data.write(cls.settings.getvalue())
        return data.getvalue()


class WallPaperNoFile(TL):
    ID = 0x8af40b25

    def __init__(cls, default: bool = None, dark: bool = None, settings: TL = None):
        cls.default = default
        cls.dark = dark
        cls.settings = settings

    @staticmethod
    def read(data) -> "WallPaperNoFile":
        flags = Int.read(data)
        default = True if flags & 2 else False
        dark = True if flags & 16 else False
        settings = data.getobj() if flags & 4 else None
        return WallPaperNoFile(default=default, dark=dark, settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.default is not None else 0
        flags |= 16 if cls.dark is not None else 0
        flags |= 4 if cls.settings is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.settings is not None:
            data.write(cls.settings.getvalue())
        return data.getvalue()


class InputReportReasonSpam(TL):
    ID = 0x58dbcab8

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputReportReasonSpam":
        
        return InputReportReasonSpam()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputReportReasonViolence(TL):
    ID = 0x1e22c78d

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputReportReasonViolence":
        
        return InputReportReasonViolence()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputReportReasonPornography(TL):
    ID = 0x2e59d922

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputReportReasonPornography":
        
        return InputReportReasonPornography()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputReportReasonChildAbuse(TL):
    ID = 0xadf44ee3

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputReportReasonChildAbuse":
        
        return InputReportReasonChildAbuse()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputReportReasonOther(TL):
    ID = 0xc1e4a2b1

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputReportReasonOther":
        
        return InputReportReasonOther()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputReportReasonCopyright(TL):
    ID = 0x9b89f93a

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputReportReasonCopyright":
        
        return InputReportReasonCopyright()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputReportReasonGeoIrrelevant(TL):
    ID = 0xdbd4feed

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputReportReasonGeoIrrelevant":
        
        return InputReportReasonGeoIrrelevant()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputReportReasonFake(TL):
    ID = 0xf5ddd6e7

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputReportReasonFake":
        
        return InputReportReasonFake()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UserFull(TL):
    ID = 0x139a9a77

    def __init__(cls, user: TL, settings: TL, notify_settings: TL, common_chats_count: int, blocked: bool = None, phone_calls_available: bool = None, phone_calls_private: bool = None, can_pin_message: bool = None, has_scheduled: bool = None, video_calls_available: bool = None, about: str = None, profile_photo: TL = None, bot_info: TL = None, pinned_msg_id: int = None, folder_id: int = None, ttl_period: int = None):
        cls.blocked = blocked
        cls.phone_calls_available = phone_calls_available
        cls.phone_calls_private = phone_calls_private
        cls.can_pin_message = can_pin_message
        cls.has_scheduled = has_scheduled
        cls.video_calls_available = video_calls_available
        cls.user = user
        cls.about = about
        cls.settings = settings
        cls.profile_photo = profile_photo
        cls.notify_settings = notify_settings
        cls.bot_info = bot_info
        cls.pinned_msg_id = pinned_msg_id
        cls.common_chats_count = common_chats_count
        cls.folder_id = folder_id
        cls.ttl_period = ttl_period

    @staticmethod
    def read(data) -> "UserFull":
        flags = Int.read(data)
        blocked = True if flags & 1 else False
        phone_calls_available = True if flags & 16 else False
        phone_calls_private = True if flags & 32 else False
        can_pin_message = True if flags & 128 else False
        has_scheduled = True if flags & 4096 else False
        video_calls_available = True if flags & 8192 else False
        user = data.getobj()
        about = String.read(data) if flags & 2 else None
        settings = data.getobj()
        profile_photo = data.getobj() if flags & 4 else None
        notify_settings = data.getobj()
        bot_info = data.getobj() if flags & 8 else None
        pinned_msg_id = Int.read(data) if flags & 64 else None
        common_chats_count = Int.read(data)
        folder_id = Int.read(data) if flags & 2048 else None
        ttl_period = Int.read(data) if flags & 16384 else None
        return UserFull(blocked=blocked, phone_calls_available=phone_calls_available, phone_calls_private=phone_calls_private, can_pin_message=can_pin_message, has_scheduled=has_scheduled, video_calls_available=video_calls_available, user=user, about=about, settings=settings, profile_photo=profile_photo, notify_settings=notify_settings, bot_info=bot_info, pinned_msg_id=pinned_msg_id, common_chats_count=common_chats_count, folder_id=folder_id, ttl_period=ttl_period)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.blocked is not None else 0
        flags |= 16 if cls.phone_calls_available is not None else 0
        flags |= 32 if cls.phone_calls_private is not None else 0
        flags |= 128 if cls.can_pin_message is not None else 0
        flags |= 4096 if cls.has_scheduled is not None else 0
        flags |= 8192 if cls.video_calls_available is not None else 0
        flags |= 2 if cls.about is not None else 0
        flags |= 4 if cls.profile_photo is not None else 0
        flags |= 8 if cls.bot_info is not None else 0
        flags |= 64 if cls.pinned_msg_id is not None else 0
        flags |= 2048 if cls.folder_id is not None else 0
        flags |= 16384 if cls.ttl_period is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.user.getvalue())
        
        if cls.about is not None:
            data.write(String.getvalue(cls.about))
        data.write(cls.settings.getvalue())
        
        if cls.profile_photo is not None:
            data.write(cls.profile_photo.getvalue())
        data.write(cls.notify_settings.getvalue())
        
        if cls.bot_info is not None:
            data.write(cls.bot_info.getvalue())
        
        if cls.pinned_msg_id is not None:
            data.write(Int.getvalue(cls.pinned_msg_id))
        data.write(Int.getvalue(cls.common_chats_count))
        
        if cls.folder_id is not None:
            data.write(Int.getvalue(cls.folder_id))
        
        if cls.ttl_period is not None:
            data.write(Int.getvalue(cls.ttl_period))
        return data.getvalue()


class Contact(TL):
    ID = 0xf911c994

    def __init__(cls, user_id: int, mutual: bool):
        cls.user_id = user_id
        cls.mutual = mutual

    @staticmethod
    def read(data) -> "Contact":
        user_id = Int.read(data)
        mutual = Bool.read(data)
        return Contact(user_id=user_id, mutual=mutual)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Bool.getvalue(cls.mutual))
        return data.getvalue()


class ImportedContact(TL):
    ID = 0xd0028438

    def __init__(cls, user_id: int, client_id: int):
        cls.user_id = user_id
        cls.client_id = client_id

    @staticmethod
    def read(data) -> "ImportedContact":
        user_id = Int.read(data)
        client_id = Long.read(data)
        return ImportedContact(user_id=user_id, client_id=client_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Long.getvalue(cls.client_id))
        return data.getvalue()


class ContactStatus(TL):
    ID = 0xd3680c61

    def __init__(cls, user_id: int, status: TL):
        cls.user_id = user_id
        cls.status = status

    @staticmethod
    def read(data) -> "ContactStatus":
        user_id = Int.read(data)
        status = data.getobj()
        return ContactStatus(user_id=user_id, status=status)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(cls.status.getvalue())
        return data.getvalue()


class InputMessagesFilterEmpty(TL):
    ID = 0x57e2f66c

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterEmpty":
        
        return InputMessagesFilterEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessagesFilterPhotos(TL):
    ID = 0x9609a51c

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterPhotos":
        
        return InputMessagesFilterPhotos()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessagesFilterVideo(TL):
    ID = 0x9fc00e65

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterVideo":
        
        return InputMessagesFilterVideo()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessagesFilterPhotoVideo(TL):
    ID = 0x56e9f0e4

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterPhotoVideo":
        
        return InputMessagesFilterPhotoVideo()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessagesFilterDocument(TL):
    ID = 0x9eddf188

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterDocument":
        
        return InputMessagesFilterDocument()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessagesFilterUrl(TL):
    ID = 0x7ef0dd87

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterUrl":
        
        return InputMessagesFilterUrl()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessagesFilterGif(TL):
    ID = 0xffc86587

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterGif":
        
        return InputMessagesFilterGif()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessagesFilterVoice(TL):
    ID = 0x50f5c392

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterVoice":
        
        return InputMessagesFilterVoice()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessagesFilterMusic(TL):
    ID = 0x3751b49e

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterMusic":
        
        return InputMessagesFilterMusic()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessagesFilterChatPhotos(TL):
    ID = 0x3a20ecb8

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterChatPhotos":
        
        return InputMessagesFilterChatPhotos()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessagesFilterPhoneCalls(TL):
    ID = 0x80c99768

    def __init__(cls, missed: bool = None):
        cls.missed = missed

    @staticmethod
    def read(data) -> "InputMessagesFilterPhoneCalls":
        flags = Int.read(data)
        missed = True if flags & 1 else False
        return InputMessagesFilterPhoneCalls(missed=missed)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.missed is not None else 0
        data.write(Int.getvalue(flags))
        return data.getvalue()


class InputMessagesFilterRoundVoice(TL):
    ID = 0x7a7c17a4

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterRoundVoice":
        
        return InputMessagesFilterRoundVoice()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessagesFilterRoundVideo(TL):
    ID = 0xb549da53

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterRoundVideo":
        
        return InputMessagesFilterRoundVideo()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessagesFilterMyMentions(TL):
    ID = 0xc1f8e69a

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterMyMentions":
        
        return InputMessagesFilterMyMentions()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessagesFilterGeo(TL):
    ID = 0xe7026d0d

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterGeo":
        
        return InputMessagesFilterGeo()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessagesFilterContacts(TL):
    ID = 0xe062db83

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterContacts":
        
        return InputMessagesFilterContacts()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessagesFilterPinned(TL):
    ID = 0x1bb00451

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagesFilterPinned":
        
        return InputMessagesFilterPinned()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UpdateNewMessage(TL):
    ID = 0x1f2b0afd

    def __init__(cls, message: TL, pts: int, pts_count: int):
        cls.message = message
        cls.pts = pts
        cls.pts_count = pts_count

    @staticmethod
    def read(data) -> "UpdateNewMessage":
        message = data.getobj()
        pts = Int.read(data)
        pts_count = Int.read(data)
        return UpdateNewMessage(message=message, pts=pts, pts_count=pts_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.message.getvalue())
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        return data.getvalue()


class UpdateMessageID(TL):
    ID = 0x4e90bfd6

    def __init__(cls, id: int, random_id: int):
        cls.id = id
        cls.random_id = random_id

    @staticmethod
    def read(data) -> "UpdateMessageID":
        id = Int.read(data)
        random_id = Long.read(data)
        return UpdateMessageID(id=id, random_id=random_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.id))
        data.write(Long.getvalue(cls.random_id))
        return data.getvalue()


class UpdateDeleteMessages(TL):
    ID = 0xa20db0e5

    def __init__(cls, messages: List[int], pts: int, pts_count: int):
        cls.messages = messages
        cls.pts = pts
        cls.pts_count = pts_count

    @staticmethod
    def read(data) -> "UpdateDeleteMessages":
        messages = data.getobj(Int)
        pts = Int.read(data)
        pts_count = Int.read(data)
        return UpdateDeleteMessages(messages=messages, pts=pts, pts_count=pts_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.messages, Int))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        return data.getvalue()


class UpdateUserTyping(TL):
    ID = 0x5c486927

    def __init__(cls, user_id: int, action: TL):
        cls.user_id = user_id
        cls.action = action

    @staticmethod
    def read(data) -> "UpdateUserTyping":
        user_id = Int.read(data)
        action = data.getobj()
        return UpdateUserTyping(user_id=user_id, action=action)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(cls.action.getvalue())
        return data.getvalue()


class UpdateChatUserTyping(TL):
    ID = 0x9a65ea1f

    def __init__(cls, chat_id: int, user_id: int, action: TL):
        cls.chat_id = chat_id
        cls.user_id = user_id
        cls.action = action

    @staticmethod
    def read(data) -> "UpdateChatUserTyping":
        chat_id = Int.read(data)
        user_id = Int.read(data)
        action = data.getobj()
        return UpdateChatUserTyping(chat_id=chat_id, user_id=user_id, action=action)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        data.write(Int.getvalue(cls.user_id))
        data.write(cls.action.getvalue())
        return data.getvalue()


class UpdateChatParticipants(TL):
    ID = 0x7761198

    def __init__(cls, participants: TL):
        cls.participants = participants

    @staticmethod
    def read(data) -> "UpdateChatParticipants":
        participants = data.getobj()
        return UpdateChatParticipants(participants=participants)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.participants.getvalue())
        return data.getvalue()


class UpdateUserStatus(TL):
    ID = 0x1bfbd823

    def __init__(cls, user_id: int, status: TL):
        cls.user_id = user_id
        cls.status = status

    @staticmethod
    def read(data) -> "UpdateUserStatus":
        user_id = Int.read(data)
        status = data.getobj()
        return UpdateUserStatus(user_id=user_id, status=status)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(cls.status.getvalue())
        return data.getvalue()


class UpdateUserName(TL):
    ID = 0xa7332b73

    def __init__(cls, user_id: int, first_name: str, last_name: str, username: str):
        cls.user_id = user_id
        cls.first_name = first_name
        cls.last_name = last_name
        cls.username = username

    @staticmethod
    def read(data) -> "UpdateUserName":
        user_id = Int.read(data)
        first_name = String.read(data)
        last_name = String.read(data)
        username = String.read(data)
        return UpdateUserName(user_id=user_id, first_name=first_name, last_name=last_name, username=username)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(String.getvalue(cls.first_name))
        data.write(String.getvalue(cls.last_name))
        data.write(String.getvalue(cls.username))
        return data.getvalue()


class UpdateUserPhoto(TL):
    ID = 0x95313b0c

    def __init__(cls, user_id: int, date: int, photo: TL, previous: bool):
        cls.user_id = user_id
        cls.date = date
        cls.photo = photo
        cls.previous = previous

    @staticmethod
    def read(data) -> "UpdateUserPhoto":
        user_id = Int.read(data)
        date = Int.read(data)
        photo = data.getobj()
        previous = Bool.read(data)
        return UpdateUserPhoto(user_id=user_id, date=date, photo=photo, previous=previous)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Int.getvalue(cls.date))
        data.write(cls.photo.getvalue())
        data.write(Bool.getvalue(cls.previous))
        return data.getvalue()


class UpdateNewEncryptedMessage(TL):
    ID = 0x12bcbd9a

    def __init__(cls, message: TL, qts: int):
        cls.message = message
        cls.qts = qts

    @staticmethod
    def read(data) -> "UpdateNewEncryptedMessage":
        message = data.getobj()
        qts = Int.read(data)
        return UpdateNewEncryptedMessage(message=message, qts=qts)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.message.getvalue())
        data.write(Int.getvalue(cls.qts))
        return data.getvalue()


class UpdateEncryptedChatTyping(TL):
    ID = 0x1710f156

    def __init__(cls, chat_id: int):
        cls.chat_id = chat_id

    @staticmethod
    def read(data) -> "UpdateEncryptedChatTyping":
        chat_id = Int.read(data)
        return UpdateEncryptedChatTyping(chat_id=chat_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        return data.getvalue()


class UpdateEncryption(TL):
    ID = 0xb4a2e88d

    def __init__(cls, chat: TL, date: int):
        cls.chat = chat
        cls.date = date

    @staticmethod
    def read(data) -> "UpdateEncryption":
        chat = data.getobj()
        date = Int.read(data)
        return UpdateEncryption(chat=chat, date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.chat.getvalue())
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class UpdateEncryptedMessagesRead(TL):
    ID = 0x38fe25b7

    def __init__(cls, chat_id: int, max_date: int, date: int):
        cls.chat_id = chat_id
        cls.max_date = max_date
        cls.date = date

    @staticmethod
    def read(data) -> "UpdateEncryptedMessagesRead":
        chat_id = Int.read(data)
        max_date = Int.read(data)
        date = Int.read(data)
        return UpdateEncryptedMessagesRead(chat_id=chat_id, max_date=max_date, date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        data.write(Int.getvalue(cls.max_date))
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class UpdateChatParticipantAdd(TL):
    ID = 0xea4b0e5c

    def __init__(cls, chat_id: int, user_id: int, inviter_id: int, date: int, version: int):
        cls.chat_id = chat_id
        cls.user_id = user_id
        cls.inviter_id = inviter_id
        cls.date = date
        cls.version = version

    @staticmethod
    def read(data) -> "UpdateChatParticipantAdd":
        chat_id = Int.read(data)
        user_id = Int.read(data)
        inviter_id = Int.read(data)
        date = Int.read(data)
        version = Int.read(data)
        return UpdateChatParticipantAdd(chat_id=chat_id, user_id=user_id, inviter_id=inviter_id, date=date, version=version)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        data.write(Int.getvalue(cls.user_id))
        data.write(Int.getvalue(cls.inviter_id))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.version))
        return data.getvalue()


class UpdateChatParticipantDelete(TL):
    ID = 0x6e5f8c22

    def __init__(cls, chat_id: int, user_id: int, version: int):
        cls.chat_id = chat_id
        cls.user_id = user_id
        cls.version = version

    @staticmethod
    def read(data) -> "UpdateChatParticipantDelete":
        chat_id = Int.read(data)
        user_id = Int.read(data)
        version = Int.read(data)
        return UpdateChatParticipantDelete(chat_id=chat_id, user_id=user_id, version=version)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        data.write(Int.getvalue(cls.user_id))
        data.write(Int.getvalue(cls.version))
        return data.getvalue()


class UpdateDcOptions(TL):
    ID = 0x8e5e9873

    def __init__(cls, dc_options: List[TL]):
        cls.dc_options = dc_options

    @staticmethod
    def read(data) -> "UpdateDcOptions":
        dc_options = data.getobj()
        return UpdateDcOptions(dc_options=dc_options)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.dc_options))
        return data.getvalue()


class UpdateNotifySettings(TL):
    ID = 0xbec268ef

    def __init__(cls, peer: TL, notify_settings: TL):
        cls.peer = peer
        cls.notify_settings = notify_settings

    @staticmethod
    def read(data) -> "UpdateNotifySettings":
        peer = data.getobj()
        notify_settings = data.getobj()
        return UpdateNotifySettings(peer=peer, notify_settings=notify_settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(cls.notify_settings.getvalue())
        return data.getvalue()


class UpdateServiceNotification(TL):
    ID = 0xebe46819

    def __init__(cls, type: str, message: str, media: TL, entities: List[TL], popup: bool = None, inbox_date: int = None):
        cls.popup = popup
        cls.inbox_date = inbox_date
        cls.type = type
        cls.message = message
        cls.media = media
        cls.entities = entities

    @staticmethod
    def read(data) -> "UpdateServiceNotification":
        flags = Int.read(data)
        popup = True if flags & 1 else False
        inbox_date = Int.read(data) if flags & 2 else None
        type = String.read(data)
        message = String.read(data)
        media = data.getobj()
        entities = data.getobj()
        return UpdateServiceNotification(popup=popup, inbox_date=inbox_date, type=type, message=message, media=media, entities=entities)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.popup is not None else 0
        flags |= 2 if cls.inbox_date is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.inbox_date is not None:
            data.write(Int.getvalue(cls.inbox_date))
        data.write(String.getvalue(cls.type))
        data.write(String.getvalue(cls.message))
        data.write(cls.media.getvalue())
        data.write(Vector().getvalue(cls.entities))
        return data.getvalue()


class UpdatePrivacy(TL):
    ID = 0xee3b272a

    def __init__(cls, key: TL, rules: List[TL]):
        cls.key = key
        cls.rules = rules

    @staticmethod
    def read(data) -> "UpdatePrivacy":
        key = data.getobj()
        rules = data.getobj()
        return UpdatePrivacy(key=key, rules=rules)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.key.getvalue())
        data.write(Vector().getvalue(cls.rules))
        return data.getvalue()


class UpdateUserPhone(TL):
    ID = 0x12b9417b

    def __init__(cls, user_id: int, phone: str):
        cls.user_id = user_id
        cls.phone = phone

    @staticmethod
    def read(data) -> "UpdateUserPhone":
        user_id = Int.read(data)
        phone = String.read(data)
        return UpdateUserPhone(user_id=user_id, phone=phone)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(String.getvalue(cls.phone))
        return data.getvalue()


class UpdateReadHistoryInbox(TL):
    ID = 0x9c974fdf

    def __init__(cls, peer: TL, max_id: int, still_unread_count: int, pts: int, pts_count: int, folder_id: int = None):
        cls.folder_id = folder_id
        cls.peer = peer
        cls.max_id = max_id
        cls.still_unread_count = still_unread_count
        cls.pts = pts
        cls.pts_count = pts_count

    @staticmethod
    def read(data) -> "UpdateReadHistoryInbox":
        flags = Int.read(data)
        folder_id = Int.read(data) if flags & 1 else None
        peer = data.getobj()
        max_id = Int.read(data)
        still_unread_count = Int.read(data)
        pts = Int.read(data)
        pts_count = Int.read(data)
        return UpdateReadHistoryInbox(folder_id=folder_id, peer=peer, max_id=max_id, still_unread_count=still_unread_count, pts=pts, pts_count=pts_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.folder_id is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.folder_id is not None:
            data.write(Int.getvalue(cls.folder_id))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.max_id))
        data.write(Int.getvalue(cls.still_unread_count))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        return data.getvalue()


class UpdateReadHistoryOutbox(TL):
    ID = 0x2f2f21bf

    def __init__(cls, peer: TL, max_id: int, pts: int, pts_count: int):
        cls.peer = peer
        cls.max_id = max_id
        cls.pts = pts
        cls.pts_count = pts_count

    @staticmethod
    def read(data) -> "UpdateReadHistoryOutbox":
        peer = data.getobj()
        max_id = Int.read(data)
        pts = Int.read(data)
        pts_count = Int.read(data)
        return UpdateReadHistoryOutbox(peer=peer, max_id=max_id, pts=pts, pts_count=pts_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.max_id))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        return data.getvalue()


class UpdateWebPage(TL):
    ID = 0x7f891213

    def __init__(cls, webpage: TL, pts: int, pts_count: int):
        cls.webpage = webpage
        cls.pts = pts
        cls.pts_count = pts_count

    @staticmethod
    def read(data) -> "UpdateWebPage":
        webpage = data.getobj()
        pts = Int.read(data)
        pts_count = Int.read(data)
        return UpdateWebPage(webpage=webpage, pts=pts, pts_count=pts_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.webpage.getvalue())
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        return data.getvalue()


class UpdateReadMessagesContents(TL):
    ID = 0x68c13933

    def __init__(cls, messages: List[int], pts: int, pts_count: int):
        cls.messages = messages
        cls.pts = pts
        cls.pts_count = pts_count

    @staticmethod
    def read(data) -> "UpdateReadMessagesContents":
        messages = data.getobj(Int)
        pts = Int.read(data)
        pts_count = Int.read(data)
        return UpdateReadMessagesContents(messages=messages, pts=pts, pts_count=pts_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.messages, Int))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        return data.getvalue()


class UpdateChannelTooLong(TL):
    ID = 0xeb0467fb

    def __init__(cls, channel_id: int, pts: int = None):
        cls.channel_id = channel_id
        cls.pts = pts

    @staticmethod
    def read(data) -> "UpdateChannelTooLong":
        flags = Int.read(data)
        channel_id = Int.read(data)
        pts = Int.read(data) if flags & 1 else None
        return UpdateChannelTooLong(channel_id=channel_id, pts=pts)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.pts is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.channel_id))
        
        if cls.pts is not None:
            data.write(Int.getvalue(cls.pts))
        return data.getvalue()


class UpdateChannel(TL):
    ID = 0xb6d45656

    def __init__(cls, channel_id: int):
        cls.channel_id = channel_id

    @staticmethod
    def read(data) -> "UpdateChannel":
        channel_id = Int.read(data)
        return UpdateChannel(channel_id=channel_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.channel_id))
        return data.getvalue()


class UpdateNewChannelMessage(TL):
    ID = 0x62ba04d9

    def __init__(cls, message: TL, pts: int, pts_count: int):
        cls.message = message
        cls.pts = pts
        cls.pts_count = pts_count

    @staticmethod
    def read(data) -> "UpdateNewChannelMessage":
        message = data.getobj()
        pts = Int.read(data)
        pts_count = Int.read(data)
        return UpdateNewChannelMessage(message=message, pts=pts, pts_count=pts_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.message.getvalue())
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        return data.getvalue()


class UpdateReadChannelInbox(TL):
    ID = 0x330b5424

    def __init__(cls, channel_id: int, max_id: int, still_unread_count: int, pts: int, folder_id: int = None):
        cls.folder_id = folder_id
        cls.channel_id = channel_id
        cls.max_id = max_id
        cls.still_unread_count = still_unread_count
        cls.pts = pts

    @staticmethod
    def read(data) -> "UpdateReadChannelInbox":
        flags = Int.read(data)
        folder_id = Int.read(data) if flags & 1 else None
        channel_id = Int.read(data)
        max_id = Int.read(data)
        still_unread_count = Int.read(data)
        pts = Int.read(data)
        return UpdateReadChannelInbox(folder_id=folder_id, channel_id=channel_id, max_id=max_id, still_unread_count=still_unread_count, pts=pts)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.folder_id is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.folder_id is not None:
            data.write(Int.getvalue(cls.folder_id))
        data.write(Int.getvalue(cls.channel_id))
        data.write(Int.getvalue(cls.max_id))
        data.write(Int.getvalue(cls.still_unread_count))
        data.write(Int.getvalue(cls.pts))
        return data.getvalue()


class UpdateDeleteChannelMessages(TL):
    ID = 0xc37521c9

    def __init__(cls, channel_id: int, messages: List[int], pts: int, pts_count: int):
        cls.channel_id = channel_id
        cls.messages = messages
        cls.pts = pts
        cls.pts_count = pts_count

    @staticmethod
    def read(data) -> "UpdateDeleteChannelMessages":
        channel_id = Int.read(data)
        messages = data.getobj(Int)
        pts = Int.read(data)
        pts_count = Int.read(data)
        return UpdateDeleteChannelMessages(channel_id=channel_id, messages=messages, pts=pts, pts_count=pts_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.channel_id))
        data.write(Vector().getvalue(cls.messages, Int))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        return data.getvalue()


class UpdateChannelMessageViews(TL):
    ID = 0x98a12b4b

    def __init__(cls, channel_id: int, id: int, views: int):
        cls.channel_id = channel_id
        cls.id = id
        cls.views = views

    @staticmethod
    def read(data) -> "UpdateChannelMessageViews":
        channel_id = Int.read(data)
        id = Int.read(data)
        views = Int.read(data)
        return UpdateChannelMessageViews(channel_id=channel_id, id=id, views=views)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.channel_id))
        data.write(Int.getvalue(cls.id))
        data.write(Int.getvalue(cls.views))
        return data.getvalue()


class UpdateChatParticipantAdmin(TL):
    ID = 0xb6901959

    def __init__(cls, chat_id: int, user_id: int, is_admin: bool, version: int):
        cls.chat_id = chat_id
        cls.user_id = user_id
        cls.is_admin = is_admin
        cls.version = version

    @staticmethod
    def read(data) -> "UpdateChatParticipantAdmin":
        chat_id = Int.read(data)
        user_id = Int.read(data)
        is_admin = Bool.read(data)
        version = Int.read(data)
        return UpdateChatParticipantAdmin(chat_id=chat_id, user_id=user_id, is_admin=is_admin, version=version)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        data.write(Int.getvalue(cls.user_id))
        data.write(Bool.getvalue(cls.is_admin))
        data.write(Int.getvalue(cls.version))
        return data.getvalue()


class UpdateNewStickerSet(TL):
    ID = 0x688a30aa

    def __init__(cls, stickerset: TL):
        cls.stickerset = stickerset

    @staticmethod
    def read(data) -> "UpdateNewStickerSet":
        stickerset = data.getobj()
        return UpdateNewStickerSet(stickerset=stickerset)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.stickerset.getvalue())
        return data.getvalue()


class UpdateStickerSetsOrder(TL):
    ID = 0xbb2d201

    def __init__(cls, order: List[int], masks: bool = None):
        cls.masks = masks
        cls.order = order

    @staticmethod
    def read(data) -> "UpdateStickerSetsOrder":
        flags = Int.read(data)
        masks = True if flags & 1 else False
        order = data.getobj(Long)
        return UpdateStickerSetsOrder(masks=masks, order=order)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.masks is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Vector().getvalue(cls.order, Long))
        return data.getvalue()


class UpdateStickerSets(TL):
    ID = 0x43ae3dec

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UpdateStickerSets":
        
        return UpdateStickerSets()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UpdateSavedGifs(TL):
    ID = 0x9375341e

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UpdateSavedGifs":
        
        return UpdateSavedGifs()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UpdateBotInlineQuery(TL):
    ID = 0x3f2038db

    def __init__(cls, query_id: int, user_id: int, query: str, offset: str, geo: TL = None, peer_type: TL = None):
        cls.query_id = query_id
        cls.user_id = user_id
        cls.query = query
        cls.geo = geo
        cls.peer_type = peer_type
        cls.offset = offset

    @staticmethod
    def read(data) -> "UpdateBotInlineQuery":
        flags = Int.read(data)
        query_id = Long.read(data)
        user_id = Int.read(data)
        query = String.read(data)
        geo = data.getobj() if flags & 1 else None
        peer_type = data.getobj() if flags & 2 else None
        offset = String.read(data)
        return UpdateBotInlineQuery(query_id=query_id, user_id=user_id, query=query, geo=geo, peer_type=peer_type, offset=offset)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.geo is not None else 0
        flags |= 2 if cls.peer_type is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.query_id))
        data.write(Int.getvalue(cls.user_id))
        data.write(String.getvalue(cls.query))
        
        if cls.geo is not None:
            data.write(cls.geo.getvalue())
        
        if cls.peer_type is not None:
            data.write(cls.peer_type.getvalue())
        data.write(String.getvalue(cls.offset))
        return data.getvalue()


class UpdateBotInlineSend(TL):
    ID = 0xe48f964

    def __init__(cls, user_id: int, query: str, id: str, geo: TL = None, msg_id: TL = None):
        cls.user_id = user_id
        cls.query = query
        cls.geo = geo
        cls.id = id
        cls.msg_id = msg_id

    @staticmethod
    def read(data) -> "UpdateBotInlineSend":
        flags = Int.read(data)
        user_id = Int.read(data)
        query = String.read(data)
        geo = data.getobj() if flags & 1 else None
        id = String.read(data)
        msg_id = data.getobj() if flags & 2 else None
        return UpdateBotInlineSend(user_id=user_id, query=query, geo=geo, id=id, msg_id=msg_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.geo is not None else 0
        flags |= 2 if cls.msg_id is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.user_id))
        data.write(String.getvalue(cls.query))
        
        if cls.geo is not None:
            data.write(cls.geo.getvalue())
        data.write(String.getvalue(cls.id))
        
        if cls.msg_id is not None:
            data.write(cls.msg_id.getvalue())
        return data.getvalue()


class UpdateEditChannelMessage(TL):
    ID = 0x1b3f4df7

    def __init__(cls, message: TL, pts: int, pts_count: int):
        cls.message = message
        cls.pts = pts
        cls.pts_count = pts_count

    @staticmethod
    def read(data) -> "UpdateEditChannelMessage":
        message = data.getobj()
        pts = Int.read(data)
        pts_count = Int.read(data)
        return UpdateEditChannelMessage(message=message, pts=pts, pts_count=pts_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.message.getvalue())
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        return data.getvalue()


class UpdateBotCallbackQuery(TL):
    ID = 0xe73547e1

    def __init__(cls, query_id: int, user_id: int, peer: TL, msg_id: int, chat_instance: int, data: bytes = None, game_short_name: str = None):
        cls.query_id = query_id
        cls.user_id = user_id
        cls.peer = peer
        cls.msg_id = msg_id
        cls.chat_instance = chat_instance
        cls.data = data
        cls.game_short_name = game_short_name

    @staticmethod
    def read(data) -> "UpdateBotCallbackQuery":
        flags = Int.read(data)
        query_id = Long.read(data)
        user_id = Int.read(data)
        peer = data.getobj()
        msg_id = Int.read(data)
        chat_instance = Long.read(data)
        data = Bytes.read(data) if flags & 1 else None
        game_short_name = String.read(data) if flags & 2 else None
        return UpdateBotCallbackQuery(query_id=query_id, user_id=user_id, peer=peer, msg_id=msg_id, chat_instance=chat_instance, data=data, game_short_name=game_short_name)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.data is not None else 0
        flags |= 2 if cls.game_short_name is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.query_id))
        data.write(Int.getvalue(cls.user_id))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        data.write(Long.getvalue(cls.chat_instance))
        
        if cls.data is not None:
            data.write(Bytes.getvalue(cls.data))
        
        if cls.game_short_name is not None:
            data.write(String.getvalue(cls.game_short_name))
        return data.getvalue()


class UpdateEditMessage(TL):
    ID = 0xe40370a3

    def __init__(cls, message: TL, pts: int, pts_count: int):
        cls.message = message
        cls.pts = pts
        cls.pts_count = pts_count

    @staticmethod
    def read(data) -> "UpdateEditMessage":
        message = data.getobj()
        pts = Int.read(data)
        pts_count = Int.read(data)
        return UpdateEditMessage(message=message, pts=pts, pts_count=pts_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.message.getvalue())
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        return data.getvalue()


class UpdateInlineBotCallbackQuery(TL):
    ID = 0xf9d27a5a

    def __init__(cls, query_id: int, user_id: int, msg_id: TL, chat_instance: int, data: bytes = None, game_short_name: str = None):
        cls.query_id = query_id
        cls.user_id = user_id
        cls.msg_id = msg_id
        cls.chat_instance = chat_instance
        cls.data = data
        cls.game_short_name = game_short_name

    @staticmethod
    def read(data) -> "UpdateInlineBotCallbackQuery":
        flags = Int.read(data)
        query_id = Long.read(data)
        user_id = Int.read(data)
        msg_id = data.getobj()
        chat_instance = Long.read(data)
        data = Bytes.read(data) if flags & 1 else None
        game_short_name = String.read(data) if flags & 2 else None
        return UpdateInlineBotCallbackQuery(query_id=query_id, user_id=user_id, msg_id=msg_id, chat_instance=chat_instance, data=data, game_short_name=game_short_name)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.data is not None else 0
        flags |= 2 if cls.game_short_name is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.query_id))
        data.write(Int.getvalue(cls.user_id))
        data.write(cls.msg_id.getvalue())
        data.write(Long.getvalue(cls.chat_instance))
        
        if cls.data is not None:
            data.write(Bytes.getvalue(cls.data))
        
        if cls.game_short_name is not None:
            data.write(String.getvalue(cls.game_short_name))
        return data.getvalue()


class UpdateReadChannelOutbox(TL):
    ID = 0x25d6c9c7

    def __init__(cls, channel_id: int, max_id: int):
        cls.channel_id = channel_id
        cls.max_id = max_id

    @staticmethod
    def read(data) -> "UpdateReadChannelOutbox":
        channel_id = Int.read(data)
        max_id = Int.read(data)
        return UpdateReadChannelOutbox(channel_id=channel_id, max_id=max_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.channel_id))
        data.write(Int.getvalue(cls.max_id))
        return data.getvalue()


class UpdateDraftMessage(TL):
    ID = 0xee2bb969

    def __init__(cls, peer: TL, draft: TL):
        cls.peer = peer
        cls.draft = draft

    @staticmethod
    def read(data) -> "UpdateDraftMessage":
        peer = data.getobj()
        draft = data.getobj()
        return UpdateDraftMessage(peer=peer, draft=draft)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(cls.draft.getvalue())
        return data.getvalue()


class UpdateReadFeaturedStickers(TL):
    ID = 0x571d2742

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UpdateReadFeaturedStickers":
        
        return UpdateReadFeaturedStickers()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UpdateRecentStickers(TL):
    ID = 0x9a422c20

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UpdateRecentStickers":
        
        return UpdateRecentStickers()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UpdateConfig(TL):
    ID = 0xa229dd06

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UpdateConfig":
        
        return UpdateConfig()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UpdatePtsChanged(TL):
    ID = 0x3354678f

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UpdatePtsChanged":
        
        return UpdatePtsChanged()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UpdateChannelWebPage(TL):
    ID = 0x40771900

    def __init__(cls, channel_id: int, webpage: TL, pts: int, pts_count: int):
        cls.channel_id = channel_id
        cls.webpage = webpage
        cls.pts = pts
        cls.pts_count = pts_count

    @staticmethod
    def read(data) -> "UpdateChannelWebPage":
        channel_id = Int.read(data)
        webpage = data.getobj()
        pts = Int.read(data)
        pts_count = Int.read(data)
        return UpdateChannelWebPage(channel_id=channel_id, webpage=webpage, pts=pts, pts_count=pts_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.channel_id))
        data.write(cls.webpage.getvalue())
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        return data.getvalue()


class UpdateDialogPinned(TL):
    ID = 0x6e6fe51c

    def __init__(cls, peer: TL, pinned: bool = None, folder_id: int = None):
        cls.pinned = pinned
        cls.folder_id = folder_id
        cls.peer = peer

    @staticmethod
    def read(data) -> "UpdateDialogPinned":
        flags = Int.read(data)
        pinned = True if flags & 1 else False
        folder_id = Int.read(data) if flags & 2 else None
        peer = data.getobj()
        return UpdateDialogPinned(pinned=pinned, folder_id=folder_id, peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.pinned is not None else 0
        flags |= 2 if cls.folder_id is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.folder_id is not None:
            data.write(Int.getvalue(cls.folder_id))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class UpdatePinnedDialogs(TL):
    ID = 0xfa0f3ca2

    def __init__(cls, folder_id: int = None, order: List[TL] = None):
        cls.folder_id = folder_id
        cls.order = order

    @staticmethod
    def read(data) -> "UpdatePinnedDialogs":
        flags = Int.read(data)
        folder_id = Int.read(data) if flags & 2 else None
        order = data.getobj() if flags & 1 else []
        return UpdatePinnedDialogs(folder_id=folder_id, order=order)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.folder_id is not None else 0
        flags |= 1 if cls.order is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.folder_id is not None:
            data.write(Int.getvalue(cls.folder_id))
        
        if cls.order is not None:
            data.write(Vector().getvalue(cls.order))
        return data.getvalue()


class UpdateBotWebhookJSON(TL):
    ID = 0x8317c0c3

    def __init__(cls, data: TL):
        cls.data = data

    @staticmethod
    def read(data) -> "UpdateBotWebhookJSON":
        data = data.getobj()
        return UpdateBotWebhookJSON(data=data)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.data.getvalue())
        return data.getvalue()


class UpdateBotWebhookJSONQuery(TL):
    ID = 0x9b9240a6

    def __init__(cls, query_id: int, data: TL, timeout: int):
        cls.query_id = query_id
        cls.data = data
        cls.timeout = timeout

    @staticmethod
    def read(data) -> "UpdateBotWebhookJSONQuery":
        query_id = Long.read(data)
        data = data.getobj()
        timeout = Int.read(data)
        return UpdateBotWebhookJSONQuery(query_id=query_id, data=data, timeout=timeout)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.query_id))
        data.write(cls.data.getvalue())
        data.write(Int.getvalue(cls.timeout))
        return data.getvalue()


class UpdateBotShippingQuery(TL):
    ID = 0xe0cdc940

    def __init__(cls, query_id: int, user_id: int, payload: bytes, shipping_address: TL):
        cls.query_id = query_id
        cls.user_id = user_id
        cls.payload = payload
        cls.shipping_address = shipping_address

    @staticmethod
    def read(data) -> "UpdateBotShippingQuery":
        query_id = Long.read(data)
        user_id = Int.read(data)
        payload = Bytes.read(data)
        shipping_address = data.getobj()
        return UpdateBotShippingQuery(query_id=query_id, user_id=user_id, payload=payload, shipping_address=shipping_address)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.query_id))
        data.write(Int.getvalue(cls.user_id))
        data.write(Bytes.getvalue(cls.payload))
        data.write(cls.shipping_address.getvalue())
        return data.getvalue()


class UpdateBotPrecheckoutQuery(TL):
    ID = 0x5d2f3aa9

    def __init__(cls, query_id: int, user_id: int, payload: bytes, currency: str, total_amount: int, info: TL = None, shipping_option_id: str = None):
        cls.query_id = query_id
        cls.user_id = user_id
        cls.payload = payload
        cls.info = info
        cls.shipping_option_id = shipping_option_id
        cls.currency = currency
        cls.total_amount = total_amount

    @staticmethod
    def read(data) -> "UpdateBotPrecheckoutQuery":
        flags = Int.read(data)
        query_id = Long.read(data)
        user_id = Int.read(data)
        payload = Bytes.read(data)
        info = data.getobj() if flags & 1 else None
        shipping_option_id = String.read(data) if flags & 2 else None
        currency = String.read(data)
        total_amount = Long.read(data)
        return UpdateBotPrecheckoutQuery(query_id=query_id, user_id=user_id, payload=payload, info=info, shipping_option_id=shipping_option_id, currency=currency, total_amount=total_amount)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.info is not None else 0
        flags |= 2 if cls.shipping_option_id is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.query_id))
        data.write(Int.getvalue(cls.user_id))
        data.write(Bytes.getvalue(cls.payload))
        
        if cls.info is not None:
            data.write(cls.info.getvalue())
        
        if cls.shipping_option_id is not None:
            data.write(String.getvalue(cls.shipping_option_id))
        data.write(String.getvalue(cls.currency))
        data.write(Long.getvalue(cls.total_amount))
        return data.getvalue()


class UpdatePhoneCall(TL):
    ID = 0xab0f6b1e

    def __init__(cls, phone_call: TL):
        cls.phone_call = phone_call

    @staticmethod
    def read(data) -> "UpdatePhoneCall":
        phone_call = data.getobj()
        return UpdatePhoneCall(phone_call=phone_call)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.phone_call.getvalue())
        return data.getvalue()


class UpdateLangPackTooLong(TL):
    ID = 0x46560264

    def __init__(cls, lang_code: str):
        cls.lang_code = lang_code

    @staticmethod
    def read(data) -> "UpdateLangPackTooLong":
        lang_code = String.read(data)
        return UpdateLangPackTooLong(lang_code=lang_code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.lang_code))
        return data.getvalue()


class UpdateLangPack(TL):
    ID = 0x56022f4d

    def __init__(cls, difference: TL):
        cls.difference = difference

    @staticmethod
    def read(data) -> "UpdateLangPack":
        difference = data.getobj()
        return UpdateLangPack(difference=difference)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.difference.getvalue())
        return data.getvalue()


class UpdateFavedStickers(TL):
    ID = 0xe511996d

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UpdateFavedStickers":
        
        return UpdateFavedStickers()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UpdateChannelReadMessagesContents(TL):
    ID = 0x89893b45

    def __init__(cls, channel_id: int, messages: List[int]):
        cls.channel_id = channel_id
        cls.messages = messages

    @staticmethod
    def read(data) -> "UpdateChannelReadMessagesContents":
        channel_id = Int.read(data)
        messages = data.getobj(Int)
        return UpdateChannelReadMessagesContents(channel_id=channel_id, messages=messages)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.channel_id))
        data.write(Vector().getvalue(cls.messages, Int))
        return data.getvalue()


class UpdateContactsReset(TL):
    ID = 0x7084a7be

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UpdateContactsReset":
        
        return UpdateContactsReset()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UpdateChannelAvailableMessages(TL):
    ID = 0x70db6837

    def __init__(cls, channel_id: int, available_min_id: int):
        cls.channel_id = channel_id
        cls.available_min_id = available_min_id

    @staticmethod
    def read(data) -> "UpdateChannelAvailableMessages":
        channel_id = Int.read(data)
        available_min_id = Int.read(data)
        return UpdateChannelAvailableMessages(channel_id=channel_id, available_min_id=available_min_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.channel_id))
        data.write(Int.getvalue(cls.available_min_id))
        return data.getvalue()


class UpdateDialogUnreadMark(TL):
    ID = 0xe16459c3

    def __init__(cls, peer: TL, unread: bool = None):
        cls.unread = unread
        cls.peer = peer

    @staticmethod
    def read(data) -> "UpdateDialogUnreadMark":
        flags = Int.read(data)
        unread = True if flags & 1 else False
        peer = data.getobj()
        return UpdateDialogUnreadMark(unread=unread, peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.unread is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class UpdateMessagePoll(TL):
    ID = 0xaca1657b

    def __init__(cls, poll_id: int, results: TL, poll: TL = None):
        cls.poll_id = poll_id
        cls.poll = poll
        cls.results = results

    @staticmethod
    def read(data) -> "UpdateMessagePoll":
        flags = Int.read(data)
        poll_id = Long.read(data)
        poll = data.getobj() if flags & 1 else None
        results = data.getobj()
        return UpdateMessagePoll(poll_id=poll_id, poll=poll, results=results)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.poll is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.poll_id))
        
        if cls.poll is not None:
            data.write(cls.poll.getvalue())
        data.write(cls.results.getvalue())
        return data.getvalue()


class UpdateChatDefaultBannedRights(TL):
    ID = 0x54c01850

    def __init__(cls, peer: TL, default_banned_rights: TL, version: int):
        cls.peer = peer
        cls.default_banned_rights = default_banned_rights
        cls.version = version

    @staticmethod
    def read(data) -> "UpdateChatDefaultBannedRights":
        peer = data.getobj()
        default_banned_rights = data.getobj()
        version = Int.read(data)
        return UpdateChatDefaultBannedRights(peer=peer, default_banned_rights=default_banned_rights, version=version)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(cls.default_banned_rights.getvalue())
        data.write(Int.getvalue(cls.version))
        return data.getvalue()


class UpdateFolderPeers(TL):
    ID = 0x19360dc0

    def __init__(cls, folder_peers: List[TL], pts: int, pts_count: int):
        cls.folder_peers = folder_peers
        cls.pts = pts
        cls.pts_count = pts_count

    @staticmethod
    def read(data) -> "UpdateFolderPeers":
        folder_peers = data.getobj()
        pts = Int.read(data)
        pts_count = Int.read(data)
        return UpdateFolderPeers(folder_peers=folder_peers, pts=pts, pts_count=pts_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.folder_peers))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        return data.getvalue()


class UpdatePeerSettings(TL):
    ID = 0x6a7e7366

    def __init__(cls, peer: TL, settings: TL):
        cls.peer = peer
        cls.settings = settings

    @staticmethod
    def read(data) -> "UpdatePeerSettings":
        peer = data.getobj()
        settings = data.getobj()
        return UpdatePeerSettings(peer=peer, settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(cls.settings.getvalue())
        return data.getvalue()


class UpdatePeerLocated(TL):
    ID = 0xb4afcfb0

    def __init__(cls, peers: List[TL]):
        cls.peers = peers

    @staticmethod
    def read(data) -> "UpdatePeerLocated":
        peers = data.getobj()
        return UpdatePeerLocated(peers=peers)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.peers))
        return data.getvalue()


class UpdateNewScheduledMessage(TL):
    ID = 0x39a51dfb

    def __init__(cls, message: TL):
        cls.message = message

    @staticmethod
    def read(data) -> "UpdateNewScheduledMessage":
        message = data.getobj()
        return UpdateNewScheduledMessage(message=message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.message.getvalue())
        return data.getvalue()


class UpdateDeleteScheduledMessages(TL):
    ID = 0x90866cee

    def __init__(cls, peer: TL, messages: List[int]):
        cls.peer = peer
        cls.messages = messages

    @staticmethod
    def read(data) -> "UpdateDeleteScheduledMessages":
        peer = data.getobj()
        messages = data.getobj(Int)
        return UpdateDeleteScheduledMessages(peer=peer, messages=messages)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Vector().getvalue(cls.messages, Int))
        return data.getvalue()


class UpdateTheme(TL):
    ID = 0x8216fba3

    def __init__(cls, theme: TL):
        cls.theme = theme

    @staticmethod
    def read(data) -> "UpdateTheme":
        theme = data.getobj()
        return UpdateTheme(theme=theme)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.theme.getvalue())
        return data.getvalue()


class UpdateGeoLiveViewed(TL):
    ID = 0x871fb939

    def __init__(cls, peer: TL, msg_id: int):
        cls.peer = peer
        cls.msg_id = msg_id

    @staticmethod
    def read(data) -> "UpdateGeoLiveViewed":
        peer = data.getobj()
        msg_id = Int.read(data)
        return UpdateGeoLiveViewed(peer=peer, msg_id=msg_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        return data.getvalue()


class UpdateLoginToken(TL):
    ID = 0x564fe691

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UpdateLoginToken":
        
        return UpdateLoginToken()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UpdateMessagePollVote(TL):
    ID = 0x42f88f2c

    def __init__(cls, poll_id: int, user_id: int, options: List[bytes]):
        cls.poll_id = poll_id
        cls.user_id = user_id
        cls.options = options

    @staticmethod
    def read(data) -> "UpdateMessagePollVote":
        poll_id = Long.read(data)
        user_id = Int.read(data)
        options = data.getobj(Bytes)
        return UpdateMessagePollVote(poll_id=poll_id, user_id=user_id, options=options)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.poll_id))
        data.write(Int.getvalue(cls.user_id))
        data.write(Vector().getvalue(cls.options, Bytes))
        return data.getvalue()


class UpdateDialogFilter(TL):
    ID = 0x26ffde7d

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


class UpdateDialogFilterOrder(TL):
    ID = 0xa5d72105

    def __init__(cls, order: List[int]):
        cls.order = order

    @staticmethod
    def read(data) -> "UpdateDialogFilterOrder":
        order = data.getobj(Int)
        return UpdateDialogFilterOrder(order=order)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.order, Int))
        return data.getvalue()


class UpdateDialogFilters(TL):
    ID = 0x3504914f

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UpdateDialogFilters":
        
        return UpdateDialogFilters()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UpdatePhoneCallSignalingData(TL):
    ID = 0x2661bf09

    def __init__(cls, phone_call_id: int, data: bytes):
        cls.phone_call_id = phone_call_id
        cls.data = data

    @staticmethod
    def read(data) -> "UpdatePhoneCallSignalingData":
        phone_call_id = Long.read(data)
        data = Bytes.read(data)
        return UpdatePhoneCallSignalingData(phone_call_id=phone_call_id, data=data)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.phone_call_id))
        data.write(Bytes.getvalue(cls.data))
        return data.getvalue()


class UpdateChannelMessageForwards(TL):
    ID = 0x6e8a84df

    def __init__(cls, channel_id: int, id: int, forwards: int):
        cls.channel_id = channel_id
        cls.id = id
        cls.forwards = forwards

    @staticmethod
    def read(data) -> "UpdateChannelMessageForwards":
        channel_id = Int.read(data)
        id = Int.read(data)
        forwards = Int.read(data)
        return UpdateChannelMessageForwards(channel_id=channel_id, id=id, forwards=forwards)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.channel_id))
        data.write(Int.getvalue(cls.id))
        data.write(Int.getvalue(cls.forwards))
        return data.getvalue()


class UpdateReadChannelDiscussionInbox(TL):
    ID = 0x1cc7de54

    def __init__(cls, channel_id: int, top_msg_id: int, read_max_id: int, broadcast_id: int = None, broadcast_post: int = None):
        cls.channel_id = channel_id
        cls.top_msg_id = top_msg_id
        cls.read_max_id = read_max_id
        cls.broadcast_id = broadcast_id
        cls.broadcast_post = broadcast_post

    @staticmethod
    def read(data) -> "UpdateReadChannelDiscussionInbox":
        flags = Int.read(data)
        channel_id = Int.read(data)
        top_msg_id = Int.read(data)
        read_max_id = Int.read(data)
        broadcast_id = Int.read(data) if flags & 1 else None
        broadcast_post = Int.read(data) if flags & 1 else None
        return UpdateReadChannelDiscussionInbox(channel_id=channel_id, top_msg_id=top_msg_id, read_max_id=read_max_id, broadcast_id=broadcast_id, broadcast_post=broadcast_post)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.broadcast_id is not None else 0
        flags |= 1 if cls.broadcast_post is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.channel_id))
        data.write(Int.getvalue(cls.top_msg_id))
        data.write(Int.getvalue(cls.read_max_id))
        
        if cls.broadcast_id is not None:
            data.write(Int.getvalue(cls.broadcast_id))
        
        if cls.broadcast_post is not None:
            data.write(Int.getvalue(cls.broadcast_post))
        return data.getvalue()


class UpdateReadChannelDiscussionOutbox(TL):
    ID = 0x4638a26c

    def __init__(cls, channel_id: int, top_msg_id: int, read_max_id: int):
        cls.channel_id = channel_id
        cls.top_msg_id = top_msg_id
        cls.read_max_id = read_max_id

    @staticmethod
    def read(data) -> "UpdateReadChannelDiscussionOutbox":
        channel_id = Int.read(data)
        top_msg_id = Int.read(data)
        read_max_id = Int.read(data)
        return UpdateReadChannelDiscussionOutbox(channel_id=channel_id, top_msg_id=top_msg_id, read_max_id=read_max_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.channel_id))
        data.write(Int.getvalue(cls.top_msg_id))
        data.write(Int.getvalue(cls.read_max_id))
        return data.getvalue()


class UpdatePeerBlocked(TL):
    ID = 0x246a4b22

    def __init__(cls, peer_id: TL, blocked: bool):
        cls.peer_id = peer_id
        cls.blocked = blocked

    @staticmethod
    def read(data) -> "UpdatePeerBlocked":
        peer_id = data.getobj()
        blocked = Bool.read(data)
        return UpdatePeerBlocked(peer_id=peer_id, blocked=blocked)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer_id.getvalue())
        data.write(Bool.getvalue(cls.blocked))
        return data.getvalue()


class UpdateChannelUserTyping(TL):
    ID = 0xff2abe9f

    def __init__(cls, channel_id: int, user_id: int, action: TL, top_msg_id: int = None):
        cls.channel_id = channel_id
        cls.top_msg_id = top_msg_id
        cls.user_id = user_id
        cls.action = action

    @staticmethod
    def read(data) -> "UpdateChannelUserTyping":
        flags = Int.read(data)
        channel_id = Int.read(data)
        top_msg_id = Int.read(data) if flags & 1 else None
        user_id = Int.read(data)
        action = data.getobj()
        return UpdateChannelUserTyping(channel_id=channel_id, top_msg_id=top_msg_id, user_id=user_id, action=action)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.top_msg_id is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.channel_id))
        
        if cls.top_msg_id is not None:
            data.write(Int.getvalue(cls.top_msg_id))
        data.write(Int.getvalue(cls.user_id))
        data.write(cls.action.getvalue())
        return data.getvalue()


class UpdatePinnedMessages(TL):
    ID = 0xed85eab5

    def __init__(cls, peer: TL, messages: List[int], pts: int, pts_count: int, pinned: bool = None):
        cls.pinned = pinned
        cls.peer = peer
        cls.messages = messages
        cls.pts = pts
        cls.pts_count = pts_count

    @staticmethod
    def read(data) -> "UpdatePinnedMessages":
        flags = Int.read(data)
        pinned = True if flags & 1 else False
        peer = data.getobj()
        messages = data.getobj(Int)
        pts = Int.read(data)
        pts_count = Int.read(data)
        return UpdatePinnedMessages(pinned=pinned, peer=peer, messages=messages, pts=pts, pts_count=pts_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.pinned is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        data.write(Vector().getvalue(cls.messages, Int))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        return data.getvalue()


class UpdatePinnedChannelMessages(TL):
    ID = 0x8588878b

    def __init__(cls, channel_id: int, messages: List[int], pts: int, pts_count: int, pinned: bool = None):
        cls.pinned = pinned
        cls.channel_id = channel_id
        cls.messages = messages
        cls.pts = pts
        cls.pts_count = pts_count

    @staticmethod
    def read(data) -> "UpdatePinnedChannelMessages":
        flags = Int.read(data)
        pinned = True if flags & 1 else False
        channel_id = Int.read(data)
        messages = data.getobj(Int)
        pts = Int.read(data)
        pts_count = Int.read(data)
        return UpdatePinnedChannelMessages(pinned=pinned, channel_id=channel_id, messages=messages, pts=pts, pts_count=pts_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.pinned is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.channel_id))
        data.write(Vector().getvalue(cls.messages, Int))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        return data.getvalue()


class UpdateChat(TL):
    ID = 0x1330a196

    def __init__(cls, chat_id: int):
        cls.chat_id = chat_id

    @staticmethod
    def read(data) -> "UpdateChat":
        chat_id = Int.read(data)
        return UpdateChat(chat_id=chat_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        return data.getvalue()


class UpdateGroupCallParticipants(TL):
    ID = 0xf2ebdb4e

    def __init__(cls, call: TL, participants: List[TL], version: int):
        cls.call = call
        cls.participants = participants
        cls.version = version

    @staticmethod
    def read(data) -> "UpdateGroupCallParticipants":
        call = data.getobj()
        participants = data.getobj()
        version = Int.read(data)
        return UpdateGroupCallParticipants(call=call, participants=participants, version=version)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.call.getvalue())
        data.write(Vector().getvalue(cls.participants))
        data.write(Int.getvalue(cls.version))
        return data.getvalue()


class UpdateGroupCall(TL):
    ID = 0xa45eb99b

    def __init__(cls, chat_id: int, call: TL):
        cls.chat_id = chat_id
        cls.call = call

    @staticmethod
    def read(data) -> "UpdateGroupCall":
        chat_id = Int.read(data)
        call = data.getobj()
        return UpdateGroupCall(chat_id=chat_id, call=call)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        data.write(cls.call.getvalue())
        return data.getvalue()


class UpdatePeerHistoryTTL(TL):
    ID = 0xbb9bb9a5

    def __init__(cls, peer: TL, ttl_period: int = None):
        cls.peer = peer
        cls.ttl_period = ttl_period

    @staticmethod
    def read(data) -> "UpdatePeerHistoryTTL":
        flags = Int.read(data)
        peer = data.getobj()
        ttl_period = Int.read(data) if flags & 1 else None
        return UpdatePeerHistoryTTL(peer=peer, ttl_period=ttl_period)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.ttl_period is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.peer.getvalue())
        
        if cls.ttl_period is not None:
            data.write(Int.getvalue(cls.ttl_period))
        return data.getvalue()


class UpdateChatParticipant(TL):
    ID = 0x609a6ed4

    def __init__(cls, chat_id: int, date: int, user_id: int, qts: int, prev_participant: TL = None, new_participant: TL = None):
        cls.chat_id = chat_id
        cls.date = date
        cls.user_id = user_id
        cls.prev_participant = prev_participant
        cls.new_participant = new_participant
        cls.qts = qts

    @staticmethod
    def read(data) -> "UpdateChatParticipant":
        flags = Int.read(data)
        chat_id = Int.read(data)
        date = Int.read(data)
        user_id = Int.read(data)
        prev_participant = data.getobj() if flags & 1 else None
        new_participant = data.getobj() if flags & 2 else None
        qts = Int.read(data)
        return UpdateChatParticipant(chat_id=chat_id, date=date, user_id=user_id, prev_participant=prev_participant, new_participant=new_participant, qts=qts)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.prev_participant is not None else 0
        flags |= 2 if cls.new_participant is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.chat_id))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.user_id))
        
        if cls.prev_participant is not None:
            data.write(cls.prev_participant.getvalue())
        
        if cls.new_participant is not None:
            data.write(cls.new_participant.getvalue())
        data.write(Int.getvalue(cls.qts))
        return data.getvalue()


class UpdateChannelParticipant(TL):
    ID = 0x65d2b464

    def __init__(cls, channel_id: int, date: int, user_id: int, qts: int, prev_participant: TL = None, new_participant: TL = None):
        cls.channel_id = channel_id
        cls.date = date
        cls.user_id = user_id
        cls.prev_participant = prev_participant
        cls.new_participant = new_participant
        cls.qts = qts

    @staticmethod
    def read(data) -> "UpdateChannelParticipant":
        flags = Int.read(data)
        channel_id = Int.read(data)
        date = Int.read(data)
        user_id = Int.read(data)
        prev_participant = data.getobj() if flags & 1 else None
        new_participant = data.getobj() if flags & 2 else None
        qts = Int.read(data)
        return UpdateChannelParticipant(channel_id=channel_id, date=date, user_id=user_id, prev_participant=prev_participant, new_participant=new_participant, qts=qts)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.prev_participant is not None else 0
        flags |= 2 if cls.new_participant is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.channel_id))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.user_id))
        
        if cls.prev_participant is not None:
            data.write(cls.prev_participant.getvalue())
        
        if cls.new_participant is not None:
            data.write(cls.new_participant.getvalue())
        data.write(Int.getvalue(cls.qts))
        return data.getvalue()


class UpdateBotStopped(TL):
    ID = 0x30ec6ebc

    def __init__(cls, user_id: int, stopped: bool, qts: int):
        cls.user_id = user_id
        cls.stopped = stopped
        cls.qts = qts

    @staticmethod
    def read(data) -> "UpdateBotStopped":
        user_id = Int.read(data)
        stopped = Bool.read(data)
        qts = Int.read(data)
        return UpdateBotStopped(user_id=user_id, stopped=stopped, qts=qts)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Bool.getvalue(cls.stopped))
        data.write(Int.getvalue(cls.qts))
        return data.getvalue()


class UpdatesTooLong(TL):
    ID = 0xe317af7e

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UpdatesTooLong":
        
        return UpdatesTooLong()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class UpdateShortMessage(TL):
    ID = 0xfaeff833

    def __init__(cls, id: int, user_id: int, message: str, pts: int, pts_count: int, date: int, out: bool = None, mentioned: bool = None, media_unread: bool = None, silent: bool = None, fwd_from: TL = None, via_bot_id: int = None, reply_to: TL = None, entities: List[TL] = None, ttl_period: int = None):
        cls.out = out
        cls.mentioned = mentioned
        cls.media_unread = media_unread
        cls.silent = silent
        cls.id = id
        cls.user_id = user_id
        cls.message = message
        cls.pts = pts
        cls.pts_count = pts_count
        cls.date = date
        cls.fwd_from = fwd_from
        cls.via_bot_id = via_bot_id
        cls.reply_to = reply_to
        cls.entities = entities
        cls.ttl_period = ttl_period

    @staticmethod
    def read(data) -> "UpdateShortMessage":
        flags = Int.read(data)
        out = True if flags & 2 else False
        mentioned = True if flags & 16 else False
        media_unread = True if flags & 32 else False
        silent = True if flags & 8192 else False
        id = Int.read(data)
        user_id = Int.read(data)
        message = String.read(data)
        pts = Int.read(data)
        pts_count = Int.read(data)
        date = Int.read(data)
        fwd_from = data.getobj() if flags & 4 else None
        via_bot_id = Int.read(data) if flags & 2048 else None
        reply_to = data.getobj() if flags & 8 else None
        entities = data.getobj() if flags & 128 else []
        ttl_period = Int.read(data) if flags & 33554432 else None
        return UpdateShortMessage(out=out, mentioned=mentioned, media_unread=media_unread, silent=silent, id=id, user_id=user_id, message=message, pts=pts, pts_count=pts_count, date=date, fwd_from=fwd_from, via_bot_id=via_bot_id, reply_to=reply_to, entities=entities, ttl_period=ttl_period)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.out is not None else 0
        flags |= 16 if cls.mentioned is not None else 0
        flags |= 32 if cls.media_unread is not None else 0
        flags |= 8192 if cls.silent is not None else 0
        flags |= 4 if cls.fwd_from is not None else 0
        flags |= 2048 if cls.via_bot_id is not None else 0
        flags |= 8 if cls.reply_to is not None else 0
        flags |= 128 if cls.entities is not None else 0
        flags |= 33554432 if cls.ttl_period is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        data.write(Int.getvalue(cls.user_id))
        data.write(String.getvalue(cls.message))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        data.write(Int.getvalue(cls.date))
        
        if cls.fwd_from is not None:
            data.write(cls.fwd_from.getvalue())
        
        if cls.via_bot_id is not None:
            data.write(Int.getvalue(cls.via_bot_id))
        
        if cls.reply_to is not None:
            data.write(cls.reply_to.getvalue())
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        
        if cls.ttl_period is not None:
            data.write(Int.getvalue(cls.ttl_period))
        return data.getvalue()


class UpdateShortChatMessage(TL):
    ID = 0x1157b858

    def __init__(cls, id: int, from_id: int, chat_id: int, message: str, pts: int, pts_count: int, date: int, out: bool = None, mentioned: bool = None, media_unread: bool = None, silent: bool = None, fwd_from: TL = None, via_bot_id: int = None, reply_to: TL = None, entities: List[TL] = None, ttl_period: int = None):
        cls.out = out
        cls.mentioned = mentioned
        cls.media_unread = media_unread
        cls.silent = silent
        cls.id = id
        cls.from_id = from_id
        cls.chat_id = chat_id
        cls.message = message
        cls.pts = pts
        cls.pts_count = pts_count
        cls.date = date
        cls.fwd_from = fwd_from
        cls.via_bot_id = via_bot_id
        cls.reply_to = reply_to
        cls.entities = entities
        cls.ttl_period = ttl_period

    @staticmethod
    def read(data) -> "UpdateShortChatMessage":
        flags = Int.read(data)
        out = True if flags & 2 else False
        mentioned = True if flags & 16 else False
        media_unread = True if flags & 32 else False
        silent = True if flags & 8192 else False
        id = Int.read(data)
        from_id = Int.read(data)
        chat_id = Int.read(data)
        message = String.read(data)
        pts = Int.read(data)
        pts_count = Int.read(data)
        date = Int.read(data)
        fwd_from = data.getobj() if flags & 4 else None
        via_bot_id = Int.read(data) if flags & 2048 else None
        reply_to = data.getobj() if flags & 8 else None
        entities = data.getobj() if flags & 128 else []
        ttl_period = Int.read(data) if flags & 33554432 else None
        return UpdateShortChatMessage(out=out, mentioned=mentioned, media_unread=media_unread, silent=silent, id=id, from_id=from_id, chat_id=chat_id, message=message, pts=pts, pts_count=pts_count, date=date, fwd_from=fwd_from, via_bot_id=via_bot_id, reply_to=reply_to, entities=entities, ttl_period=ttl_period)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.out is not None else 0
        flags |= 16 if cls.mentioned is not None else 0
        flags |= 32 if cls.media_unread is not None else 0
        flags |= 8192 if cls.silent is not None else 0
        flags |= 4 if cls.fwd_from is not None else 0
        flags |= 2048 if cls.via_bot_id is not None else 0
        flags |= 8 if cls.reply_to is not None else 0
        flags |= 128 if cls.entities is not None else 0
        flags |= 33554432 if cls.ttl_period is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        data.write(Int.getvalue(cls.from_id))
        data.write(Int.getvalue(cls.chat_id))
        data.write(String.getvalue(cls.message))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        data.write(Int.getvalue(cls.date))
        
        if cls.fwd_from is not None:
            data.write(cls.fwd_from.getvalue())
        
        if cls.via_bot_id is not None:
            data.write(Int.getvalue(cls.via_bot_id))
        
        if cls.reply_to is not None:
            data.write(cls.reply_to.getvalue())
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        
        if cls.ttl_period is not None:
            data.write(Int.getvalue(cls.ttl_period))
        return data.getvalue()


class UpdateShort(TL):
    ID = 0x78d4dec1

    def __init__(cls, update: TL, date: int):
        cls.update = update
        cls.date = date

    @staticmethod
    def read(data) -> "UpdateShort":
        update = data.getobj()
        date = Int.read(data)
        return UpdateShort(update=update, date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.update.getvalue())
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class UpdatesCombined(TL):
    ID = 0x725b04c3

    def __init__(cls, updates: List[TL], users: List[TL], chats: List[TL], date: int, seq_start: int, seq: int):
        cls.updates = updates
        cls.users = users
        cls.chats = chats
        cls.date = date
        cls.seq_start = seq_start
        cls.seq = seq

    @staticmethod
    def read(data) -> "UpdatesCombined":
        updates = data.getobj()
        users = data.getobj()
        chats = data.getobj()
        date = Int.read(data)
        seq_start = Int.read(data)
        seq = Int.read(data)
        return UpdatesCombined(updates=updates, users=users, chats=chats, date=date, seq_start=seq_start, seq=seq)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.updates))
        data.write(Vector().getvalue(cls.users))
        data.write(Vector().getvalue(cls.chats))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.seq_start))
        data.write(Int.getvalue(cls.seq))
        return data.getvalue()


class Updates(TL):
    ID = 0x74ae4240

    def __init__(cls, updates: List[TL], users: List[TL], chats: List[TL], date: int, seq: int):
        cls.updates = updates
        cls.users = users
        cls.chats = chats
        cls.date = date
        cls.seq = seq

    @staticmethod
    def read(data) -> "Updates":
        updates = data.getobj()
        users = data.getobj()
        chats = data.getobj()
        date = Int.read(data)
        seq = Int.read(data)
        return Updates(updates=updates, users=users, chats=chats, date=date, seq=seq)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.updates))
        data.write(Vector().getvalue(cls.users))
        data.write(Vector().getvalue(cls.chats))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.seq))
        return data.getvalue()


class UpdateShortSentMessage(TL):
    ID = 0x9015e101

    def __init__(cls, id: int, pts: int, pts_count: int, date: int, out: bool = None, media: TL = None, entities: List[TL] = None, ttl_period: int = None):
        cls.out = out
        cls.id = id
        cls.pts = pts
        cls.pts_count = pts_count
        cls.date = date
        cls.media = media
        cls.entities = entities
        cls.ttl_period = ttl_period

    @staticmethod
    def read(data) -> "UpdateShortSentMessage":
        flags = Int.read(data)
        out = True if flags & 2 else False
        id = Int.read(data)
        pts = Int.read(data)
        pts_count = Int.read(data)
        date = Int.read(data)
        media = data.getobj() if flags & 512 else None
        entities = data.getobj() if flags & 128 else []
        ttl_period = Int.read(data) if flags & 33554432 else None
        return UpdateShortSentMessage(out=out, id=id, pts=pts, pts_count=pts_count, date=date, media=media, entities=entities, ttl_period=ttl_period)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.out is not None else 0
        flags |= 512 if cls.media is not None else 0
        flags |= 128 if cls.entities is not None else 0
        flags |= 33554432 if cls.ttl_period is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        data.write(Int.getvalue(cls.pts))
        data.write(Int.getvalue(cls.pts_count))
        data.write(Int.getvalue(cls.date))
        
        if cls.media is not None:
            data.write(cls.media.getvalue())
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        
        if cls.ttl_period is not None:
            data.write(Int.getvalue(cls.ttl_period))
        return data.getvalue()


class DcOption(TL):
    ID = 0x18b7a10d

    def __init__(cls, id: int, ip_address: str, port: int, ipv6: bool = None, media_only: bool = None, tcpo_only: bool = None, cdn: bool = None, static: bool = None, secret: bytes = None):
        cls.ipv6 = ipv6
        cls.media_only = media_only
        cls.tcpo_only = tcpo_only
        cls.cdn = cdn
        cls.static = static
        cls.id = id
        cls.ip_address = ip_address
        cls.port = port
        cls.secret = secret

    @staticmethod
    def read(data) -> "DcOption":
        flags = Int.read(data)
        ipv6 = True if flags & 1 else False
        media_only = True if flags & 2 else False
        tcpo_only = True if flags & 4 else False
        cdn = True if flags & 8 else False
        static = True if flags & 16 else False
        id = Int.read(data)
        ip_address = String.read(data)
        port = Int.read(data)
        secret = Bytes.read(data) if flags & 1024 else None
        return DcOption(ipv6=ipv6, media_only=media_only, tcpo_only=tcpo_only, cdn=cdn, static=static, id=id, ip_address=ip_address, port=port, secret=secret)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.ipv6 is not None else 0
        flags |= 2 if cls.media_only is not None else 0
        flags |= 4 if cls.tcpo_only is not None else 0
        flags |= 8 if cls.cdn is not None else 0
        flags |= 16 if cls.static is not None else 0
        flags |= 1024 if cls.secret is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        data.write(String.getvalue(cls.ip_address))
        data.write(Int.getvalue(cls.port))
        
        if cls.secret is not None:
            data.write(Bytes.getvalue(cls.secret))
        return data.getvalue()


class Config(TL):
    ID = 0x330b4067

    def __init__(cls, date: int, expires: int, test_mode: bool, this_dc: int, dc_options: List[TL], dc_txt_domain_name: str, chat_size_max: int, megagroup_size_max: int, forwarded_count_max: int, online_update_period_ms: int, offline_blur_timeout_ms: int, offline_idle_timeout_ms: int, online_cloud_timeout_ms: int, notify_cloud_delay_ms: int, notify_default_delay_ms: int, push_chat_period_ms: int, push_chat_limit: int, saved_gifs_limit: int, edit_time_limit: int, revoke_time_limit: int, revoke_pm_time_limit: int, rating_e_decay: int, stickers_recent_limit: int, stickers_faved_limit: int, channels_read_media_period: int, pinned_dialogs_count_max: int, pinned_infolder_count_max: int, call_receive_timeout_ms: int, call_ring_timeout_ms: int, call_connect_timeout_ms: int, call_packet_timeout_ms: int, me_url_prefix: str, caption_length_max: int, message_length_max: int, webfile_dc_id: int, phonecalls_enabled: bool = None, default_p2p_contacts: bool = None, preload_featured_stickers: bool = None, ignore_phone_entities: bool = None, revoke_pm_inbox: bool = None, blocked_mode: bool = None, pfs_enabled: bool = None, tmp_sessions: int = None, autoupdate_url_prefix: str = None, gif_search_username: str = None, venue_search_username: str = None, img_search_username: str = None, static_maps_provider: str = None, suggested_lang_code: str = None, lang_pack_version: int = None, base_lang_pack_version: int = None):
        cls.phonecalls_enabled = phonecalls_enabled
        cls.default_p2p_contacts = default_p2p_contacts
        cls.preload_featured_stickers = preload_featured_stickers
        cls.ignore_phone_entities = ignore_phone_entities
        cls.revoke_pm_inbox = revoke_pm_inbox
        cls.blocked_mode = blocked_mode
        cls.pfs_enabled = pfs_enabled
        cls.date = date
        cls.expires = expires
        cls.test_mode = test_mode
        cls.this_dc = this_dc
        cls.dc_options = dc_options
        cls.dc_txt_domain_name = dc_txt_domain_name
        cls.chat_size_max = chat_size_max
        cls.megagroup_size_max = megagroup_size_max
        cls.forwarded_count_max = forwarded_count_max
        cls.online_update_period_ms = online_update_period_ms
        cls.offline_blur_timeout_ms = offline_blur_timeout_ms
        cls.offline_idle_timeout_ms = offline_idle_timeout_ms
        cls.online_cloud_timeout_ms = online_cloud_timeout_ms
        cls.notify_cloud_delay_ms = notify_cloud_delay_ms
        cls.notify_default_delay_ms = notify_default_delay_ms
        cls.push_chat_period_ms = push_chat_period_ms
        cls.push_chat_limit = push_chat_limit
        cls.saved_gifs_limit = saved_gifs_limit
        cls.edit_time_limit = edit_time_limit
        cls.revoke_time_limit = revoke_time_limit
        cls.revoke_pm_time_limit = revoke_pm_time_limit
        cls.rating_e_decay = rating_e_decay
        cls.stickers_recent_limit = stickers_recent_limit
        cls.stickers_faved_limit = stickers_faved_limit
        cls.channels_read_media_period = channels_read_media_period
        cls.tmp_sessions = tmp_sessions
        cls.pinned_dialogs_count_max = pinned_dialogs_count_max
        cls.pinned_infolder_count_max = pinned_infolder_count_max
        cls.call_receive_timeout_ms = call_receive_timeout_ms
        cls.call_ring_timeout_ms = call_ring_timeout_ms
        cls.call_connect_timeout_ms = call_connect_timeout_ms
        cls.call_packet_timeout_ms = call_packet_timeout_ms
        cls.me_url_prefix = me_url_prefix
        cls.autoupdate_url_prefix = autoupdate_url_prefix
        cls.gif_search_username = gif_search_username
        cls.venue_search_username = venue_search_username
        cls.img_search_username = img_search_username
        cls.static_maps_provider = static_maps_provider
        cls.caption_length_max = caption_length_max
        cls.message_length_max = message_length_max
        cls.webfile_dc_id = webfile_dc_id
        cls.suggested_lang_code = suggested_lang_code
        cls.lang_pack_version = lang_pack_version
        cls.base_lang_pack_version = base_lang_pack_version

    @staticmethod
    def read(data) -> "Config":
        flags = Int.read(data)
        phonecalls_enabled = True if flags & 2 else False
        default_p2p_contacts = True if flags & 8 else False
        preload_featured_stickers = True if flags & 16 else False
        ignore_phone_entities = True if flags & 32 else False
        revoke_pm_inbox = True if flags & 64 else False
        blocked_mode = True if flags & 256 else False
        pfs_enabled = True if flags & 8192 else False
        date = Int.read(data)
        expires = Int.read(data)
        test_mode = Bool.read(data)
        this_dc = Int.read(data)
        dc_options = data.getobj()
        dc_txt_domain_name = String.read(data)
        chat_size_max = Int.read(data)
        megagroup_size_max = Int.read(data)
        forwarded_count_max = Int.read(data)
        online_update_period_ms = Int.read(data)
        offline_blur_timeout_ms = Int.read(data)
        offline_idle_timeout_ms = Int.read(data)
        online_cloud_timeout_ms = Int.read(data)
        notify_cloud_delay_ms = Int.read(data)
        notify_default_delay_ms = Int.read(data)
        push_chat_period_ms = Int.read(data)
        push_chat_limit = Int.read(data)
        saved_gifs_limit = Int.read(data)
        edit_time_limit = Int.read(data)
        revoke_time_limit = Int.read(data)
        revoke_pm_time_limit = Int.read(data)
        rating_e_decay = Int.read(data)
        stickers_recent_limit = Int.read(data)
        stickers_faved_limit = Int.read(data)
        channels_read_media_period = Int.read(data)
        tmp_sessions = Int.read(data) if flags & 1 else None
        pinned_dialogs_count_max = Int.read(data)
        pinned_infolder_count_max = Int.read(data)
        call_receive_timeout_ms = Int.read(data)
        call_ring_timeout_ms = Int.read(data)
        call_connect_timeout_ms = Int.read(data)
        call_packet_timeout_ms = Int.read(data)
        me_url_prefix = String.read(data)
        autoupdate_url_prefix = String.read(data) if flags & 128 else None
        gif_search_username = String.read(data) if flags & 512 else None
        venue_search_username = String.read(data) if flags & 1024 else None
        img_search_username = String.read(data) if flags & 2048 else None
        static_maps_provider = String.read(data) if flags & 4096 else None
        caption_length_max = Int.read(data)
        message_length_max = Int.read(data)
        webfile_dc_id = Int.read(data)
        suggested_lang_code = String.read(data) if flags & 4 else None
        lang_pack_version = Int.read(data) if flags & 4 else None
        base_lang_pack_version = Int.read(data) if flags & 4 else None
        return Config(phonecalls_enabled=phonecalls_enabled, default_p2p_contacts=default_p2p_contacts, preload_featured_stickers=preload_featured_stickers, ignore_phone_entities=ignore_phone_entities, revoke_pm_inbox=revoke_pm_inbox, blocked_mode=blocked_mode, pfs_enabled=pfs_enabled, date=date, expires=expires, test_mode=test_mode, this_dc=this_dc, dc_options=dc_options, dc_txt_domain_name=dc_txt_domain_name, chat_size_max=chat_size_max, megagroup_size_max=megagroup_size_max, forwarded_count_max=forwarded_count_max, online_update_period_ms=online_update_period_ms, offline_blur_timeout_ms=offline_blur_timeout_ms, offline_idle_timeout_ms=offline_idle_timeout_ms, online_cloud_timeout_ms=online_cloud_timeout_ms, notify_cloud_delay_ms=notify_cloud_delay_ms, notify_default_delay_ms=notify_default_delay_ms, push_chat_period_ms=push_chat_period_ms, push_chat_limit=push_chat_limit, saved_gifs_limit=saved_gifs_limit, edit_time_limit=edit_time_limit, revoke_time_limit=revoke_time_limit, revoke_pm_time_limit=revoke_pm_time_limit, rating_e_decay=rating_e_decay, stickers_recent_limit=stickers_recent_limit, stickers_faved_limit=stickers_faved_limit, channels_read_media_period=channels_read_media_period, tmp_sessions=tmp_sessions, pinned_dialogs_count_max=pinned_dialogs_count_max, pinned_infolder_count_max=pinned_infolder_count_max, call_receive_timeout_ms=call_receive_timeout_ms, call_ring_timeout_ms=call_ring_timeout_ms, call_connect_timeout_ms=call_connect_timeout_ms, call_packet_timeout_ms=call_packet_timeout_ms, me_url_prefix=me_url_prefix, autoupdate_url_prefix=autoupdate_url_prefix, gif_search_username=gif_search_username, venue_search_username=venue_search_username, img_search_username=img_search_username, static_maps_provider=static_maps_provider, caption_length_max=caption_length_max, message_length_max=message_length_max, webfile_dc_id=webfile_dc_id, suggested_lang_code=suggested_lang_code, lang_pack_version=lang_pack_version, base_lang_pack_version=base_lang_pack_version)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.phonecalls_enabled is not None else 0
        flags |= 8 if cls.default_p2p_contacts is not None else 0
        flags |= 16 if cls.preload_featured_stickers is not None else 0
        flags |= 32 if cls.ignore_phone_entities is not None else 0
        flags |= 64 if cls.revoke_pm_inbox is not None else 0
        flags |= 256 if cls.blocked_mode is not None else 0
        flags |= 8192 if cls.pfs_enabled is not None else 0
        flags |= 1 if cls.tmp_sessions is not None else 0
        flags |= 128 if cls.autoupdate_url_prefix is not None else 0
        flags |= 512 if cls.gif_search_username is not None else 0
        flags |= 1024 if cls.venue_search_username is not None else 0
        flags |= 2048 if cls.img_search_username is not None else 0
        flags |= 4096 if cls.static_maps_provider is not None else 0
        flags |= 4 if cls.suggested_lang_code is not None else 0
        flags |= 4 if cls.lang_pack_version is not None else 0
        flags |= 4 if cls.base_lang_pack_version is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.expires))
        data.write(Bool.getvalue(cls.test_mode))
        data.write(Int.getvalue(cls.this_dc))
        data.write(Vector().getvalue(cls.dc_options))
        data.write(String.getvalue(cls.dc_txt_domain_name))
        data.write(Int.getvalue(cls.chat_size_max))
        data.write(Int.getvalue(cls.megagroup_size_max))
        data.write(Int.getvalue(cls.forwarded_count_max))
        data.write(Int.getvalue(cls.online_update_period_ms))
        data.write(Int.getvalue(cls.offline_blur_timeout_ms))
        data.write(Int.getvalue(cls.offline_idle_timeout_ms))
        data.write(Int.getvalue(cls.online_cloud_timeout_ms))
        data.write(Int.getvalue(cls.notify_cloud_delay_ms))
        data.write(Int.getvalue(cls.notify_default_delay_ms))
        data.write(Int.getvalue(cls.push_chat_period_ms))
        data.write(Int.getvalue(cls.push_chat_limit))
        data.write(Int.getvalue(cls.saved_gifs_limit))
        data.write(Int.getvalue(cls.edit_time_limit))
        data.write(Int.getvalue(cls.revoke_time_limit))
        data.write(Int.getvalue(cls.revoke_pm_time_limit))
        data.write(Int.getvalue(cls.rating_e_decay))
        data.write(Int.getvalue(cls.stickers_recent_limit))
        data.write(Int.getvalue(cls.stickers_faved_limit))
        data.write(Int.getvalue(cls.channels_read_media_period))
        
        if cls.tmp_sessions is not None:
            data.write(Int.getvalue(cls.tmp_sessions))
        data.write(Int.getvalue(cls.pinned_dialogs_count_max))
        data.write(Int.getvalue(cls.pinned_infolder_count_max))
        data.write(Int.getvalue(cls.call_receive_timeout_ms))
        data.write(Int.getvalue(cls.call_ring_timeout_ms))
        data.write(Int.getvalue(cls.call_connect_timeout_ms))
        data.write(Int.getvalue(cls.call_packet_timeout_ms))
        data.write(String.getvalue(cls.me_url_prefix))
        
        if cls.autoupdate_url_prefix is not None:
            data.write(String.getvalue(cls.autoupdate_url_prefix))
        
        if cls.gif_search_username is not None:
            data.write(String.getvalue(cls.gif_search_username))
        
        if cls.venue_search_username is not None:
            data.write(String.getvalue(cls.venue_search_username))
        
        if cls.img_search_username is not None:
            data.write(String.getvalue(cls.img_search_username))
        
        if cls.static_maps_provider is not None:
            data.write(String.getvalue(cls.static_maps_provider))
        data.write(Int.getvalue(cls.caption_length_max))
        data.write(Int.getvalue(cls.message_length_max))
        data.write(Int.getvalue(cls.webfile_dc_id))
        
        if cls.suggested_lang_code is not None:
            data.write(String.getvalue(cls.suggested_lang_code))
        
        if cls.lang_pack_version is not None:
            data.write(Int.getvalue(cls.lang_pack_version))
        
        if cls.base_lang_pack_version is not None:
            data.write(Int.getvalue(cls.base_lang_pack_version))
        return data.getvalue()


class NearestDc(TL):
    ID = 0x8e1a1775

    def __init__(cls, country: str, this_dc: int, nearest_dc: int):
        cls.country = country
        cls.this_dc = this_dc
        cls.nearest_dc = nearest_dc

    @staticmethod
    def read(data) -> "NearestDc":
        country = String.read(data)
        this_dc = Int.read(data)
        nearest_dc = Int.read(data)
        return NearestDc(country=country, this_dc=this_dc, nearest_dc=nearest_dc)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.country))
        data.write(Int.getvalue(cls.this_dc))
        data.write(Int.getvalue(cls.nearest_dc))
        return data.getvalue()


class EncryptedChatEmpty(TL):
    ID = 0xab7ec0a0

    def __init__(cls, id: int):
        cls.id = id

    @staticmethod
    def read(data) -> "EncryptedChatEmpty":
        id = Int.read(data)
        return EncryptedChatEmpty(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.id))
        return data.getvalue()


class EncryptedChatWaiting(TL):
    ID = 0x3bf703dc

    def __init__(cls, id: int, access_hash: int, date: int, admin_id: int, participant_id: int):
        cls.id = id
        cls.access_hash = access_hash
        cls.date = date
        cls.admin_id = admin_id
        cls.participant_id = participant_id

    @staticmethod
    def read(data) -> "EncryptedChatWaiting":
        id = Int.read(data)
        access_hash = Long.read(data)
        date = Int.read(data)
        admin_id = Int.read(data)
        participant_id = Int.read(data)
        return EncryptedChatWaiting(id=id, access_hash=access_hash, date=date, admin_id=admin_id, participant_id=participant_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.admin_id))
        data.write(Int.getvalue(cls.participant_id))
        return data.getvalue()


class EncryptedChatRequested(TL):
    ID = 0x62718a82

    def __init__(cls, id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_a: bytes, folder_id: int = None):
        cls.folder_id = folder_id
        cls.id = id
        cls.access_hash = access_hash
        cls.date = date
        cls.admin_id = admin_id
        cls.participant_id = participant_id
        cls.g_a = g_a

    @staticmethod
    def read(data) -> "EncryptedChatRequested":
        flags = Int.read(data)
        folder_id = Int.read(data) if flags & 1 else None
        id = Int.read(data)
        access_hash = Long.read(data)
        date = Int.read(data)
        admin_id = Int.read(data)
        participant_id = Int.read(data)
        g_a = Bytes.read(data)
        return EncryptedChatRequested(folder_id=folder_id, id=id, access_hash=access_hash, date=date, admin_id=admin_id, participant_id=participant_id, g_a=g_a)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.folder_id is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.folder_id is not None:
            data.write(Int.getvalue(cls.folder_id))
        data.write(Int.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.admin_id))
        data.write(Int.getvalue(cls.participant_id))
        data.write(Bytes.getvalue(cls.g_a))
        return data.getvalue()


class EncryptedChat(TL):
    ID = 0xfa56ce36

    def __init__(cls, id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_a_or_b: bytes, key_fingerprint: int):
        cls.id = id
        cls.access_hash = access_hash
        cls.date = date
        cls.admin_id = admin_id
        cls.participant_id = participant_id
        cls.g_a_or_b = g_a_or_b
        cls.key_fingerprint = key_fingerprint

    @staticmethod
    def read(data) -> "EncryptedChat":
        id = Int.read(data)
        access_hash = Long.read(data)
        date = Int.read(data)
        admin_id = Int.read(data)
        participant_id = Int.read(data)
        g_a_or_b = Bytes.read(data)
        key_fingerprint = Long.read(data)
        return EncryptedChat(id=id, access_hash=access_hash, date=date, admin_id=admin_id, participant_id=participant_id, g_a_or_b=g_a_or_b, key_fingerprint=key_fingerprint)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.admin_id))
        data.write(Int.getvalue(cls.participant_id))
        data.write(Bytes.getvalue(cls.g_a_or_b))
        data.write(Long.getvalue(cls.key_fingerprint))
        return data.getvalue()


class EncryptedChatDiscarded(TL):
    ID = 0x1e1c7c45

    def __init__(cls, id: int, history_deleted: bool = None):
        cls.history_deleted = history_deleted
        cls.id = id

    @staticmethod
    def read(data) -> "EncryptedChatDiscarded":
        flags = Int.read(data)
        history_deleted = True if flags & 1 else False
        id = Int.read(data)
        return EncryptedChatDiscarded(history_deleted=history_deleted, id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.history_deleted is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        return data.getvalue()


class InputEncryptedChat(TL):
    ID = 0xf141b5e1

    def __init__(cls, chat_id: int, access_hash: int):
        cls.chat_id = chat_id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputEncryptedChat":
        chat_id = Int.read(data)
        access_hash = Long.read(data)
        return InputEncryptedChat(chat_id=chat_id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.chat_id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class EncryptedFileEmpty(TL):
    ID = 0xc21f497e

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "EncryptedFileEmpty":
        
        return EncryptedFileEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class EncryptedFile(TL):
    ID = 0x4a70994c

    def __init__(cls, id: int, access_hash: int, size: int, dc_id: int, key_fingerprint: int):
        cls.id = id
        cls.access_hash = access_hash
        cls.size = size
        cls.dc_id = dc_id
        cls.key_fingerprint = key_fingerprint

    @staticmethod
    def read(data) -> "EncryptedFile":
        id = Long.read(data)
        access_hash = Long.read(data)
        size = Int.read(data)
        dc_id = Int.read(data)
        key_fingerprint = Int.read(data)
        return EncryptedFile(id=id, access_hash=access_hash, size=size, dc_id=dc_id, key_fingerprint=key_fingerprint)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Int.getvalue(cls.size))
        data.write(Int.getvalue(cls.dc_id))
        data.write(Int.getvalue(cls.key_fingerprint))
        return data.getvalue()


class InputEncryptedFileEmpty(TL):
    ID = 0x1837c364

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputEncryptedFileEmpty":
        
        return InputEncryptedFileEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputEncryptedFileUploaded(TL):
    ID = 0x64bd0306

    def __init__(cls, id: int, parts: int, md5_checksum: str, key_fingerprint: int):
        cls.id = id
        cls.parts = parts
        cls.md5_checksum = md5_checksum
        cls.key_fingerprint = key_fingerprint

    @staticmethod
    def read(data) -> "InputEncryptedFileUploaded":
        id = Long.read(data)
        parts = Int.read(data)
        md5_checksum = String.read(data)
        key_fingerprint = Int.read(data)
        return InputEncryptedFileUploaded(id=id, parts=parts, md5_checksum=md5_checksum, key_fingerprint=key_fingerprint)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Int.getvalue(cls.parts))
        data.write(String.getvalue(cls.md5_checksum))
        data.write(Int.getvalue(cls.key_fingerprint))
        return data.getvalue()


class InputEncryptedFile(TL):
    ID = 0x5a17b5e5

    def __init__(cls, id: int, access_hash: int):
        cls.id = id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputEncryptedFile":
        id = Long.read(data)
        access_hash = Long.read(data)
        return InputEncryptedFile(id=id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class InputEncryptedFileBigUploaded(TL):
    ID = 0x2dc173c8

    def __init__(cls, id: int, parts: int, key_fingerprint: int):
        cls.id = id
        cls.parts = parts
        cls.key_fingerprint = key_fingerprint

    @staticmethod
    def read(data) -> "InputEncryptedFileBigUploaded":
        id = Long.read(data)
        parts = Int.read(data)
        key_fingerprint = Int.read(data)
        return InputEncryptedFileBigUploaded(id=id, parts=parts, key_fingerprint=key_fingerprint)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Int.getvalue(cls.parts))
        data.write(Int.getvalue(cls.key_fingerprint))
        return data.getvalue()


class EncryptedMessage(TL):
    ID = 0xed18c118

    def __init__(cls, random_id: int, chat_id: int, date: int, bytes: bytes, file: TL):
        cls.random_id = random_id
        cls.chat_id = chat_id
        cls.date = date
        cls.bytes = bytes
        cls.file = file

    @staticmethod
    def read(data) -> "EncryptedMessage":
        random_id = Long.read(data)
        chat_id = Int.read(data)
        date = Int.read(data)
        bytes = Bytes.read(data)
        file = data.getobj()
        return EncryptedMessage(random_id=random_id, chat_id=chat_id, date=date, bytes=bytes, file=file)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.random_id))
        data.write(Int.getvalue(cls.chat_id))
        data.write(Int.getvalue(cls.date))
        data.write(Bytes.getvalue(cls.bytes))
        data.write(cls.file.getvalue())
        return data.getvalue()


class EncryptedMessageService(TL):
    ID = 0x23734b06

    def __init__(cls, random_id: int, chat_id: int, date: int, bytes: bytes):
        cls.random_id = random_id
        cls.chat_id = chat_id
        cls.date = date
        cls.bytes = bytes

    @staticmethod
    def read(data) -> "EncryptedMessageService":
        random_id = Long.read(data)
        chat_id = Int.read(data)
        date = Int.read(data)
        bytes = Bytes.read(data)
        return EncryptedMessageService(random_id=random_id, chat_id=chat_id, date=date, bytes=bytes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.random_id))
        data.write(Int.getvalue(cls.chat_id))
        data.write(Int.getvalue(cls.date))
        data.write(Bytes.getvalue(cls.bytes))
        return data.getvalue()


class InputDocumentEmpty(TL):
    ID = 0x72f0eaae

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputDocumentEmpty":
        
        return InputDocumentEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputDocument(TL):
    ID = 0x1abfb575

    def __init__(cls, id: int, access_hash: int, file_reference: bytes):
        cls.id = id
        cls.access_hash = access_hash
        cls.file_reference = file_reference

    @staticmethod
    def read(data) -> "InputDocument":
        id = Long.read(data)
        access_hash = Long.read(data)
        file_reference = Bytes.read(data)
        return InputDocument(id=id, access_hash=access_hash, file_reference=file_reference)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Bytes.getvalue(cls.file_reference))
        return data.getvalue()


class DocumentEmpty(TL):
    ID = 0x36f8c871

    def __init__(cls, id: int):
        cls.id = id

    @staticmethod
    def read(data) -> "DocumentEmpty":
        id = Long.read(data)
        return DocumentEmpty(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        return data.getvalue()


class Document(TL):
    ID = 0x1e87342b

    def __init__(cls, id: int, access_hash: int, file_reference: bytes, date: int, mime_type: str, size: int, dc_id: int, attributes: List[TL], thumbs: List[TL] = None, video_thumbs: List[TL] = None):
        cls.id = id
        cls.access_hash = access_hash
        cls.file_reference = file_reference
        cls.date = date
        cls.mime_type = mime_type
        cls.size = size
        cls.thumbs = thumbs
        cls.video_thumbs = video_thumbs
        cls.dc_id = dc_id
        cls.attributes = attributes

    @staticmethod
    def read(data) -> "Document":
        flags = Int.read(data)
        id = Long.read(data)
        access_hash = Long.read(data)
        file_reference = Bytes.read(data)
        date = Int.read(data)
        mime_type = String.read(data)
        size = Int.read(data)
        thumbs = data.getobj() if flags & 1 else []
        video_thumbs = data.getobj() if flags & 2 else []
        dc_id = Int.read(data)
        attributes = data.getobj()
        return Document(id=id, access_hash=access_hash, file_reference=file_reference, date=date, mime_type=mime_type, size=size, thumbs=thumbs, video_thumbs=video_thumbs, dc_id=dc_id, attributes=attributes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.thumbs is not None else 0
        flags |= 2 if cls.video_thumbs is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Bytes.getvalue(cls.file_reference))
        data.write(Int.getvalue(cls.date))
        data.write(String.getvalue(cls.mime_type))
        data.write(Int.getvalue(cls.size))
        
        if cls.thumbs is not None:
            data.write(Vector().getvalue(cls.thumbs))
        
        if cls.video_thumbs is not None:
            data.write(Vector().getvalue(cls.video_thumbs))
        data.write(Int.getvalue(cls.dc_id))
        data.write(Vector().getvalue(cls.attributes))
        return data.getvalue()


class NotifyPeer(TL):
    ID = 0x9fd40bd8

    def __init__(cls, peer: TL):
        cls.peer = peer

    @staticmethod
    def read(data) -> "NotifyPeer":
        peer = data.getobj()
        return NotifyPeer(peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class NotifyUsers(TL):
    ID = 0xb4c83b4c

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "NotifyUsers":
        
        return NotifyUsers()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class NotifyChats(TL):
    ID = 0xc007cec3

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "NotifyChats":
        
        return NotifyChats()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class NotifyBroadcasts(TL):
    ID = 0xd612e8ef

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "NotifyBroadcasts":
        
        return NotifyBroadcasts()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SendMessageTypingAction(TL):
    ID = 0x16bf744e

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SendMessageTypingAction":
        
        return SendMessageTypingAction()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SendMessageCancelAction(TL):
    ID = 0xfd5ec8f5

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SendMessageCancelAction":
        
        return SendMessageCancelAction()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SendMessageRecordVideoAction(TL):
    ID = 0xa187d66f

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SendMessageRecordVideoAction":
        
        return SendMessageRecordVideoAction()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SendMessageUploadVideoAction(TL):
    ID = 0xe9763aec

    def __init__(cls, progress: int):
        cls.progress = progress

    @staticmethod
    def read(data) -> "SendMessageUploadVideoAction":
        progress = Int.read(data)
        return SendMessageUploadVideoAction(progress=progress)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.progress))
        return data.getvalue()


class SendMessageRecordAudioAction(TL):
    ID = 0xd52f73f7

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SendMessageRecordAudioAction":
        
        return SendMessageRecordAudioAction()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SendMessageUploadAudioAction(TL):
    ID = 0xf351d7ab

    def __init__(cls, progress: int):
        cls.progress = progress

    @staticmethod
    def read(data) -> "SendMessageUploadAudioAction":
        progress = Int.read(data)
        return SendMessageUploadAudioAction(progress=progress)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.progress))
        return data.getvalue()


class SendMessageUploadPhotoAction(TL):
    ID = 0xd1d34a26

    def __init__(cls, progress: int):
        cls.progress = progress

    @staticmethod
    def read(data) -> "SendMessageUploadPhotoAction":
        progress = Int.read(data)
        return SendMessageUploadPhotoAction(progress=progress)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.progress))
        return data.getvalue()


class SendMessageUploadDocumentAction(TL):
    ID = 0xaa0cd9e4

    def __init__(cls, progress: int):
        cls.progress = progress

    @staticmethod
    def read(data) -> "SendMessageUploadDocumentAction":
        progress = Int.read(data)
        return SendMessageUploadDocumentAction(progress=progress)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.progress))
        return data.getvalue()


class SendMessageGeoLocationAction(TL):
    ID = 0x176f8ba1

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SendMessageGeoLocationAction":
        
        return SendMessageGeoLocationAction()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SendMessageChooseContactAction(TL):
    ID = 0x628cbc6f

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SendMessageChooseContactAction":
        
        return SendMessageChooseContactAction()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SendMessageGamePlayAction(TL):
    ID = 0xdd6a8f48

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SendMessageGamePlayAction":
        
        return SendMessageGamePlayAction()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SendMessageRecordRoundAction(TL):
    ID = 0x88f27fbc

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SendMessageRecordRoundAction":
        
        return SendMessageRecordRoundAction()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SendMessageUploadRoundAction(TL):
    ID = 0x243e1c66

    def __init__(cls, progress: int):
        cls.progress = progress

    @staticmethod
    def read(data) -> "SendMessageUploadRoundAction":
        progress = Int.read(data)
        return SendMessageUploadRoundAction(progress=progress)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.progress))
        return data.getvalue()


class SpeakingInGroupCallAction(TL):
    ID = 0xd92c2285

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SpeakingInGroupCallAction":
        
        return SpeakingInGroupCallAction()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SendMessageHistoryImportAction(TL):
    ID = 0xdbda9246

    def __init__(cls, progress: int):
        cls.progress = progress

    @staticmethod
    def read(data) -> "SendMessageHistoryImportAction":
        progress = Int.read(data)
        return SendMessageHistoryImportAction(progress=progress)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.progress))
        return data.getvalue()


class InputPrivacyKeyStatusTimestamp(TL):
    ID = 0x4f96cb18

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputPrivacyKeyStatusTimestamp":
        
        return InputPrivacyKeyStatusTimestamp()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPrivacyKeyChatInvite(TL):
    ID = 0xbdfb0426

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputPrivacyKeyChatInvite":
        
        return InputPrivacyKeyChatInvite()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPrivacyKeyPhoneCall(TL):
    ID = 0xfabadc5f

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputPrivacyKeyPhoneCall":
        
        return InputPrivacyKeyPhoneCall()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPrivacyKeyPhoneP2P(TL):
    ID = 0xdb9e70d2

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputPrivacyKeyPhoneP2P":
        
        return InputPrivacyKeyPhoneP2P()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPrivacyKeyForwards(TL):
    ID = 0xa4dd4c08

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputPrivacyKeyForwards":
        
        return InputPrivacyKeyForwards()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPrivacyKeyProfilePhoto(TL):
    ID = 0x5719bacc

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputPrivacyKeyProfilePhoto":
        
        return InputPrivacyKeyProfilePhoto()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPrivacyKeyPhoneNumber(TL):
    ID = 0x352dafa

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputPrivacyKeyPhoneNumber":
        
        return InputPrivacyKeyPhoneNumber()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPrivacyKeyAddedByPhone(TL):
    ID = 0xd1219bdd

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputPrivacyKeyAddedByPhone":
        
        return InputPrivacyKeyAddedByPhone()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PrivacyKeyStatusTimestamp(TL):
    ID = 0xbc2eab30

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PrivacyKeyStatusTimestamp":
        
        return PrivacyKeyStatusTimestamp()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PrivacyKeyChatInvite(TL):
    ID = 0x500e6dfa

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PrivacyKeyChatInvite":
        
        return PrivacyKeyChatInvite()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PrivacyKeyPhoneCall(TL):
    ID = 0x3d662b7b

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PrivacyKeyPhoneCall":
        
        return PrivacyKeyPhoneCall()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PrivacyKeyPhoneP2P(TL):
    ID = 0x39491cc8

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PrivacyKeyPhoneP2P":
        
        return PrivacyKeyPhoneP2P()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PrivacyKeyForwards(TL):
    ID = 0x69ec56a3

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PrivacyKeyForwards":
        
        return PrivacyKeyForwards()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PrivacyKeyProfilePhoto(TL):
    ID = 0x96151fed

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PrivacyKeyProfilePhoto":
        
        return PrivacyKeyProfilePhoto()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PrivacyKeyPhoneNumber(TL):
    ID = 0xd19ae46d

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PrivacyKeyPhoneNumber":
        
        return PrivacyKeyPhoneNumber()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PrivacyKeyAddedByPhone(TL):
    ID = 0x42ffd42b

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PrivacyKeyAddedByPhone":
        
        return PrivacyKeyAddedByPhone()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPrivacyValueAllowContacts(TL):
    ID = 0xd09e07b

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputPrivacyValueAllowContacts":
        
        return InputPrivacyValueAllowContacts()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPrivacyValueAllowAll(TL):
    ID = 0x184b35ce

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputPrivacyValueAllowAll":
        
        return InputPrivacyValueAllowAll()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPrivacyValueAllowUsers(TL):
    ID = 0x131cc67f

    def __init__(cls, users: List[TL]):
        cls.users = users

    @staticmethod
    def read(data) -> "InputPrivacyValueAllowUsers":
        users = data.getobj()
        return InputPrivacyValueAllowUsers(users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class InputPrivacyValueDisallowContacts(TL):
    ID = 0xba52007

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputPrivacyValueDisallowContacts":
        
        return InputPrivacyValueDisallowContacts()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPrivacyValueDisallowAll(TL):
    ID = 0xd66b66c9

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputPrivacyValueDisallowAll":
        
        return InputPrivacyValueDisallowAll()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputPrivacyValueDisallowUsers(TL):
    ID = 0x90110467

    def __init__(cls, users: List[TL]):
        cls.users = users

    @staticmethod
    def read(data) -> "InputPrivacyValueDisallowUsers":
        users = data.getobj()
        return InputPrivacyValueDisallowUsers(users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class InputPrivacyValueAllowChatParticipants(TL):
    ID = 0x4c81c1ba

    def __init__(cls, chats: List[int]):
        cls.chats = chats

    @staticmethod
    def read(data) -> "InputPrivacyValueAllowChatParticipants":
        chats = data.getobj(Int)
        return InputPrivacyValueAllowChatParticipants(chats=chats)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.chats, Int))
        return data.getvalue()


class InputPrivacyValueDisallowChatParticipants(TL):
    ID = 0xd82363af

    def __init__(cls, chats: List[int]):
        cls.chats = chats

    @staticmethod
    def read(data) -> "InputPrivacyValueDisallowChatParticipants":
        chats = data.getobj(Int)
        return InputPrivacyValueDisallowChatParticipants(chats=chats)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.chats, Int))
        return data.getvalue()


class PrivacyValueAllowContacts(TL):
    ID = 0xfffe1bac

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PrivacyValueAllowContacts":
        
        return PrivacyValueAllowContacts()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PrivacyValueAllowAll(TL):
    ID = 0x65427b82

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PrivacyValueAllowAll":
        
        return PrivacyValueAllowAll()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PrivacyValueAllowUsers(TL):
    ID = 0x4d5bbe0c

    def __init__(cls, users: List[int]):
        cls.users = users

    @staticmethod
    def read(data) -> "PrivacyValueAllowUsers":
        users = data.getobj(Int)
        return PrivacyValueAllowUsers(users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.users, Int))
        return data.getvalue()


class PrivacyValueDisallowContacts(TL):
    ID = 0xf888fa1a

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PrivacyValueDisallowContacts":
        
        return PrivacyValueDisallowContacts()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PrivacyValueDisallowAll(TL):
    ID = 0x8b73e763

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PrivacyValueDisallowAll":
        
        return PrivacyValueDisallowAll()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PrivacyValueDisallowUsers(TL):
    ID = 0xc7f49b7

    def __init__(cls, users: List[int]):
        cls.users = users

    @staticmethod
    def read(data) -> "PrivacyValueDisallowUsers":
        users = data.getobj(Int)
        return PrivacyValueDisallowUsers(users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.users, Int))
        return data.getvalue()


class PrivacyValueAllowChatParticipants(TL):
    ID = 0x18be796b

    def __init__(cls, chats: List[int]):
        cls.chats = chats

    @staticmethod
    def read(data) -> "PrivacyValueAllowChatParticipants":
        chats = data.getobj(Int)
        return PrivacyValueAllowChatParticipants(chats=chats)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.chats, Int))
        return data.getvalue()


class PrivacyValueDisallowChatParticipants(TL):
    ID = 0xacae0690

    def __init__(cls, chats: List[int]):
        cls.chats = chats

    @staticmethod
    def read(data) -> "PrivacyValueDisallowChatParticipants":
        chats = data.getobj(Int)
        return PrivacyValueDisallowChatParticipants(chats=chats)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.chats, Int))
        return data.getvalue()


class AccountDaysTTL(TL):
    ID = 0xb8d0afdf

    def __init__(cls, days: int):
        cls.days = days

    @staticmethod
    def read(data) -> "AccountDaysTTL":
        days = Int.read(data)
        return AccountDaysTTL(days=days)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.days))
        return data.getvalue()


class DocumentAttributeImageSize(TL):
    ID = 0x6c37c15c

    def __init__(cls, w: int, h: int):
        cls.w = w
        cls.h = h

    @staticmethod
    def read(data) -> "DocumentAttributeImageSize":
        w = Int.read(data)
        h = Int.read(data)
        return DocumentAttributeImageSize(w=w, h=h)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.w))
        data.write(Int.getvalue(cls.h))
        return data.getvalue()


class DocumentAttributeAnimated(TL):
    ID = 0x11b58939

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "DocumentAttributeAnimated":
        
        return DocumentAttributeAnimated()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class DocumentAttributeSticker(TL):
    ID = 0x6319d612

    def __init__(cls, alt: str, stickerset: TL, mask: bool = None, mask_coords: TL = None):
        cls.mask = mask
        cls.alt = alt
        cls.stickerset = stickerset
        cls.mask_coords = mask_coords

    @staticmethod
    def read(data) -> "DocumentAttributeSticker":
        flags = Int.read(data)
        mask = True if flags & 2 else False
        alt = String.read(data)
        stickerset = data.getobj()
        mask_coords = data.getobj() if flags & 1 else None
        return DocumentAttributeSticker(mask=mask, alt=alt, stickerset=stickerset, mask_coords=mask_coords)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.mask is not None else 0
        flags |= 1 if cls.mask_coords is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.alt))
        data.write(cls.stickerset.getvalue())
        
        if cls.mask_coords is not None:
            data.write(cls.mask_coords.getvalue())
        return data.getvalue()


class DocumentAttributeVideo(TL):
    ID = 0xef02ce6

    def __init__(cls, duration: int, w: int, h: int, round_message: bool = None, supports_streaming: bool = None):
        cls.round_message = round_message
        cls.supports_streaming = supports_streaming
        cls.duration = duration
        cls.w = w
        cls.h = h

    @staticmethod
    def read(data) -> "DocumentAttributeVideo":
        flags = Int.read(data)
        round_message = True if flags & 1 else False
        supports_streaming = True if flags & 2 else False
        duration = Int.read(data)
        w = Int.read(data)
        h = Int.read(data)
        return DocumentAttributeVideo(round_message=round_message, supports_streaming=supports_streaming, duration=duration, w=w, h=h)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.round_message is not None else 0
        flags |= 2 if cls.supports_streaming is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.duration))
        data.write(Int.getvalue(cls.w))
        data.write(Int.getvalue(cls.h))
        return data.getvalue()


class DocumentAttributeAudio(TL):
    ID = 0x9852f9c6

    def __init__(cls, duration: int, voice: bool = None, title: str = None, performer: str = None, waveform: bytes = None):
        cls.voice = voice
        cls.duration = duration
        cls.title = title
        cls.performer = performer
        cls.waveform = waveform

    @staticmethod
    def read(data) -> "DocumentAttributeAudio":
        flags = Int.read(data)
        voice = True if flags & 1024 else False
        duration = Int.read(data)
        title = String.read(data) if flags & 1 else None
        performer = String.read(data) if flags & 2 else None
        waveform = Bytes.read(data) if flags & 4 else None
        return DocumentAttributeAudio(voice=voice, duration=duration, title=title, performer=performer, waveform=waveform)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1024 if cls.voice is not None else 0
        flags |= 1 if cls.title is not None else 0
        flags |= 2 if cls.performer is not None else 0
        flags |= 4 if cls.waveform is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.duration))
        
        if cls.title is not None:
            data.write(String.getvalue(cls.title))
        
        if cls.performer is not None:
            data.write(String.getvalue(cls.performer))
        
        if cls.waveform is not None:
            data.write(Bytes.getvalue(cls.waveform))
        return data.getvalue()


class DocumentAttributeFilename(TL):
    ID = 0x15590068

    def __init__(cls, file_name: str):
        cls.file_name = file_name

    @staticmethod
    def read(data) -> "DocumentAttributeFilename":
        file_name = String.read(data)
        return DocumentAttributeFilename(file_name=file_name)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.file_name))
        return data.getvalue()


class DocumentAttributeHasStickers(TL):
    ID = 0x9801d2f7

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "DocumentAttributeHasStickers":
        
        return DocumentAttributeHasStickers()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class StickerPack(TL):
    ID = 0x12b299d4

    def __init__(cls, emoticon: str, documents: List[int]):
        cls.emoticon = emoticon
        cls.documents = documents

    @staticmethod
    def read(data) -> "StickerPack":
        emoticon = String.read(data)
        documents = data.getobj(Long)
        return StickerPack(emoticon=emoticon, documents=documents)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.emoticon))
        data.write(Vector().getvalue(cls.documents, Long))
        return data.getvalue()


class WebPageEmpty(TL):
    ID = 0xeb1477e8

    def __init__(cls, id: int):
        cls.id = id

    @staticmethod
    def read(data) -> "WebPageEmpty":
        id = Long.read(data)
        return WebPageEmpty(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        return data.getvalue()


class WebPagePending(TL):
    ID = 0xc586da1c

    def __init__(cls, id: int, date: int):
        cls.id = id
        cls.date = date

    @staticmethod
    def read(data) -> "WebPagePending":
        id = Long.read(data)
        date = Int.read(data)
        return WebPagePending(id=id, date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class WebPage(TL):
    ID = 0xe89c45b2

    def __init__(cls, id: int, url: str, display_url: str, hash: int, type: str = None, site_name: str = None, title: str = None, description: str = None, photo: TL = None, embed_url: str = None, embed_type: str = None, embed_width: int = None, embed_height: int = None, duration: int = None, author: str = None, document: TL = None, cached_page: TL = None, attributes: List[TL] = None):
        cls.id = id
        cls.url = url
        cls.display_url = display_url
        cls.hash = hash
        cls.type = type
        cls.site_name = site_name
        cls.title = title
        cls.description = description
        cls.photo = photo
        cls.embed_url = embed_url
        cls.embed_type = embed_type
        cls.embed_width = embed_width
        cls.embed_height = embed_height
        cls.duration = duration
        cls.author = author
        cls.document = document
        cls.cached_page = cached_page
        cls.attributes = attributes

    @staticmethod
    def read(data) -> "WebPage":
        flags = Int.read(data)
        id = Long.read(data)
        url = String.read(data)
        display_url = String.read(data)
        hash = Int.read(data)
        type = String.read(data) if flags & 1 else None
        site_name = String.read(data) if flags & 2 else None
        title = String.read(data) if flags & 4 else None
        description = String.read(data) if flags & 8 else None
        photo = data.getobj() if flags & 16 else None
        embed_url = String.read(data) if flags & 32 else None
        embed_type = String.read(data) if flags & 32 else None
        embed_width = Int.read(data) if flags & 64 else None
        embed_height = Int.read(data) if flags & 64 else None
        duration = Int.read(data) if flags & 128 else None
        author = String.read(data) if flags & 256 else None
        document = data.getobj() if flags & 512 else None
        cached_page = data.getobj() if flags & 1024 else None
        attributes = data.getobj() if flags & 4096 else []
        return WebPage(id=id, url=url, display_url=display_url, hash=hash, type=type, site_name=site_name, title=title, description=description, photo=photo, embed_url=embed_url, embed_type=embed_type, embed_width=embed_width, embed_height=embed_height, duration=duration, author=author, document=document, cached_page=cached_page, attributes=attributes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.type is not None else 0
        flags |= 2 if cls.site_name is not None else 0
        flags |= 4 if cls.title is not None else 0
        flags |= 8 if cls.description is not None else 0
        flags |= 16 if cls.photo is not None else 0
        flags |= 32 if cls.embed_url is not None else 0
        flags |= 32 if cls.embed_type is not None else 0
        flags |= 64 if cls.embed_width is not None else 0
        flags |= 64 if cls.embed_height is not None else 0
        flags |= 128 if cls.duration is not None else 0
        flags |= 256 if cls.author is not None else 0
        flags |= 512 if cls.document is not None else 0
        flags |= 1024 if cls.cached_page is not None else 0
        flags |= 4096 if cls.attributes is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.id))
        data.write(String.getvalue(cls.url))
        data.write(String.getvalue(cls.display_url))
        data.write(Int.getvalue(cls.hash))
        
        if cls.type is not None:
            data.write(String.getvalue(cls.type))
        
        if cls.site_name is not None:
            data.write(String.getvalue(cls.site_name))
        
        if cls.title is not None:
            data.write(String.getvalue(cls.title))
        
        if cls.description is not None:
            data.write(String.getvalue(cls.description))
        
        if cls.photo is not None:
            data.write(cls.photo.getvalue())
        
        if cls.embed_url is not None:
            data.write(String.getvalue(cls.embed_url))
        
        if cls.embed_type is not None:
            data.write(String.getvalue(cls.embed_type))
        
        if cls.embed_width is not None:
            data.write(Int.getvalue(cls.embed_width))
        
        if cls.embed_height is not None:
            data.write(Int.getvalue(cls.embed_height))
        
        if cls.duration is not None:
            data.write(Int.getvalue(cls.duration))
        
        if cls.author is not None:
            data.write(String.getvalue(cls.author))
        
        if cls.document is not None:
            data.write(cls.document.getvalue())
        
        if cls.cached_page is not None:
            data.write(cls.cached_page.getvalue())
        
        if cls.attributes is not None:
            data.write(Vector().getvalue(cls.attributes))
        return data.getvalue()


class WebPageNotModified(TL):
    ID = 0x7311ca11

    def __init__(cls, cached_page_views: int = None):
        cls.cached_page_views = cached_page_views

    @staticmethod
    def read(data) -> "WebPageNotModified":
        flags = Int.read(data)
        cached_page_views = Int.read(data) if flags & 1 else None
        return WebPageNotModified(cached_page_views=cached_page_views)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.cached_page_views is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.cached_page_views is not None:
            data.write(Int.getvalue(cls.cached_page_views))
        return data.getvalue()


class Authorization(TL):
    ID = 0xad01d61d

    def __init__(cls, hash: int, device_model: str, platform: str, system_version: str, api_id: int, app_name: str, app_version: str, date_created: int, date_active: int, ip: str, country: str, region: str, current: bool = None, official_app: bool = None, password_pending: bool = None):
        cls.current = current
        cls.official_app = official_app
        cls.password_pending = password_pending
        cls.hash = hash
        cls.device_model = device_model
        cls.platform = platform
        cls.system_version = system_version
        cls.api_id = api_id
        cls.app_name = app_name
        cls.app_version = app_version
        cls.date_created = date_created
        cls.date_active = date_active
        cls.ip = ip
        cls.country = country
        cls.region = region

    @staticmethod
    def read(data) -> "Authorization":
        flags = Int.read(data)
        current = True if flags & 1 else False
        official_app = True if flags & 2 else False
        password_pending = True if flags & 4 else False
        hash = Long.read(data)
        device_model = String.read(data)
        platform = String.read(data)
        system_version = String.read(data)
        api_id = Int.read(data)
        app_name = String.read(data)
        app_version = String.read(data)
        date_created = Int.read(data)
        date_active = Int.read(data)
        ip = String.read(data)
        country = String.read(data)
        region = String.read(data)
        return Authorization(current=current, official_app=official_app, password_pending=password_pending, hash=hash, device_model=device_model, platform=platform, system_version=system_version, api_id=api_id, app_name=app_name, app_version=app_version, date_created=date_created, date_active=date_active, ip=ip, country=country, region=region)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.current is not None else 0
        flags |= 2 if cls.official_app is not None else 0
        flags |= 4 if cls.password_pending is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.hash))
        data.write(String.getvalue(cls.device_model))
        data.write(String.getvalue(cls.platform))
        data.write(String.getvalue(cls.system_version))
        data.write(Int.getvalue(cls.api_id))
        data.write(String.getvalue(cls.app_name))
        data.write(String.getvalue(cls.app_version))
        data.write(Int.getvalue(cls.date_created))
        data.write(Int.getvalue(cls.date_active))
        data.write(String.getvalue(cls.ip))
        data.write(String.getvalue(cls.country))
        data.write(String.getvalue(cls.region))
        return data.getvalue()


class ReceivedNotifyMessage(TL):
    ID = 0xa384b779

    def __init__(cls, id: int):
        cls.id = id

    @staticmethod
    def read(data) -> "ReceivedNotifyMessage":
        id = Int.read(data)
        flags = Int.read(data)
        return ReceivedNotifyMessage(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        return data.getvalue()


class ChatInviteExported(TL):
    ID = 0x6e24fc9d

    def __init__(cls, link: str, admin_id: int, date: int, revoked: bool = None, permanent: bool = None, start_date: int = None, expire_date: int = None, usage_limit: int = None, usage: int = None):
        cls.revoked = revoked
        cls.permanent = permanent
        cls.link = link
        cls.admin_id = admin_id
        cls.date = date
        cls.start_date = start_date
        cls.expire_date = expire_date
        cls.usage_limit = usage_limit
        cls.usage = usage

    @staticmethod
    def read(data) -> "ChatInviteExported":
        flags = Int.read(data)
        revoked = True if flags & 1 else False
        permanent = True if flags & 32 else False
        link = String.read(data)
        admin_id = Int.read(data)
        date = Int.read(data)
        start_date = Int.read(data) if flags & 16 else None
        expire_date = Int.read(data) if flags & 2 else None
        usage_limit = Int.read(data) if flags & 4 else None
        usage = Int.read(data) if flags & 8 else None
        return ChatInviteExported(revoked=revoked, permanent=permanent, link=link, admin_id=admin_id, date=date, start_date=start_date, expire_date=expire_date, usage_limit=usage_limit, usage=usage)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.revoked is not None else 0
        flags |= 32 if cls.permanent is not None else 0
        flags |= 16 if cls.start_date is not None else 0
        flags |= 2 if cls.expire_date is not None else 0
        flags |= 4 if cls.usage_limit is not None else 0
        flags |= 8 if cls.usage is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.link))
        data.write(Int.getvalue(cls.admin_id))
        data.write(Int.getvalue(cls.date))
        
        if cls.start_date is not None:
            data.write(Int.getvalue(cls.start_date))
        
        if cls.expire_date is not None:
            data.write(Int.getvalue(cls.expire_date))
        
        if cls.usage_limit is not None:
            data.write(Int.getvalue(cls.usage_limit))
        
        if cls.usage is not None:
            data.write(Int.getvalue(cls.usage))
        return data.getvalue()


class ChatInviteAlready(TL):
    ID = 0x5a686d7c

    def __init__(cls, chat: TL):
        cls.chat = chat

    @staticmethod
    def read(data) -> "ChatInviteAlready":
        chat = data.getobj()
        return ChatInviteAlready(chat=chat)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.chat.getvalue())
        return data.getvalue()


class ChatInvite(TL):
    ID = 0xdfc2f58e

    def __init__(cls, title: str, photo: TL, participants_count: int, channel: bool = None, broadcast: bool = None, public: bool = None, megagroup: bool = None, participants: List[TL] = None):
        cls.channel = channel
        cls.broadcast = broadcast
        cls.public = public
        cls.megagroup = megagroup
        cls.title = title
        cls.photo = photo
        cls.participants_count = participants_count
        cls.participants = participants

    @staticmethod
    def read(data) -> "ChatInvite":
        flags = Int.read(data)
        channel = True if flags & 1 else False
        broadcast = True if flags & 2 else False
        public = True if flags & 4 else False
        megagroup = True if flags & 8 else False
        title = String.read(data)
        photo = data.getobj()
        participants_count = Int.read(data)
        participants = data.getobj() if flags & 16 else []
        return ChatInvite(channel=channel, broadcast=broadcast, public=public, megagroup=megagroup, title=title, photo=photo, participants_count=participants_count, participants=participants)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.channel is not None else 0
        flags |= 2 if cls.broadcast is not None else 0
        flags |= 4 if cls.public is not None else 0
        flags |= 8 if cls.megagroup is not None else 0
        flags |= 16 if cls.participants is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.title))
        data.write(cls.photo.getvalue())
        data.write(Int.getvalue(cls.participants_count))
        
        if cls.participants is not None:
            data.write(Vector().getvalue(cls.participants))
        return data.getvalue()


class ChatInvitePeek(TL):
    ID = 0x61695cb0

    def __init__(cls, chat: TL, expires: int):
        cls.chat = chat
        cls.expires = expires

    @staticmethod
    def read(data) -> "ChatInvitePeek":
        chat = data.getobj()
        expires = Int.read(data)
        return ChatInvitePeek(chat=chat, expires=expires)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.chat.getvalue())
        data.write(Int.getvalue(cls.expires))
        return data.getvalue()


class InputStickerSetEmpty(TL):
    ID = 0xffb62b95

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputStickerSetEmpty":
        
        return InputStickerSetEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputStickerSetID(TL):
    ID = 0x9de7a269

    def __init__(cls, id: int, access_hash: int):
        cls.id = id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputStickerSetID":
        id = Long.read(data)
        access_hash = Long.read(data)
        return InputStickerSetID(id=id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class InputStickerSetShortName(TL):
    ID = 0x861cc8a0

    def __init__(cls, short_name: str):
        cls.short_name = short_name

    @staticmethod
    def read(data) -> "InputStickerSetShortName":
        short_name = String.read(data)
        return InputStickerSetShortName(short_name=short_name)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.short_name))
        return data.getvalue()


class InputStickerSetAnimatedEmoji(TL):
    ID = 0x28703c8

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputStickerSetAnimatedEmoji":
        
        return InputStickerSetAnimatedEmoji()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputStickerSetDice(TL):
    ID = 0xe67f520e

    def __init__(cls, emoticon: str):
        cls.emoticon = emoticon

    @staticmethod
    def read(data) -> "InputStickerSetDice":
        emoticon = String.read(data)
        return InputStickerSetDice(emoticon=emoticon)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.emoticon))
        return data.getvalue()


class StickerSet(TL):
    ID = 0x40e237a8

    def __init__(cls, id: int, access_hash: int, title: str, short_name: str, count: int, hash: int, archived: bool = None, official: bool = None, masks: bool = None, animated: bool = None, installed_date: int = None, thumbs: List[TL] = None, thumb_dc_id: int = None):
        cls.archived = archived
        cls.official = official
        cls.masks = masks
        cls.animated = animated
        cls.installed_date = installed_date
        cls.id = id
        cls.access_hash = access_hash
        cls.title = title
        cls.short_name = short_name
        cls.thumbs = thumbs
        cls.thumb_dc_id = thumb_dc_id
        cls.count = count
        cls.hash = hash

    @staticmethod
    def read(data) -> "StickerSet":
        flags = Int.read(data)
        archived = True if flags & 2 else False
        official = True if flags & 4 else False
        masks = True if flags & 8 else False
        animated = True if flags & 32 else False
        installed_date = Int.read(data) if flags & 1 else None
        id = Long.read(data)
        access_hash = Long.read(data)
        title = String.read(data)
        short_name = String.read(data)
        thumbs = data.getobj() if flags & 16 else []
        thumb_dc_id = Int.read(data) if flags & 16 else None
        count = Int.read(data)
        hash = Int.read(data)
        return StickerSet(archived=archived, official=official, masks=masks, animated=animated, installed_date=installed_date, id=id, access_hash=access_hash, title=title, short_name=short_name, thumbs=thumbs, thumb_dc_id=thumb_dc_id, count=count, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.archived is not None else 0
        flags |= 4 if cls.official is not None else 0
        flags |= 8 if cls.masks is not None else 0
        flags |= 32 if cls.animated is not None else 0
        flags |= 1 if cls.installed_date is not None else 0
        flags |= 16 if cls.thumbs is not None else 0
        flags |= 16 if cls.thumb_dc_id is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.installed_date is not None:
            data.write(Int.getvalue(cls.installed_date))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(String.getvalue(cls.title))
        data.write(String.getvalue(cls.short_name))
        
        if cls.thumbs is not None:
            data.write(Vector().getvalue(cls.thumbs))
        
        if cls.thumb_dc_id is not None:
            data.write(Int.getvalue(cls.thumb_dc_id))
        data.write(Int.getvalue(cls.count))
        data.write(Int.getvalue(cls.hash))
        return data.getvalue()


class BotCommand(TL):
    ID = 0xc27ac8c7

    def __init__(cls, command: str, description: str):
        cls.command = command
        cls.description = description

    @staticmethod
    def read(data) -> "BotCommand":
        command = String.read(data)
        description = String.read(data)
        return BotCommand(command=command, description=description)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.command))
        data.write(String.getvalue(cls.description))
        return data.getvalue()


class BotInfo(TL):
    ID = 0x98e81d3a

    def __init__(cls, user_id: int, description: str, commands: List[TL]):
        cls.user_id = user_id
        cls.description = description
        cls.commands = commands

    @staticmethod
    def read(data) -> "BotInfo":
        user_id = Int.read(data)
        description = String.read(data)
        commands = data.getobj()
        return BotInfo(user_id=user_id, description=description, commands=commands)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(String.getvalue(cls.description))
        data.write(Vector().getvalue(cls.commands))
        return data.getvalue()


class KeyboardButton(TL):
    ID = 0xa2fa4880

    def __init__(cls, text: str):
        cls.text = text

    @staticmethod
    def read(data) -> "KeyboardButton":
        text = String.read(data)
        return KeyboardButton(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class KeyboardButtonUrl(TL):
    ID = 0x258aff05

    def __init__(cls, text: str, url: str):
        cls.text = text
        cls.url = url

    @staticmethod
    def read(data) -> "KeyboardButtonUrl":
        text = String.read(data)
        url = String.read(data)
        return KeyboardButtonUrl(text=text, url=url)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.text))
        data.write(String.getvalue(cls.url))
        return data.getvalue()


class KeyboardButtonCallback(TL):
    ID = 0x35bbdb6b

    def __init__(cls, text: str, data: bytes, requires_password: bool = None):
        cls.requires_password = requires_password
        cls.text = text
        cls.data = data

    @staticmethod
    def read(data) -> "KeyboardButtonCallback":
        flags = Int.read(data)
        requires_password = True if flags & 1 else False
        text = String.read(data)
        data = Bytes.read(data)
        return KeyboardButtonCallback(requires_password=requires_password, text=text, data=data)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.requires_password is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.text))
        data.write(Bytes.getvalue(cls.data))
        return data.getvalue()


class KeyboardButtonRequestPhone(TL):
    ID = 0xb16a6c29

    def __init__(cls, text: str):
        cls.text = text

    @staticmethod
    def read(data) -> "KeyboardButtonRequestPhone":
        text = String.read(data)
        return KeyboardButtonRequestPhone(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class KeyboardButtonRequestGeoLocation(TL):
    ID = 0xfc796b3f

    def __init__(cls, text: str):
        cls.text = text

    @staticmethod
    def read(data) -> "KeyboardButtonRequestGeoLocation":
        text = String.read(data)
        return KeyboardButtonRequestGeoLocation(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class KeyboardButtonSwitchInline(TL):
    ID = 0x568a748

    def __init__(cls, text: str, query: str, same_peer: bool = None):
        cls.same_peer = same_peer
        cls.text = text
        cls.query = query

    @staticmethod
    def read(data) -> "KeyboardButtonSwitchInline":
        flags = Int.read(data)
        same_peer = True if flags & 1 else False
        text = String.read(data)
        query = String.read(data)
        return KeyboardButtonSwitchInline(same_peer=same_peer, text=text, query=query)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.same_peer is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.text))
        data.write(String.getvalue(cls.query))
        return data.getvalue()


class KeyboardButtonGame(TL):
    ID = 0x50f41ccf

    def __init__(cls, text: str):
        cls.text = text

    @staticmethod
    def read(data) -> "KeyboardButtonGame":
        text = String.read(data)
        return KeyboardButtonGame(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class KeyboardButtonBuy(TL):
    ID = 0xafd93fbb

    def __init__(cls, text: str):
        cls.text = text

    @staticmethod
    def read(data) -> "KeyboardButtonBuy":
        text = String.read(data)
        return KeyboardButtonBuy(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class KeyboardButtonUrlAuth(TL):
    ID = 0x10b78d29

    def __init__(cls, text: str, url: str, button_id: int, fwd_text: str = None):
        cls.text = text
        cls.fwd_text = fwd_text
        cls.url = url
        cls.button_id = button_id

    @staticmethod
    def read(data) -> "KeyboardButtonUrlAuth":
        flags = Int.read(data)
        text = String.read(data)
        fwd_text = String.read(data) if flags & 1 else None
        url = String.read(data)
        button_id = Int.read(data)
        return KeyboardButtonUrlAuth(text=text, fwd_text=fwd_text, url=url, button_id=button_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.fwd_text is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.text))
        
        if cls.fwd_text is not None:
            data.write(String.getvalue(cls.fwd_text))
        data.write(String.getvalue(cls.url))
        data.write(Int.getvalue(cls.button_id))
        return data.getvalue()


class InputKeyboardButtonUrlAuth(TL):
    ID = 0xd02e7fd4

    def __init__(cls, text: str, url: str, bot: TL, request_write_access: bool = None, fwd_text: str = None):
        cls.request_write_access = request_write_access
        cls.text = text
        cls.fwd_text = fwd_text
        cls.url = url
        cls.bot = bot

    @staticmethod
    def read(data) -> "InputKeyboardButtonUrlAuth":
        flags = Int.read(data)
        request_write_access = True if flags & 1 else False
        text = String.read(data)
        fwd_text = String.read(data) if flags & 2 else None
        url = String.read(data)
        bot = data.getobj()
        return InputKeyboardButtonUrlAuth(request_write_access=request_write_access, text=text, fwd_text=fwd_text, url=url, bot=bot)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.request_write_access is not None else 0
        flags |= 2 if cls.fwd_text is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.text))
        
        if cls.fwd_text is not None:
            data.write(String.getvalue(cls.fwd_text))
        data.write(String.getvalue(cls.url))
        data.write(cls.bot.getvalue())
        return data.getvalue()


class KeyboardButtonRequestPoll(TL):
    ID = 0xbbc7515d

    def __init__(cls, text: str, quiz: bool = None):
        cls.quiz = quiz
        cls.text = text

    @staticmethod
    def read(data) -> "KeyboardButtonRequestPoll":
        flags = Int.read(data)
        quiz = Bool.read(data) if flags & 1 else None
        text = String.read(data)
        return KeyboardButtonRequestPoll(quiz=quiz, text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.quiz is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class KeyboardButtonRow(TL):
    ID = 0x77608b83

    def __init__(cls, buttons: List[TL]):
        cls.buttons = buttons

    @staticmethod
    def read(data) -> "KeyboardButtonRow":
        buttons = data.getobj()
        return KeyboardButtonRow(buttons=buttons)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.buttons))
        return data.getvalue()


class ReplyKeyboardHide(TL):
    ID = 0xa03e5b85

    def __init__(cls, selective: bool = None):
        cls.selective = selective

    @staticmethod
    def read(data) -> "ReplyKeyboardHide":
        flags = Int.read(data)
        selective = True if flags & 4 else False
        return ReplyKeyboardHide(selective=selective)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 4 if cls.selective is not None else 0
        data.write(Int.getvalue(flags))
        return data.getvalue()


class ReplyKeyboardForceReply(TL):
    ID = 0xf4108aa0

    def __init__(cls, single_use: bool = None, selective: bool = None):
        cls.single_use = single_use
        cls.selective = selective

    @staticmethod
    def read(data) -> "ReplyKeyboardForceReply":
        flags = Int.read(data)
        single_use = True if flags & 2 else False
        selective = True if flags & 4 else False
        return ReplyKeyboardForceReply(single_use=single_use, selective=selective)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.single_use is not None else 0
        flags |= 4 if cls.selective is not None else 0
        data.write(Int.getvalue(flags))
        return data.getvalue()


class ReplyKeyboardMarkup(TL):
    ID = 0x3502758c

    def __init__(cls, rows: List[TL], resize: bool = None, single_use: bool = None, selective: bool = None):
        cls.resize = resize
        cls.single_use = single_use
        cls.selective = selective
        cls.rows = rows

    @staticmethod
    def read(data) -> "ReplyKeyboardMarkup":
        flags = Int.read(data)
        resize = True if flags & 1 else False
        single_use = True if flags & 2 else False
        selective = True if flags & 4 else False
        rows = data.getobj()
        return ReplyKeyboardMarkup(resize=resize, single_use=single_use, selective=selective, rows=rows)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.resize is not None else 0
        flags |= 2 if cls.single_use is not None else 0
        flags |= 4 if cls.selective is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Vector().getvalue(cls.rows))
        return data.getvalue()


class ReplyInlineMarkup(TL):
    ID = 0x48a30254

    def __init__(cls, rows: List[TL]):
        cls.rows = rows

    @staticmethod
    def read(data) -> "ReplyInlineMarkup":
        rows = data.getobj()
        return ReplyInlineMarkup(rows=rows)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.rows))
        return data.getvalue()


class MessageEntityUnknown(TL):
    ID = 0xbb92ba95

    def __init__(cls, offset: int, length: int):
        cls.offset = offset
        cls.length = length

    @staticmethod
    def read(data) -> "MessageEntityUnknown":
        offset = Int.read(data)
        length = Int.read(data)
        return MessageEntityUnknown(offset=offset, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class MessageEntityMention(TL):
    ID = 0xfa04579d

    def __init__(cls, offset: int, length: int):
        cls.offset = offset
        cls.length = length

    @staticmethod
    def read(data) -> "MessageEntityMention":
        offset = Int.read(data)
        length = Int.read(data)
        return MessageEntityMention(offset=offset, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class MessageEntityHashtag(TL):
    ID = 0x6f635b0d

    def __init__(cls, offset: int, length: int):
        cls.offset = offset
        cls.length = length

    @staticmethod
    def read(data) -> "MessageEntityHashtag":
        offset = Int.read(data)
        length = Int.read(data)
        return MessageEntityHashtag(offset=offset, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class MessageEntityBotCommand(TL):
    ID = 0x6cef8ac7

    def __init__(cls, offset: int, length: int):
        cls.offset = offset
        cls.length = length

    @staticmethod
    def read(data) -> "MessageEntityBotCommand":
        offset = Int.read(data)
        length = Int.read(data)
        return MessageEntityBotCommand(offset=offset, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class MessageEntityUrl(TL):
    ID = 0x6ed02538

    def __init__(cls, offset: int, length: int):
        cls.offset = offset
        cls.length = length

    @staticmethod
    def read(data) -> "MessageEntityUrl":
        offset = Int.read(data)
        length = Int.read(data)
        return MessageEntityUrl(offset=offset, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class MessageEntityEmail(TL):
    ID = 0x64e475c2

    def __init__(cls, offset: int, length: int):
        cls.offset = offset
        cls.length = length

    @staticmethod
    def read(data) -> "MessageEntityEmail":
        offset = Int.read(data)
        length = Int.read(data)
        return MessageEntityEmail(offset=offset, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class MessageEntityBold(TL):
    ID = 0xbd610bc9

    def __init__(cls, offset: int, length: int):
        cls.offset = offset
        cls.length = length

    @staticmethod
    def read(data) -> "MessageEntityBold":
        offset = Int.read(data)
        length = Int.read(data)
        return MessageEntityBold(offset=offset, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class MessageEntityItalic(TL):
    ID = 0x826f8b60

    def __init__(cls, offset: int, length: int):
        cls.offset = offset
        cls.length = length

    @staticmethod
    def read(data) -> "MessageEntityItalic":
        offset = Int.read(data)
        length = Int.read(data)
        return MessageEntityItalic(offset=offset, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class MessageEntityCode(TL):
    ID = 0x28a20571

    def __init__(cls, offset: int, length: int):
        cls.offset = offset
        cls.length = length

    @staticmethod
    def read(data) -> "MessageEntityCode":
        offset = Int.read(data)
        length = Int.read(data)
        return MessageEntityCode(offset=offset, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class MessageEntityPre(TL):
    ID = 0x73924be0

    def __init__(cls, offset: int, length: int, language: str):
        cls.offset = offset
        cls.length = length
        cls.language = language

    @staticmethod
    def read(data) -> "MessageEntityPre":
        offset = Int.read(data)
        length = Int.read(data)
        language = String.read(data)
        return MessageEntityPre(offset=offset, length=length, language=language)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        data.write(String.getvalue(cls.language))
        return data.getvalue()


class MessageEntityTextUrl(TL):
    ID = 0x76a6d327

    def __init__(cls, offset: int, length: int, url: str):
        cls.offset = offset
        cls.length = length
        cls.url = url

    @staticmethod
    def read(data) -> "MessageEntityTextUrl":
        offset = Int.read(data)
        length = Int.read(data)
        url = String.read(data)
        return MessageEntityTextUrl(offset=offset, length=length, url=url)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        data.write(String.getvalue(cls.url))
        return data.getvalue()


class MessageEntityMentionName(TL):
    ID = 0x352dca58

    def __init__(cls, offset: int, length: int, user_id: int):
        cls.offset = offset
        cls.length = length
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "MessageEntityMentionName":
        offset = Int.read(data)
        length = Int.read(data)
        user_id = Int.read(data)
        return MessageEntityMentionName(offset=offset, length=length, user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        data.write(Int.getvalue(cls.user_id))
        return data.getvalue()


class InputMessageEntityMentionName(TL):
    ID = 0x208e68c9

    def __init__(cls, offset: int, length: int, user_id: TL):
        cls.offset = offset
        cls.length = length
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "InputMessageEntityMentionName":
        offset = Int.read(data)
        length = Int.read(data)
        user_id = data.getobj()
        return InputMessageEntityMentionName(offset=offset, length=length, user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        data.write(cls.user_id.getvalue())
        return data.getvalue()


class MessageEntityPhone(TL):
    ID = 0x9b69e34b

    def __init__(cls, offset: int, length: int):
        cls.offset = offset
        cls.length = length

    @staticmethod
    def read(data) -> "MessageEntityPhone":
        offset = Int.read(data)
        length = Int.read(data)
        return MessageEntityPhone(offset=offset, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class MessageEntityCashtag(TL):
    ID = 0x4c4e743f

    def __init__(cls, offset: int, length: int):
        cls.offset = offset
        cls.length = length

    @staticmethod
    def read(data) -> "MessageEntityCashtag":
        offset = Int.read(data)
        length = Int.read(data)
        return MessageEntityCashtag(offset=offset, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class MessageEntityUnderline(TL):
    ID = 0x9c4e7e8b

    def __init__(cls, offset: int, length: int):
        cls.offset = offset
        cls.length = length

    @staticmethod
    def read(data) -> "MessageEntityUnderline":
        offset = Int.read(data)
        length = Int.read(data)
        return MessageEntityUnderline(offset=offset, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class MessageEntityStrike(TL):
    ID = 0xbf0693d4

    def __init__(cls, offset: int, length: int):
        cls.offset = offset
        cls.length = length

    @staticmethod
    def read(data) -> "MessageEntityStrike":
        offset = Int.read(data)
        length = Int.read(data)
        return MessageEntityStrike(offset=offset, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class MessageEntityBlockquote(TL):
    ID = 0x20df5d0

    def __init__(cls, offset: int, length: int):
        cls.offset = offset
        cls.length = length

    @staticmethod
    def read(data) -> "MessageEntityBlockquote":
        offset = Int.read(data)
        length = Int.read(data)
        return MessageEntityBlockquote(offset=offset, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class MessageEntityBankCard(TL):
    ID = 0x761e6af4

    def __init__(cls, offset: int, length: int):
        cls.offset = offset
        cls.length = length

    @staticmethod
    def read(data) -> "MessageEntityBankCard":
        offset = Int.read(data)
        length = Int.read(data)
        return MessageEntityBankCard(offset=offset, length=length)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.length))
        return data.getvalue()


class InputChannelEmpty(TL):
    ID = 0xee8c1e86

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputChannelEmpty":
        
        return InputChannelEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputChannel(TL):
    ID = 0xafeb712e

    def __init__(cls, channel_id: int, access_hash: int):
        cls.channel_id = channel_id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputChannel":
        channel_id = Int.read(data)
        access_hash = Long.read(data)
        return InputChannel(channel_id=channel_id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.channel_id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class InputChannelFromMessage(TL):
    ID = 0x2a286531

    def __init__(cls, peer: TL, msg_id: int, channel_id: int):
        cls.peer = peer
        cls.msg_id = msg_id
        cls.channel_id = channel_id

    @staticmethod
    def read(data) -> "InputChannelFromMessage":
        peer = data.getobj()
        msg_id = Int.read(data)
        channel_id = Int.read(data)
        return InputChannelFromMessage(peer=peer, msg_id=msg_id, channel_id=channel_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.msg_id))
        data.write(Int.getvalue(cls.channel_id))
        return data.getvalue()


class MessageRange(TL):
    ID = 0xae30253

    def __init__(cls, min_id: int, max_id: int):
        cls.min_id = min_id
        cls.max_id = max_id

    @staticmethod
    def read(data) -> "MessageRange":
        min_id = Int.read(data)
        max_id = Int.read(data)
        return MessageRange(min_id=min_id, max_id=max_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.min_id))
        data.write(Int.getvalue(cls.max_id))
        return data.getvalue()


class ChannelMessagesFilterEmpty(TL):
    ID = 0x94d42ee7

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ChannelMessagesFilterEmpty":
        
        return ChannelMessagesFilterEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ChannelMessagesFilter(TL):
    ID = 0xcd77d957

    def __init__(cls, ranges: List[TL], exclude_new_messages: bool = None):
        cls.exclude_new_messages = exclude_new_messages
        cls.ranges = ranges

    @staticmethod
    def read(data) -> "ChannelMessagesFilter":
        flags = Int.read(data)
        exclude_new_messages = True if flags & 2 else False
        ranges = data.getobj()
        return ChannelMessagesFilter(exclude_new_messages=exclude_new_messages, ranges=ranges)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.exclude_new_messages is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Vector().getvalue(cls.ranges))
        return data.getvalue()


class ChannelParticipant(TL):
    ID = 0x15ebac1d

    def __init__(cls, user_id: int, date: int):
        cls.user_id = user_id
        cls.date = date

    @staticmethod
    def read(data) -> "ChannelParticipant":
        user_id = Int.read(data)
        date = Int.read(data)
        return ChannelParticipant(user_id=user_id, date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class ChannelParticipantSelf(TL):
    ID = 0xa3289a6d

    def __init__(cls, user_id: int, inviter_id: int, date: int):
        cls.user_id = user_id
        cls.inviter_id = inviter_id
        cls.date = date

    @staticmethod
    def read(data) -> "ChannelParticipantSelf":
        user_id = Int.read(data)
        inviter_id = Int.read(data)
        date = Int.read(data)
        return ChannelParticipantSelf(user_id=user_id, inviter_id=inviter_id, date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Int.getvalue(cls.inviter_id))
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class ChannelParticipantCreator(TL):
    ID = 0x447dca4b

    def __init__(cls, user_id: int, admin_rights: TL, rank: str = None):
        cls.user_id = user_id
        cls.admin_rights = admin_rights
        cls.rank = rank

    @staticmethod
    def read(data) -> "ChannelParticipantCreator":
        flags = Int.read(data)
        user_id = Int.read(data)
        admin_rights = data.getobj()
        rank = String.read(data) if flags & 1 else None
        return ChannelParticipantCreator(user_id=user_id, admin_rights=admin_rights, rank=rank)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.rank is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.user_id))
        data.write(cls.admin_rights.getvalue())
        
        if cls.rank is not None:
            data.write(String.getvalue(cls.rank))
        return data.getvalue()


class ChannelParticipantAdmin(TL):
    ID = 0xccbebbaf

    def __init__(cls, user_id: int, promoted_by: int, date: int, admin_rights: TL, can_edit: bool = None, self: bool = None, inviter_id: int = None, rank: str = None):
        cls.can_edit = can_edit
        cls.self = self
        cls.user_id = user_id
        cls.inviter_id = inviter_id
        cls.promoted_by = promoted_by
        cls.date = date
        cls.admin_rights = admin_rights
        cls.rank = rank

    @staticmethod
    def read(data) -> "ChannelParticipantAdmin":
        flags = Int.read(data)
        can_edit = True if flags & 1 else False
        self = True if flags & 2 else False
        user_id = Int.read(data)
        inviter_id = Int.read(data) if flags & 2 else None
        promoted_by = Int.read(data)
        date = Int.read(data)
        admin_rights = data.getobj()
        rank = String.read(data) if flags & 4 else None
        return ChannelParticipantAdmin(can_edit=can_edit, self=self, user_id=user_id, inviter_id=inviter_id, promoted_by=promoted_by, date=date, admin_rights=admin_rights, rank=rank)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.can_edit is not None else 0
        flags |= 2 if cls.self is not None else 0
        flags |= 2 if cls.inviter_id is not None else 0
        flags |= 4 if cls.rank is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.user_id))
        
        if cls.inviter_id is not None:
            data.write(Int.getvalue(cls.inviter_id))
        data.write(Int.getvalue(cls.promoted_by))
        data.write(Int.getvalue(cls.date))
        data.write(cls.admin_rights.getvalue())
        
        if cls.rank is not None:
            data.write(String.getvalue(cls.rank))
        return data.getvalue()


class ChannelParticipantBanned(TL):
    ID = 0x1c0facaf

    def __init__(cls, user_id: int, kicked_by: int, date: int, banned_rights: TL, left: bool = None):
        cls.left = left
        cls.user_id = user_id
        cls.kicked_by = kicked_by
        cls.date = date
        cls.banned_rights = banned_rights

    @staticmethod
    def read(data) -> "ChannelParticipantBanned":
        flags = Int.read(data)
        left = True if flags & 1 else False
        user_id = Int.read(data)
        kicked_by = Int.read(data)
        date = Int.read(data)
        banned_rights = data.getobj()
        return ChannelParticipantBanned(left=left, user_id=user_id, kicked_by=kicked_by, date=date, banned_rights=banned_rights)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.left is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.user_id))
        data.write(Int.getvalue(cls.kicked_by))
        data.write(Int.getvalue(cls.date))
        data.write(cls.banned_rights.getvalue())
        return data.getvalue()


class ChannelParticipantLeft(TL):
    ID = 0xc3c6796b

    def __init__(cls, user_id: int):
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "ChannelParticipantLeft":
        user_id = Int.read(data)
        return ChannelParticipantLeft(user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        return data.getvalue()


class ChannelParticipantsRecent(TL):
    ID = 0xde3f3c79

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ChannelParticipantsRecent":
        
        return ChannelParticipantsRecent()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ChannelParticipantsAdmins(TL):
    ID = 0xb4608969

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ChannelParticipantsAdmins":
        
        return ChannelParticipantsAdmins()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ChannelParticipantsKicked(TL):
    ID = 0xa3b54985

    def __init__(cls, q: str):
        cls.q = q

    @staticmethod
    def read(data) -> "ChannelParticipantsKicked":
        q = String.read(data)
        return ChannelParticipantsKicked(q=q)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.q))
        return data.getvalue()


class ChannelParticipantsBots(TL):
    ID = 0xb0d1865b

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ChannelParticipantsBots":
        
        return ChannelParticipantsBots()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ChannelParticipantsBanned(TL):
    ID = 0x1427a5e1

    def __init__(cls, q: str):
        cls.q = q

    @staticmethod
    def read(data) -> "ChannelParticipantsBanned":
        q = String.read(data)
        return ChannelParticipantsBanned(q=q)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.q))
        return data.getvalue()


class ChannelParticipantsSearch(TL):
    ID = 0x656ac4b

    def __init__(cls, q: str):
        cls.q = q

    @staticmethod
    def read(data) -> "ChannelParticipantsSearch":
        q = String.read(data)
        return ChannelParticipantsSearch(q=q)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.q))
        return data.getvalue()


class ChannelParticipantsContacts(TL):
    ID = 0xbb6ae88d

    def __init__(cls, q: str):
        cls.q = q

    @staticmethod
    def read(data) -> "ChannelParticipantsContacts":
        q = String.read(data)
        return ChannelParticipantsContacts(q=q)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.q))
        return data.getvalue()


class ChannelParticipantsMentions(TL):
    ID = 0xe04b5ceb

    def __init__(cls, q: str = None, top_msg_id: int = None):
        cls.q = q
        cls.top_msg_id = top_msg_id

    @staticmethod
    def read(data) -> "ChannelParticipantsMentions":
        flags = Int.read(data)
        q = String.read(data) if flags & 1 else None
        top_msg_id = Int.read(data) if flags & 2 else None
        return ChannelParticipantsMentions(q=q, top_msg_id=top_msg_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.q is not None else 0
        flags |= 2 if cls.top_msg_id is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.q is not None:
            data.write(String.getvalue(cls.q))
        
        if cls.top_msg_id is not None:
            data.write(Int.getvalue(cls.top_msg_id))
        return data.getvalue()


class InputBotInlineMessageMediaAuto(TL):
    ID = 0x3380c786

    def __init__(cls, message: str, entities: List[TL] = None, reply_markup: TL = None):
        cls.message = message
        cls.entities = entities
        cls.reply_markup = reply_markup

    @staticmethod
    def read(data) -> "InputBotInlineMessageMediaAuto":
        flags = Int.read(data)
        message = String.read(data)
        entities = data.getobj() if flags & 2 else []
        reply_markup = data.getobj() if flags & 4 else None
        return InputBotInlineMessageMediaAuto(message=message, entities=entities, reply_markup=reply_markup)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.entities is not None else 0
        flags |= 4 if cls.reply_markup is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.message))
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        return data.getvalue()


class InputBotInlineMessageText(TL):
    ID = 0x3dcd7a87

    def __init__(cls, message: str, no_webpage: bool = None, entities: List[TL] = None, reply_markup: TL = None):
        cls.no_webpage = no_webpage
        cls.message = message
        cls.entities = entities
        cls.reply_markup = reply_markup

    @staticmethod
    def read(data) -> "InputBotInlineMessageText":
        flags = Int.read(data)
        no_webpage = True if flags & 1 else False
        message = String.read(data)
        entities = data.getobj() if flags & 2 else []
        reply_markup = data.getobj() if flags & 4 else None
        return InputBotInlineMessageText(no_webpage=no_webpage, message=message, entities=entities, reply_markup=reply_markup)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.no_webpage is not None else 0
        flags |= 2 if cls.entities is not None else 0
        flags |= 4 if cls.reply_markup is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.message))
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        return data.getvalue()


class InputBotInlineMessageMediaGeo(TL):
    ID = 0x96929a85

    def __init__(cls, geo_point: TL, heading: int = None, period: int = None, proximity_notification_radius: int = None, reply_markup: TL = None):
        cls.geo_point = geo_point
        cls.heading = heading
        cls.period = period
        cls.proximity_notification_radius = proximity_notification_radius
        cls.reply_markup = reply_markup

    @staticmethod
    def read(data) -> "InputBotInlineMessageMediaGeo":
        flags = Int.read(data)
        geo_point = data.getobj()
        heading = Int.read(data) if flags & 1 else None
        period = Int.read(data) if flags & 2 else None
        proximity_notification_radius = Int.read(data) if flags & 8 else None
        reply_markup = data.getobj() if flags & 4 else None
        return InputBotInlineMessageMediaGeo(geo_point=geo_point, heading=heading, period=period, proximity_notification_radius=proximity_notification_radius, reply_markup=reply_markup)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.heading is not None else 0
        flags |= 2 if cls.period is not None else 0
        flags |= 8 if cls.proximity_notification_radius is not None else 0
        flags |= 4 if cls.reply_markup is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.geo_point.getvalue())
        
        if cls.heading is not None:
            data.write(Int.getvalue(cls.heading))
        
        if cls.period is not None:
            data.write(Int.getvalue(cls.period))
        
        if cls.proximity_notification_radius is not None:
            data.write(Int.getvalue(cls.proximity_notification_radius))
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        return data.getvalue()


class InputBotInlineMessageMediaVenue(TL):
    ID = 0x417bbf11

    def __init__(cls, geo_point: TL, title: str, address: str, provider: str, venue_id: str, venue_type: str, reply_markup: TL = None):
        cls.geo_point = geo_point
        cls.title = title
        cls.address = address
        cls.provider = provider
        cls.venue_id = venue_id
        cls.venue_type = venue_type
        cls.reply_markup = reply_markup

    @staticmethod
    def read(data) -> "InputBotInlineMessageMediaVenue":
        flags = Int.read(data)
        geo_point = data.getobj()
        title = String.read(data)
        address = String.read(data)
        provider = String.read(data)
        venue_id = String.read(data)
        venue_type = String.read(data)
        reply_markup = data.getobj() if flags & 4 else None
        return InputBotInlineMessageMediaVenue(geo_point=geo_point, title=title, address=address, provider=provider, venue_id=venue_id, venue_type=venue_type, reply_markup=reply_markup)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 4 if cls.reply_markup is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.geo_point.getvalue())
        data.write(String.getvalue(cls.title))
        data.write(String.getvalue(cls.address))
        data.write(String.getvalue(cls.provider))
        data.write(String.getvalue(cls.venue_id))
        data.write(String.getvalue(cls.venue_type))
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        return data.getvalue()


class InputBotInlineMessageMediaContact(TL):
    ID = 0xa6edbffd

    def __init__(cls, phone_number: str, first_name: str, last_name: str, vcard: str, reply_markup: TL = None):
        cls.phone_number = phone_number
        cls.first_name = first_name
        cls.last_name = last_name
        cls.vcard = vcard
        cls.reply_markup = reply_markup

    @staticmethod
    def read(data) -> "InputBotInlineMessageMediaContact":
        flags = Int.read(data)
        phone_number = String.read(data)
        first_name = String.read(data)
        last_name = String.read(data)
        vcard = String.read(data)
        reply_markup = data.getobj() if flags & 4 else None
        return InputBotInlineMessageMediaContact(phone_number=phone_number, first_name=first_name, last_name=last_name, vcard=vcard, reply_markup=reply_markup)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 4 if cls.reply_markup is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.phone_number))
        data.write(String.getvalue(cls.first_name))
        data.write(String.getvalue(cls.last_name))
        data.write(String.getvalue(cls.vcard))
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        return data.getvalue()


class InputBotInlineMessageGame(TL):
    ID = 0x4b425864

    def __init__(cls, reply_markup: TL = None):
        cls.reply_markup = reply_markup

    @staticmethod
    def read(data) -> "InputBotInlineMessageGame":
        flags = Int.read(data)
        reply_markup = data.getobj() if flags & 4 else None
        return InputBotInlineMessageGame(reply_markup=reply_markup)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 4 if cls.reply_markup is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        return data.getvalue()


class InputBotInlineResult(TL):
    ID = 0x88bf9319

    def __init__(cls, id: str, type: str, send_message: TL, title: str = None, description: str = None, url: str = None, thumb: TL = None, content: TL = None):
        cls.id = id
        cls.type = type
        cls.title = title
        cls.description = description
        cls.url = url
        cls.thumb = thumb
        cls.content = content
        cls.send_message = send_message

    @staticmethod
    def read(data) -> "InputBotInlineResult":
        flags = Int.read(data)
        id = String.read(data)
        type = String.read(data)
        title = String.read(data) if flags & 2 else None
        description = String.read(data) if flags & 4 else None
        url = String.read(data) if flags & 8 else None
        thumb = data.getobj() if flags & 16 else None
        content = data.getobj() if flags & 32 else None
        send_message = data.getobj()
        return InputBotInlineResult(id=id, type=type, title=title, description=description, url=url, thumb=thumb, content=content, send_message=send_message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.title is not None else 0
        flags |= 4 if cls.description is not None else 0
        flags |= 8 if cls.url is not None else 0
        flags |= 16 if cls.thumb is not None else 0
        flags |= 32 if cls.content is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.id))
        data.write(String.getvalue(cls.type))
        
        if cls.title is not None:
            data.write(String.getvalue(cls.title))
        
        if cls.description is not None:
            data.write(String.getvalue(cls.description))
        
        if cls.url is not None:
            data.write(String.getvalue(cls.url))
        
        if cls.thumb is not None:
            data.write(cls.thumb.getvalue())
        
        if cls.content is not None:
            data.write(cls.content.getvalue())
        data.write(cls.send_message.getvalue())
        return data.getvalue()


class InputBotInlineResultPhoto(TL):
    ID = 0xa8d864a7

    def __init__(cls, id: str, type: str, photo: TL, send_message: TL):
        cls.id = id
        cls.type = type
        cls.photo = photo
        cls.send_message = send_message

    @staticmethod
    def read(data) -> "InputBotInlineResultPhoto":
        id = String.read(data)
        type = String.read(data)
        photo = data.getobj()
        send_message = data.getobj()
        return InputBotInlineResultPhoto(id=id, type=type, photo=photo, send_message=send_message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.id))
        data.write(String.getvalue(cls.type))
        data.write(cls.photo.getvalue())
        data.write(cls.send_message.getvalue())
        return data.getvalue()


class InputBotInlineResultDocument(TL):
    ID = 0xfff8fdc4

    def __init__(cls, id: str, type: str, document: TL, send_message: TL, title: str = None, description: str = None):
        cls.id = id
        cls.type = type
        cls.title = title
        cls.description = description
        cls.document = document
        cls.send_message = send_message

    @staticmethod
    def read(data) -> "InputBotInlineResultDocument":
        flags = Int.read(data)
        id = String.read(data)
        type = String.read(data)
        title = String.read(data) if flags & 2 else None
        description = String.read(data) if flags & 4 else None
        document = data.getobj()
        send_message = data.getobj()
        return InputBotInlineResultDocument(id=id, type=type, title=title, description=description, document=document, send_message=send_message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.title is not None else 0
        flags |= 4 if cls.description is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.id))
        data.write(String.getvalue(cls.type))
        
        if cls.title is not None:
            data.write(String.getvalue(cls.title))
        
        if cls.description is not None:
            data.write(String.getvalue(cls.description))
        data.write(cls.document.getvalue())
        data.write(cls.send_message.getvalue())
        return data.getvalue()


class InputBotInlineResultGame(TL):
    ID = 0x4fa417f2

    def __init__(cls, id: str, short_name: str, send_message: TL):
        cls.id = id
        cls.short_name = short_name
        cls.send_message = send_message

    @staticmethod
    def read(data) -> "InputBotInlineResultGame":
        id = String.read(data)
        short_name = String.read(data)
        send_message = data.getobj()
        return InputBotInlineResultGame(id=id, short_name=short_name, send_message=send_message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.id))
        data.write(String.getvalue(cls.short_name))
        data.write(cls.send_message.getvalue())
        return data.getvalue()


class BotInlineMessageMediaAuto(TL):
    ID = 0x764cf810

    def __init__(cls, message: str, entities: List[TL] = None, reply_markup: TL = None):
        cls.message = message
        cls.entities = entities
        cls.reply_markup = reply_markup

    @staticmethod
    def read(data) -> "BotInlineMessageMediaAuto":
        flags = Int.read(data)
        message = String.read(data)
        entities = data.getobj() if flags & 2 else []
        reply_markup = data.getobj() if flags & 4 else None
        return BotInlineMessageMediaAuto(message=message, entities=entities, reply_markup=reply_markup)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.entities is not None else 0
        flags |= 4 if cls.reply_markup is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.message))
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        return data.getvalue()


class BotInlineMessageText(TL):
    ID = 0x8c7f65e2

    def __init__(cls, message: str, no_webpage: bool = None, entities: List[TL] = None, reply_markup: TL = None):
        cls.no_webpage = no_webpage
        cls.message = message
        cls.entities = entities
        cls.reply_markup = reply_markup

    @staticmethod
    def read(data) -> "BotInlineMessageText":
        flags = Int.read(data)
        no_webpage = True if flags & 1 else False
        message = String.read(data)
        entities = data.getobj() if flags & 2 else []
        reply_markup = data.getobj() if flags & 4 else None
        return BotInlineMessageText(no_webpage=no_webpage, message=message, entities=entities, reply_markup=reply_markup)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.no_webpage is not None else 0
        flags |= 2 if cls.entities is not None else 0
        flags |= 4 if cls.reply_markup is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.message))
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        return data.getvalue()


class BotInlineMessageMediaGeo(TL):
    ID = 0x51846fd

    def __init__(cls, geo: TL, heading: int = None, period: int = None, proximity_notification_radius: int = None, reply_markup: TL = None):
        cls.geo = geo
        cls.heading = heading
        cls.period = period
        cls.proximity_notification_radius = proximity_notification_radius
        cls.reply_markup = reply_markup

    @staticmethod
    def read(data) -> "BotInlineMessageMediaGeo":
        flags = Int.read(data)
        geo = data.getobj()
        heading = Int.read(data) if flags & 1 else None
        period = Int.read(data) if flags & 2 else None
        proximity_notification_radius = Int.read(data) if flags & 8 else None
        reply_markup = data.getobj() if flags & 4 else None
        return BotInlineMessageMediaGeo(geo=geo, heading=heading, period=period, proximity_notification_radius=proximity_notification_radius, reply_markup=reply_markup)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.heading is not None else 0
        flags |= 2 if cls.period is not None else 0
        flags |= 8 if cls.proximity_notification_radius is not None else 0
        flags |= 4 if cls.reply_markup is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.geo.getvalue())
        
        if cls.heading is not None:
            data.write(Int.getvalue(cls.heading))
        
        if cls.period is not None:
            data.write(Int.getvalue(cls.period))
        
        if cls.proximity_notification_radius is not None:
            data.write(Int.getvalue(cls.proximity_notification_radius))
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        return data.getvalue()


class BotInlineMessageMediaVenue(TL):
    ID = 0x8a86659c

    def __init__(cls, geo: TL, title: str, address: str, provider: str, venue_id: str, venue_type: str, reply_markup: TL = None):
        cls.geo = geo
        cls.title = title
        cls.address = address
        cls.provider = provider
        cls.venue_id = venue_id
        cls.venue_type = venue_type
        cls.reply_markup = reply_markup

    @staticmethod
    def read(data) -> "BotInlineMessageMediaVenue":
        flags = Int.read(data)
        geo = data.getobj()
        title = String.read(data)
        address = String.read(data)
        provider = String.read(data)
        venue_id = String.read(data)
        venue_type = String.read(data)
        reply_markup = data.getobj() if flags & 4 else None
        return BotInlineMessageMediaVenue(geo=geo, title=title, address=address, provider=provider, venue_id=venue_id, venue_type=venue_type, reply_markup=reply_markup)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 4 if cls.reply_markup is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.geo.getvalue())
        data.write(String.getvalue(cls.title))
        data.write(String.getvalue(cls.address))
        data.write(String.getvalue(cls.provider))
        data.write(String.getvalue(cls.venue_id))
        data.write(String.getvalue(cls.venue_type))
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        return data.getvalue()


class BotInlineMessageMediaContact(TL):
    ID = 0x18d1cdc2

    def __init__(cls, phone_number: str, first_name: str, last_name: str, vcard: str, reply_markup: TL = None):
        cls.phone_number = phone_number
        cls.first_name = first_name
        cls.last_name = last_name
        cls.vcard = vcard
        cls.reply_markup = reply_markup

    @staticmethod
    def read(data) -> "BotInlineMessageMediaContact":
        flags = Int.read(data)
        phone_number = String.read(data)
        first_name = String.read(data)
        last_name = String.read(data)
        vcard = String.read(data)
        reply_markup = data.getobj() if flags & 4 else None
        return BotInlineMessageMediaContact(phone_number=phone_number, first_name=first_name, last_name=last_name, vcard=vcard, reply_markup=reply_markup)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 4 if cls.reply_markup is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.phone_number))
        data.write(String.getvalue(cls.first_name))
        data.write(String.getvalue(cls.last_name))
        data.write(String.getvalue(cls.vcard))
        
        if cls.reply_markup is not None:
            data.write(cls.reply_markup.getvalue())
        return data.getvalue()


class BotInlineResult(TL):
    ID = 0x11965f3a

    def __init__(cls, id: str, type: str, send_message: TL, title: str = None, description: str = None, url: str = None, thumb: TL = None, content: TL = None):
        cls.id = id
        cls.type = type
        cls.title = title
        cls.description = description
        cls.url = url
        cls.thumb = thumb
        cls.content = content
        cls.send_message = send_message

    @staticmethod
    def read(data) -> "BotInlineResult":
        flags = Int.read(data)
        id = String.read(data)
        type = String.read(data)
        title = String.read(data) if flags & 2 else None
        description = String.read(data) if flags & 4 else None
        url = String.read(data) if flags & 8 else None
        thumb = data.getobj() if flags & 16 else None
        content = data.getobj() if flags & 32 else None
        send_message = data.getobj()
        return BotInlineResult(id=id, type=type, title=title, description=description, url=url, thumb=thumb, content=content, send_message=send_message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.title is not None else 0
        flags |= 4 if cls.description is not None else 0
        flags |= 8 if cls.url is not None else 0
        flags |= 16 if cls.thumb is not None else 0
        flags |= 32 if cls.content is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.id))
        data.write(String.getvalue(cls.type))
        
        if cls.title is not None:
            data.write(String.getvalue(cls.title))
        
        if cls.description is not None:
            data.write(String.getvalue(cls.description))
        
        if cls.url is not None:
            data.write(String.getvalue(cls.url))
        
        if cls.thumb is not None:
            data.write(cls.thumb.getvalue())
        
        if cls.content is not None:
            data.write(cls.content.getvalue())
        data.write(cls.send_message.getvalue())
        return data.getvalue()


class BotInlineMediaResult(TL):
    ID = 0x17db940b

    def __init__(cls, id: str, type: str, send_message: TL, photo: TL = None, document: TL = None, title: str = None, description: str = None):
        cls.id = id
        cls.type = type
        cls.photo = photo
        cls.document = document
        cls.title = title
        cls.description = description
        cls.send_message = send_message

    @staticmethod
    def read(data) -> "BotInlineMediaResult":
        flags = Int.read(data)
        id = String.read(data)
        type = String.read(data)
        photo = data.getobj() if flags & 1 else None
        document = data.getobj() if flags & 2 else None
        title = String.read(data) if flags & 4 else None
        description = String.read(data) if flags & 8 else None
        send_message = data.getobj()
        return BotInlineMediaResult(id=id, type=type, photo=photo, document=document, title=title, description=description, send_message=send_message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.photo is not None else 0
        flags |= 2 if cls.document is not None else 0
        flags |= 4 if cls.title is not None else 0
        flags |= 8 if cls.description is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.id))
        data.write(String.getvalue(cls.type))
        
        if cls.photo is not None:
            data.write(cls.photo.getvalue())
        
        if cls.document is not None:
            data.write(cls.document.getvalue())
        
        if cls.title is not None:
            data.write(String.getvalue(cls.title))
        
        if cls.description is not None:
            data.write(String.getvalue(cls.description))
        data.write(cls.send_message.getvalue())
        return data.getvalue()


class ExportedMessageLink(TL):
    ID = 0x5dab1af4

    def __init__(cls, link: str, html: str):
        cls.link = link
        cls.html = html

    @staticmethod
    def read(data) -> "ExportedMessageLink":
        link = String.read(data)
        html = String.read(data)
        return ExportedMessageLink(link=link, html=html)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.link))
        data.write(String.getvalue(cls.html))
        return data.getvalue()


class MessageFwdHeader(TL):
    ID = 0x5f777dce

    def __init__(cls, date: int, imported: bool = None, from_id: TL = None, from_name: str = None, channel_post: int = None, post_author: str = None, saved_from_peer: TL = None, saved_from_msg_id: int = None, psa_type: str = None):
        cls.imported = imported
        cls.from_id = from_id
        cls.from_name = from_name
        cls.date = date
        cls.channel_post = channel_post
        cls.post_author = post_author
        cls.saved_from_peer = saved_from_peer
        cls.saved_from_msg_id = saved_from_msg_id
        cls.psa_type = psa_type

    @staticmethod
    def read(data) -> "MessageFwdHeader":
        flags = Int.read(data)
        imported = True if flags & 128 else False
        from_id = data.getobj() if flags & 1 else None
        from_name = String.read(data) if flags & 32 else None
        date = Int.read(data)
        channel_post = Int.read(data) if flags & 4 else None
        post_author = String.read(data) if flags & 8 else None
        saved_from_peer = data.getobj() if flags & 16 else None
        saved_from_msg_id = Int.read(data) if flags & 16 else None
        psa_type = String.read(data) if flags & 64 else None
        return MessageFwdHeader(imported=imported, from_id=from_id, from_name=from_name, date=date, channel_post=channel_post, post_author=post_author, saved_from_peer=saved_from_peer, saved_from_msg_id=saved_from_msg_id, psa_type=psa_type)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 128 if cls.imported is not None else 0
        flags |= 1 if cls.from_id is not None else 0
        flags |= 32 if cls.from_name is not None else 0
        flags |= 4 if cls.channel_post is not None else 0
        flags |= 8 if cls.post_author is not None else 0
        flags |= 16 if cls.saved_from_peer is not None else 0
        flags |= 16 if cls.saved_from_msg_id is not None else 0
        flags |= 64 if cls.psa_type is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.from_id is not None:
            data.write(cls.from_id.getvalue())
        
        if cls.from_name is not None:
            data.write(String.getvalue(cls.from_name))
        data.write(Int.getvalue(cls.date))
        
        if cls.channel_post is not None:
            data.write(Int.getvalue(cls.channel_post))
        
        if cls.post_author is not None:
            data.write(String.getvalue(cls.post_author))
        
        if cls.saved_from_peer is not None:
            data.write(cls.saved_from_peer.getvalue())
        
        if cls.saved_from_msg_id is not None:
            data.write(Int.getvalue(cls.saved_from_msg_id))
        
        if cls.psa_type is not None:
            data.write(String.getvalue(cls.psa_type))
        return data.getvalue()


class InputBotInlineMessageID(TL):
    ID = 0x890c3d89

    def __init__(cls, dc_id: int, id: int, access_hash: int):
        cls.dc_id = dc_id
        cls.id = id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputBotInlineMessageID":
        dc_id = Int.read(data)
        id = Long.read(data)
        access_hash = Long.read(data)
        return InputBotInlineMessageID(dc_id=dc_id, id=id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.dc_id))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class InlineBotSwitchPM(TL):
    ID = 0x3c20629f

    def __init__(cls, text: str, start_param: str):
        cls.text = text
        cls.start_param = start_param

    @staticmethod
    def read(data) -> "InlineBotSwitchPM":
        text = String.read(data)
        start_param = String.read(data)
        return InlineBotSwitchPM(text=text, start_param=start_param)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.text))
        data.write(String.getvalue(cls.start_param))
        return data.getvalue()


class TopPeer(TL):
    ID = 0xedcdc05b

    def __init__(cls, peer: TL, rating: float):
        cls.peer = peer
        cls.rating = rating

    @staticmethod
    def read(data) -> "TopPeer":
        peer = data.getobj()
        rating = Double.read(data)
        return TopPeer(peer=peer, rating=rating)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Double.getvalue(cls.rating))
        return data.getvalue()


class TopPeerCategoryBotsPM(TL):
    ID = 0xab661b5b

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "TopPeerCategoryBotsPM":
        
        return TopPeerCategoryBotsPM()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class TopPeerCategoryBotsInline(TL):
    ID = 0x148677e2

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "TopPeerCategoryBotsInline":
        
        return TopPeerCategoryBotsInline()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class TopPeerCategoryCorrespondents(TL):
    ID = 0x637b7ed

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "TopPeerCategoryCorrespondents":
        
        return TopPeerCategoryCorrespondents()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class TopPeerCategoryGroups(TL):
    ID = 0xbd17a14a

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "TopPeerCategoryGroups":
        
        return TopPeerCategoryGroups()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class TopPeerCategoryChannels(TL):
    ID = 0x161d9628

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "TopPeerCategoryChannels":
        
        return TopPeerCategoryChannels()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class TopPeerCategoryPhoneCalls(TL):
    ID = 0x1e76a78c

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "TopPeerCategoryPhoneCalls":
        
        return TopPeerCategoryPhoneCalls()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class TopPeerCategoryForwardUsers(TL):
    ID = 0xa8406ca9

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "TopPeerCategoryForwardUsers":
        
        return TopPeerCategoryForwardUsers()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class TopPeerCategoryForwardChats(TL):
    ID = 0xfbeec0f0

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "TopPeerCategoryForwardChats":
        
        return TopPeerCategoryForwardChats()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class TopPeerCategoryPeers(TL):
    ID = 0xfb834291

    def __init__(cls, category: TL, count: int, peers: List[TL]):
        cls.category = category
        cls.count = count
        cls.peers = peers

    @staticmethod
    def read(data) -> "TopPeerCategoryPeers":
        category = data.getobj()
        count = Int.read(data)
        peers = data.getobj()
        return TopPeerCategoryPeers(category=category, count=count, peers=peers)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.category.getvalue())
        data.write(Int.getvalue(cls.count))
        data.write(Vector().getvalue(cls.peers))
        return data.getvalue()


class DraftMessageEmpty(TL):
    ID = 0x1b0c841a

    def __init__(cls, date: int = None):
        cls.date = date

    @staticmethod
    def read(data) -> "DraftMessageEmpty":
        flags = Int.read(data)
        date = Int.read(data) if flags & 1 else None
        return DraftMessageEmpty(date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.date is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.date is not None:
            data.write(Int.getvalue(cls.date))
        return data.getvalue()


class DraftMessage(TL):
    ID = 0xfd8e711f

    def __init__(cls, message: str, date: int, no_webpage: bool = None, reply_to_msg_id: int = None, entities: List[TL] = None):
        cls.no_webpage = no_webpage
        cls.reply_to_msg_id = reply_to_msg_id
        cls.message = message
        cls.entities = entities
        cls.date = date

    @staticmethod
    def read(data) -> "DraftMessage":
        flags = Int.read(data)
        no_webpage = True if flags & 2 else False
        reply_to_msg_id = Int.read(data) if flags & 1 else None
        message = String.read(data)
        entities = data.getobj() if flags & 8 else []
        date = Int.read(data)
        return DraftMessage(no_webpage=no_webpage, reply_to_msg_id=reply_to_msg_id, message=message, entities=entities, date=date)

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
        data.write(String.getvalue(cls.message))
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class StickerSetCovered(TL):
    ID = 0x6410a5d2

    def __init__(cls, set: TL, cover: TL):
        cls.set = set
        cls.cover = cover

    @staticmethod
    def read(data) -> "StickerSetCovered":
        set = data.getobj()
        cover = data.getobj()
        return StickerSetCovered(set=set, cover=cover)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.set.getvalue())
        data.write(cls.cover.getvalue())
        return data.getvalue()


class StickerSetMultiCovered(TL):
    ID = 0x3407e51b

    def __init__(cls, set: TL, covers: List[TL]):
        cls.set = set
        cls.covers = covers

    @staticmethod
    def read(data) -> "StickerSetMultiCovered":
        set = data.getobj()
        covers = data.getobj()
        return StickerSetMultiCovered(set=set, covers=covers)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.set.getvalue())
        data.write(Vector().getvalue(cls.covers))
        return data.getvalue()


class MaskCoords(TL):
    ID = 0xaed6dbb2

    def __init__(cls, n: int, x: float, y: float, zoom: float):
        cls.n = n
        cls.x = x
        cls.y = y
        cls.zoom = zoom

    @staticmethod
    def read(data) -> "MaskCoords":
        n = Int.read(data)
        x = Double.read(data)
        y = Double.read(data)
        zoom = Double.read(data)
        return MaskCoords(n=n, x=x, y=y, zoom=zoom)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.n))
        data.write(Double.getvalue(cls.x))
        data.write(Double.getvalue(cls.y))
        data.write(Double.getvalue(cls.zoom))
        return data.getvalue()


class InputStickeredMediaPhoto(TL):
    ID = 0x4a992157

    def __init__(cls, id: TL):
        cls.id = id

    @staticmethod
    def read(data) -> "InputStickeredMediaPhoto":
        id = data.getobj()
        return InputStickeredMediaPhoto(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.id.getvalue())
        return data.getvalue()


class InputStickeredMediaDocument(TL):
    ID = 0x438865b

    def __init__(cls, id: TL):
        cls.id = id

    @staticmethod
    def read(data) -> "InputStickeredMediaDocument":
        id = data.getobj()
        return InputStickeredMediaDocument(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.id.getvalue())
        return data.getvalue()


class Game(TL):
    ID = 0xbdf9653b

    def __init__(cls, id: int, access_hash: int, short_name: str, title: str, description: str, photo: TL, document: TL = None):
        cls.id = id
        cls.access_hash = access_hash
        cls.short_name = short_name
        cls.title = title
        cls.description = description
        cls.photo = photo
        cls.document = document

    @staticmethod
    def read(data) -> "Game":
        flags = Int.read(data)
        id = Long.read(data)
        access_hash = Long.read(data)
        short_name = String.read(data)
        title = String.read(data)
        description = String.read(data)
        photo = data.getobj()
        document = data.getobj() if flags & 1 else None
        return Game(id=id, access_hash=access_hash, short_name=short_name, title=title, description=description, photo=photo, document=document)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.document is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(String.getvalue(cls.short_name))
        data.write(String.getvalue(cls.title))
        data.write(String.getvalue(cls.description))
        data.write(cls.photo.getvalue())
        
        if cls.document is not None:
            data.write(cls.document.getvalue())
        return data.getvalue()


class InputGameID(TL):
    ID = 0x32c3e77

    def __init__(cls, id: int, access_hash: int):
        cls.id = id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputGameID":
        id = Long.read(data)
        access_hash = Long.read(data)
        return InputGameID(id=id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class InputGameShortName(TL):
    ID = 0xc331e80a

    def __init__(cls, bot_id: TL, short_name: str):
        cls.bot_id = bot_id
        cls.short_name = short_name

    @staticmethod
    def read(data) -> "InputGameShortName":
        bot_id = data.getobj()
        short_name = String.read(data)
        return InputGameShortName(bot_id=bot_id, short_name=short_name)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.bot_id.getvalue())
        data.write(String.getvalue(cls.short_name))
        return data.getvalue()


class HighScore(TL):
    ID = 0x58fffcd0

    def __init__(cls, pos: int, user_id: int, score: int):
        cls.pos = pos
        cls.user_id = user_id
        cls.score = score

    @staticmethod
    def read(data) -> "HighScore":
        pos = Int.read(data)
        user_id = Int.read(data)
        score = Int.read(data)
        return HighScore(pos=pos, user_id=user_id, score=score)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.pos))
        data.write(Int.getvalue(cls.user_id))
        data.write(Int.getvalue(cls.score))
        return data.getvalue()


class TextEmpty(TL):
    ID = 0xdc3d824f

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "TextEmpty":
        
        return TextEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class TextPlain(TL):
    ID = 0x744694e0

    def __init__(cls, text: str):
        cls.text = text

    @staticmethod
    def read(data) -> "TextPlain":
        text = String.read(data)
        return TextPlain(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class TextBold(TL):
    ID = 0x6724abc4

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "TextBold":
        text = data.getobj()
        return TextBold(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class TextItalic(TL):
    ID = 0xd912a59c

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "TextItalic":
        text = data.getobj()
        return TextItalic(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class TextUnderline(TL):
    ID = 0xc12622c4

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "TextUnderline":
        text = data.getobj()
        return TextUnderline(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class TextStrike(TL):
    ID = 0x9bf8bb95

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "TextStrike":
        text = data.getobj()
        return TextStrike(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class TextFixed(TL):
    ID = 0x6c3f19b9

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "TextFixed":
        text = data.getobj()
        return TextFixed(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class TextUrl(TL):
    ID = 0x3c2884c1

    def __init__(cls, text: TL, url: str, webpage_id: int):
        cls.text = text
        cls.url = url
        cls.webpage_id = webpage_id

    @staticmethod
    def read(data) -> "TextUrl":
        text = data.getobj()
        url = String.read(data)
        webpage_id = Long.read(data)
        return TextUrl(text=text, url=url, webpage_id=webpage_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        data.write(String.getvalue(cls.url))
        data.write(Long.getvalue(cls.webpage_id))
        return data.getvalue()


class TextEmail(TL):
    ID = 0xde5a0dd6

    def __init__(cls, text: TL, email: str):
        cls.text = text
        cls.email = email

    @staticmethod
    def read(data) -> "TextEmail":
        text = data.getobj()
        email = String.read(data)
        return TextEmail(text=text, email=email)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        data.write(String.getvalue(cls.email))
        return data.getvalue()


class TextConcat(TL):
    ID = 0x7e6260d7

    def __init__(cls, texts: List[TL]):
        cls.texts = texts

    @staticmethod
    def read(data) -> "TextConcat":
        texts = data.getobj()
        return TextConcat(texts=texts)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.texts))
        return data.getvalue()


class TextSubscript(TL):
    ID = 0xed6a8504

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "TextSubscript":
        text = data.getobj()
        return TextSubscript(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class TextSuperscript(TL):
    ID = 0xc7fb5e01

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "TextSuperscript":
        text = data.getobj()
        return TextSuperscript(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class TextMarked(TL):
    ID = 0x34b8621

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "TextMarked":
        text = data.getobj()
        return TextMarked(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class TextPhone(TL):
    ID = 0x1ccb966a

    def __init__(cls, text: TL, phone: str):
        cls.text = text
        cls.phone = phone

    @staticmethod
    def read(data) -> "TextPhone":
        text = data.getobj()
        phone = String.read(data)
        return TextPhone(text=text, phone=phone)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        data.write(String.getvalue(cls.phone))
        return data.getvalue()


class TextImage(TL):
    ID = 0x81ccf4f

    def __init__(cls, document_id: int, w: int, h: int):
        cls.document_id = document_id
        cls.w = w
        cls.h = h

    @staticmethod
    def read(data) -> "TextImage":
        document_id = Long.read(data)
        w = Int.read(data)
        h = Int.read(data)
        return TextImage(document_id=document_id, w=w, h=h)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.document_id))
        data.write(Int.getvalue(cls.w))
        data.write(Int.getvalue(cls.h))
        return data.getvalue()


class TextAnchor(TL):
    ID = 0x35553762

    def __init__(cls, text: TL, name: str):
        cls.text = text
        cls.name = name

    @staticmethod
    def read(data) -> "TextAnchor":
        text = data.getobj()
        name = String.read(data)
        return TextAnchor(text=text, name=name)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        data.write(String.getvalue(cls.name))
        return data.getvalue()


class PageBlockUnsupported(TL):
    ID = 0x13567e8a

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PageBlockUnsupported":
        
        return PageBlockUnsupported()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PageBlockTitle(TL):
    ID = 0x70abc3fd

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "PageBlockTitle":
        text = data.getobj()
        return PageBlockTitle(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class PageBlockSubtitle(TL):
    ID = 0x8ffa9a1f

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "PageBlockSubtitle":
        text = data.getobj()
        return PageBlockSubtitle(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class PageBlockAuthorDate(TL):
    ID = 0xbaafe5e0

    def __init__(cls, author: TL, published_date: int):
        cls.author = author
        cls.published_date = published_date

    @staticmethod
    def read(data) -> "PageBlockAuthorDate":
        author = data.getobj()
        published_date = Int.read(data)
        return PageBlockAuthorDate(author=author, published_date=published_date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.author.getvalue())
        data.write(Int.getvalue(cls.published_date))
        return data.getvalue()


class PageBlockHeader(TL):
    ID = 0xbfd064ec

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "PageBlockHeader":
        text = data.getobj()
        return PageBlockHeader(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class PageBlockSubheader(TL):
    ID = 0xf12bb6e1

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "PageBlockSubheader":
        text = data.getobj()
        return PageBlockSubheader(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class PageBlockParagraph(TL):
    ID = 0x467a0766

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "PageBlockParagraph":
        text = data.getobj()
        return PageBlockParagraph(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class PageBlockPreformatted(TL):
    ID = 0xc070d93e

    def __init__(cls, text: TL, language: str):
        cls.text = text
        cls.language = language

    @staticmethod
    def read(data) -> "PageBlockPreformatted":
        text = data.getobj()
        language = String.read(data)
        return PageBlockPreformatted(text=text, language=language)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        data.write(String.getvalue(cls.language))
        return data.getvalue()


class PageBlockFooter(TL):
    ID = 0x48870999

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "PageBlockFooter":
        text = data.getobj()
        return PageBlockFooter(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class PageBlockDivider(TL):
    ID = 0xdb20b188

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PageBlockDivider":
        
        return PageBlockDivider()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PageBlockAnchor(TL):
    ID = 0xce0d37b0

    def __init__(cls, name: str):
        cls.name = name

    @staticmethod
    def read(data) -> "PageBlockAnchor":
        name = String.read(data)
        return PageBlockAnchor(name=name)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.name))
        return data.getvalue()


class PageBlockList(TL):
    ID = 0xe4e88011

    def __init__(cls, items: List[TL]):
        cls.items = items

    @staticmethod
    def read(data) -> "PageBlockList":
        items = data.getobj()
        return PageBlockList(items=items)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.items))
        return data.getvalue()


class PageBlockBlockquote(TL):
    ID = 0x263d7c26

    def __init__(cls, text: TL, caption: TL):
        cls.text = text
        cls.caption = caption

    @staticmethod
    def read(data) -> "PageBlockBlockquote":
        text = data.getobj()
        caption = data.getobj()
        return PageBlockBlockquote(text=text, caption=caption)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        data.write(cls.caption.getvalue())
        return data.getvalue()


class PageBlockPullquote(TL):
    ID = 0x4f4456d3

    def __init__(cls, text: TL, caption: TL):
        cls.text = text
        cls.caption = caption

    @staticmethod
    def read(data) -> "PageBlockPullquote":
        text = data.getobj()
        caption = data.getobj()
        return PageBlockPullquote(text=text, caption=caption)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        data.write(cls.caption.getvalue())
        return data.getvalue()


class PageBlockPhoto(TL):
    ID = 0x1759c560

    def __init__(cls, photo_id: int, caption: TL, url: str = None, webpage_id: int = None):
        cls.photo_id = photo_id
        cls.caption = caption
        cls.url = url
        cls.webpage_id = webpage_id

    @staticmethod
    def read(data) -> "PageBlockPhoto":
        flags = Int.read(data)
        photo_id = Long.read(data)
        caption = data.getobj()
        url = String.read(data) if flags & 1 else None
        webpage_id = Long.read(data) if flags & 1 else None
        return PageBlockPhoto(photo_id=photo_id, caption=caption, url=url, webpage_id=webpage_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.url is not None else 0
        flags |= 1 if cls.webpage_id is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.photo_id))
        data.write(cls.caption.getvalue())
        
        if cls.url is not None:
            data.write(String.getvalue(cls.url))
        
        if cls.webpage_id is not None:
            data.write(Long.getvalue(cls.webpage_id))
        return data.getvalue()


class PageBlockVideo(TL):
    ID = 0x7c8fe7b6

    def __init__(cls, video_id: int, caption: TL, autoplay: bool = None, loop: bool = None):
        cls.autoplay = autoplay
        cls.loop = loop
        cls.video_id = video_id
        cls.caption = caption

    @staticmethod
    def read(data) -> "PageBlockVideo":
        flags = Int.read(data)
        autoplay = True if flags & 1 else False
        loop = True if flags & 2 else False
        video_id = Long.read(data)
        caption = data.getobj()
        return PageBlockVideo(autoplay=autoplay, loop=loop, video_id=video_id, caption=caption)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.autoplay is not None else 0
        flags |= 2 if cls.loop is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.video_id))
        data.write(cls.caption.getvalue())
        return data.getvalue()


class PageBlockCover(TL):
    ID = 0x39f23300

    def __init__(cls, cover: TL):
        cls.cover = cover

    @staticmethod
    def read(data) -> "PageBlockCover":
        cover = data.getobj()
        return PageBlockCover(cover=cover)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.cover.getvalue())
        return data.getvalue()


class PageBlockEmbed(TL):
    ID = 0xa8718dc5

    def __init__(cls, caption: TL, full_width: bool = None, allow_scrolling: bool = None, url: str = None, html: str = None, poster_photo_id: int = None, w: int = None, h: int = None):
        cls.full_width = full_width
        cls.allow_scrolling = allow_scrolling
        cls.url = url
        cls.html = html
        cls.poster_photo_id = poster_photo_id
        cls.w = w
        cls.h = h
        cls.caption = caption

    @staticmethod
    def read(data) -> "PageBlockEmbed":
        flags = Int.read(data)
        full_width = True if flags & 1 else False
        allow_scrolling = True if flags & 8 else False
        url = String.read(data) if flags & 2 else None
        html = String.read(data) if flags & 4 else None
        poster_photo_id = Long.read(data) if flags & 16 else None
        w = Int.read(data) if flags & 32 else None
        h = Int.read(data) if flags & 32 else None
        caption = data.getobj()
        return PageBlockEmbed(full_width=full_width, allow_scrolling=allow_scrolling, url=url, html=html, poster_photo_id=poster_photo_id, w=w, h=h, caption=caption)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.full_width is not None else 0
        flags |= 8 if cls.allow_scrolling is not None else 0
        flags |= 2 if cls.url is not None else 0
        flags |= 4 if cls.html is not None else 0
        flags |= 16 if cls.poster_photo_id is not None else 0
        flags |= 32 if cls.w is not None else 0
        flags |= 32 if cls.h is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.url is not None:
            data.write(String.getvalue(cls.url))
        
        if cls.html is not None:
            data.write(String.getvalue(cls.html))
        
        if cls.poster_photo_id is not None:
            data.write(Long.getvalue(cls.poster_photo_id))
        
        if cls.w is not None:
            data.write(Int.getvalue(cls.w))
        
        if cls.h is not None:
            data.write(Int.getvalue(cls.h))
        data.write(cls.caption.getvalue())
        return data.getvalue()


class PageBlockEmbedPost(TL):
    ID = 0xf259a80b

    def __init__(cls, url: str, webpage_id: int, author_photo_id: int, author: str, date: int, blocks: List[TL], caption: TL):
        cls.url = url
        cls.webpage_id = webpage_id
        cls.author_photo_id = author_photo_id
        cls.author = author
        cls.date = date
        cls.blocks = blocks
        cls.caption = caption

    @staticmethod
    def read(data) -> "PageBlockEmbedPost":
        url = String.read(data)
        webpage_id = Long.read(data)
        author_photo_id = Long.read(data)
        author = String.read(data)
        date = Int.read(data)
        blocks = data.getobj()
        caption = data.getobj()
        return PageBlockEmbedPost(url=url, webpage_id=webpage_id, author_photo_id=author_photo_id, author=author, date=date, blocks=blocks, caption=caption)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        data.write(Long.getvalue(cls.webpage_id))
        data.write(Long.getvalue(cls.author_photo_id))
        data.write(String.getvalue(cls.author))
        data.write(Int.getvalue(cls.date))
        data.write(Vector().getvalue(cls.blocks))
        data.write(cls.caption.getvalue())
        return data.getvalue()


class PageBlockCollage(TL):
    ID = 0x65a0fa4d

    def __init__(cls, items: List[TL], caption: TL):
        cls.items = items
        cls.caption = caption

    @staticmethod
    def read(data) -> "PageBlockCollage":
        items = data.getobj()
        caption = data.getobj()
        return PageBlockCollage(items=items, caption=caption)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.items))
        data.write(cls.caption.getvalue())
        return data.getvalue()


class PageBlockSlideshow(TL):
    ID = 0x31f9590

    def __init__(cls, items: List[TL], caption: TL):
        cls.items = items
        cls.caption = caption

    @staticmethod
    def read(data) -> "PageBlockSlideshow":
        items = data.getobj()
        caption = data.getobj()
        return PageBlockSlideshow(items=items, caption=caption)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.items))
        data.write(cls.caption.getvalue())
        return data.getvalue()


class PageBlockChannel(TL):
    ID = 0xef1751b5

    def __init__(cls, channel: TL):
        cls.channel = channel

    @staticmethod
    def read(data) -> "PageBlockChannel":
        channel = data.getobj()
        return PageBlockChannel(channel=channel)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.channel.getvalue())
        return data.getvalue()


class PageBlockAudio(TL):
    ID = 0x804361ea

    def __init__(cls, audio_id: int, caption: TL):
        cls.audio_id = audio_id
        cls.caption = caption

    @staticmethod
    def read(data) -> "PageBlockAudio":
        audio_id = Long.read(data)
        caption = data.getobj()
        return PageBlockAudio(audio_id=audio_id, caption=caption)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.audio_id))
        data.write(cls.caption.getvalue())
        return data.getvalue()


class PageBlockKicker(TL):
    ID = 0x1e148390

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "PageBlockKicker":
        text = data.getobj()
        return PageBlockKicker(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class PageBlockTable(TL):
    ID = 0xbf4dea82

    def __init__(cls, title: TL, rows: List[TL], bordered: bool = None, striped: bool = None):
        cls.bordered = bordered
        cls.striped = striped
        cls.title = title
        cls.rows = rows

    @staticmethod
    def read(data) -> "PageBlockTable":
        flags = Int.read(data)
        bordered = True if flags & 1 else False
        striped = True if flags & 2 else False
        title = data.getobj()
        rows = data.getobj()
        return PageBlockTable(bordered=bordered, striped=striped, title=title, rows=rows)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.bordered is not None else 0
        flags |= 2 if cls.striped is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.title.getvalue())
        data.write(Vector().getvalue(cls.rows))
        return data.getvalue()


class PageBlockOrderedList(TL):
    ID = 0x9a8ae1e1

    def __init__(cls, items: List[TL]):
        cls.items = items

    @staticmethod
    def read(data) -> "PageBlockOrderedList":
        items = data.getobj()
        return PageBlockOrderedList(items=items)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.items))
        return data.getvalue()


class PageBlockDetails(TL):
    ID = 0x76768bed

    def __init__(cls, blocks: List[TL], title: TL, open: bool = None):
        cls.open = open
        cls.blocks = blocks
        cls.title = title

    @staticmethod
    def read(data) -> "PageBlockDetails":
        flags = Int.read(data)
        open = True if flags & 1 else False
        blocks = data.getobj()
        title = data.getobj()
        return PageBlockDetails(open=open, blocks=blocks, title=title)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.open is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Vector().getvalue(cls.blocks))
        data.write(cls.title.getvalue())
        return data.getvalue()


class PageBlockRelatedArticles(TL):
    ID = 0x16115a96

    def __init__(cls, title: TL, articles: List[TL]):
        cls.title = title
        cls.articles = articles

    @staticmethod
    def read(data) -> "PageBlockRelatedArticles":
        title = data.getobj()
        articles = data.getobj()
        return PageBlockRelatedArticles(title=title, articles=articles)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.title.getvalue())
        data.write(Vector().getvalue(cls.articles))
        return data.getvalue()


class PageBlockMap(TL):
    ID = 0xa44f3ef6

    def __init__(cls, geo: TL, zoom: int, w: int, h: int, caption: TL):
        cls.geo = geo
        cls.zoom = zoom
        cls.w = w
        cls.h = h
        cls.caption = caption

    @staticmethod
    def read(data) -> "PageBlockMap":
        geo = data.getobj()
        zoom = Int.read(data)
        w = Int.read(data)
        h = Int.read(data)
        caption = data.getobj()
        return PageBlockMap(geo=geo, zoom=zoom, w=w, h=h, caption=caption)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.geo.getvalue())
        data.write(Int.getvalue(cls.zoom))
        data.write(Int.getvalue(cls.w))
        data.write(Int.getvalue(cls.h))
        data.write(cls.caption.getvalue())
        return data.getvalue()


class PhoneCallDiscardReasonMissed(TL):
    ID = 0x85e42301

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PhoneCallDiscardReasonMissed":
        
        return PhoneCallDiscardReasonMissed()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PhoneCallDiscardReasonDisconnect(TL):
    ID = 0xe095c1a0

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PhoneCallDiscardReasonDisconnect":
        
        return PhoneCallDiscardReasonDisconnect()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PhoneCallDiscardReasonHangup(TL):
    ID = 0x57adc690

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PhoneCallDiscardReasonHangup":
        
        return PhoneCallDiscardReasonHangup()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PhoneCallDiscardReasonBusy(TL):
    ID = 0xfaf7e8c9

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PhoneCallDiscardReasonBusy":
        
        return PhoneCallDiscardReasonBusy()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class DataJSON(TL):
    ID = 0x7d748d04

    def __init__(cls, data: str):
        cls.data = data

    @staticmethod
    def read(data) -> "DataJSON":
        data = String.read(data)
        return DataJSON(data=data)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.data))
        return data.getvalue()


class LabeledPrice(TL):
    ID = 0xcb296bf8

    def __init__(cls, label: str, amount: int):
        cls.label = label
        cls.amount = amount

    @staticmethod
    def read(data) -> "LabeledPrice":
        label = String.read(data)
        amount = Long.read(data)
        return LabeledPrice(label=label, amount=amount)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.label))
        data.write(Long.getvalue(cls.amount))
        return data.getvalue()


class Invoice(TL):
    ID = 0xc30aa358

    def __init__(cls, currency: str, prices: List[TL], test: bool = None, name_requested: bool = None, phone_requested: bool = None, email_requested: bool = None, shipping_address_requested: bool = None, flexible: bool = None, phone_to_provider: bool = None, email_to_provider: bool = None):
        cls.test = test
        cls.name_requested = name_requested
        cls.phone_requested = phone_requested
        cls.email_requested = email_requested
        cls.shipping_address_requested = shipping_address_requested
        cls.flexible = flexible
        cls.phone_to_provider = phone_to_provider
        cls.email_to_provider = email_to_provider
        cls.currency = currency
        cls.prices = prices

    @staticmethod
    def read(data) -> "Invoice":
        flags = Int.read(data)
        test = True if flags & 1 else False
        name_requested = True if flags & 2 else False
        phone_requested = True if flags & 4 else False
        email_requested = True if flags & 8 else False
        shipping_address_requested = True if flags & 16 else False
        flexible = True if flags & 32 else False
        phone_to_provider = True if flags & 64 else False
        email_to_provider = True if flags & 128 else False
        currency = String.read(data)
        prices = data.getobj()
        return Invoice(test=test, name_requested=name_requested, phone_requested=phone_requested, email_requested=email_requested, shipping_address_requested=shipping_address_requested, flexible=flexible, phone_to_provider=phone_to_provider, email_to_provider=email_to_provider, currency=currency, prices=prices)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.test is not None else 0
        flags |= 2 if cls.name_requested is not None else 0
        flags |= 4 if cls.phone_requested is not None else 0
        flags |= 8 if cls.email_requested is not None else 0
        flags |= 16 if cls.shipping_address_requested is not None else 0
        flags |= 32 if cls.flexible is not None else 0
        flags |= 64 if cls.phone_to_provider is not None else 0
        flags |= 128 if cls.email_to_provider is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.currency))
        data.write(Vector().getvalue(cls.prices))
        return data.getvalue()


class PaymentCharge(TL):
    ID = 0xea02c27e

    def __init__(cls, id: str, provider_charge_id: str):
        cls.id = id
        cls.provider_charge_id = provider_charge_id

    @staticmethod
    def read(data) -> "PaymentCharge":
        id = String.read(data)
        provider_charge_id = String.read(data)
        return PaymentCharge(id=id, provider_charge_id=provider_charge_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.id))
        data.write(String.getvalue(cls.provider_charge_id))
        return data.getvalue()


class PostAddress(TL):
    ID = 0x1e8caaeb

    def __init__(cls, street_line1: str, street_line2: str, city: str, state: str, country_iso2: str, post_code: str):
        cls.street_line1 = street_line1
        cls.street_line2 = street_line2
        cls.city = city
        cls.state = state
        cls.country_iso2 = country_iso2
        cls.post_code = post_code

    @staticmethod
    def read(data) -> "PostAddress":
        street_line1 = String.read(data)
        street_line2 = String.read(data)
        city = String.read(data)
        state = String.read(data)
        country_iso2 = String.read(data)
        post_code = String.read(data)
        return PostAddress(street_line1=street_line1, street_line2=street_line2, city=city, state=state, country_iso2=country_iso2, post_code=post_code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.street_line1))
        data.write(String.getvalue(cls.street_line2))
        data.write(String.getvalue(cls.city))
        data.write(String.getvalue(cls.state))
        data.write(String.getvalue(cls.country_iso2))
        data.write(String.getvalue(cls.post_code))
        return data.getvalue()


class PaymentRequestedInfo(TL):
    ID = 0x909c3f94

    def __init__(cls, name: str = None, phone: str = None, email: str = None, shipping_address: TL = None):
        cls.name = name
        cls.phone = phone
        cls.email = email
        cls.shipping_address = shipping_address

    @staticmethod
    def read(data) -> "PaymentRequestedInfo":
        flags = Int.read(data)
        name = String.read(data) if flags & 1 else None
        phone = String.read(data) if flags & 2 else None
        email = String.read(data) if flags & 4 else None
        shipping_address = data.getobj() if flags & 8 else None
        return PaymentRequestedInfo(name=name, phone=phone, email=email, shipping_address=shipping_address)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.name is not None else 0
        flags |= 2 if cls.phone is not None else 0
        flags |= 4 if cls.email is not None else 0
        flags |= 8 if cls.shipping_address is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.name is not None:
            data.write(String.getvalue(cls.name))
        
        if cls.phone is not None:
            data.write(String.getvalue(cls.phone))
        
        if cls.email is not None:
            data.write(String.getvalue(cls.email))
        
        if cls.shipping_address is not None:
            data.write(cls.shipping_address.getvalue())
        return data.getvalue()


class PaymentSavedCredentialsCard(TL):
    ID = 0xcdc27a1f

    def __init__(cls, id: str, title: str):
        cls.id = id
        cls.title = title

    @staticmethod
    def read(data) -> "PaymentSavedCredentialsCard":
        id = String.read(data)
        title = String.read(data)
        return PaymentSavedCredentialsCard(id=id, title=title)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.id))
        data.write(String.getvalue(cls.title))
        return data.getvalue()


class WebDocument(TL):
    ID = 0x1c570ed1

    def __init__(cls, url: str, access_hash: int, size: int, mime_type: str, attributes: List[TL]):
        cls.url = url
        cls.access_hash = access_hash
        cls.size = size
        cls.mime_type = mime_type
        cls.attributes = attributes

    @staticmethod
    def read(data) -> "WebDocument":
        url = String.read(data)
        access_hash = Long.read(data)
        size = Int.read(data)
        mime_type = String.read(data)
        attributes = data.getobj()
        return WebDocument(url=url, access_hash=access_hash, size=size, mime_type=mime_type, attributes=attributes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Int.getvalue(cls.size))
        data.write(String.getvalue(cls.mime_type))
        data.write(Vector().getvalue(cls.attributes))
        return data.getvalue()


class WebDocumentNoProxy(TL):
    ID = 0xf9c8bcc6

    def __init__(cls, url: str, size: int, mime_type: str, attributes: List[TL]):
        cls.url = url
        cls.size = size
        cls.mime_type = mime_type
        cls.attributes = attributes

    @staticmethod
    def read(data) -> "WebDocumentNoProxy":
        url = String.read(data)
        size = Int.read(data)
        mime_type = String.read(data)
        attributes = data.getobj()
        return WebDocumentNoProxy(url=url, size=size, mime_type=mime_type, attributes=attributes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        data.write(Int.getvalue(cls.size))
        data.write(String.getvalue(cls.mime_type))
        data.write(Vector().getvalue(cls.attributes))
        return data.getvalue()


class InputWebDocument(TL):
    ID = 0x9bed434d

    def __init__(cls, url: str, size: int, mime_type: str, attributes: List[TL]):
        cls.url = url
        cls.size = size
        cls.mime_type = mime_type
        cls.attributes = attributes

    @staticmethod
    def read(data) -> "InputWebDocument":
        url = String.read(data)
        size = Int.read(data)
        mime_type = String.read(data)
        attributes = data.getobj()
        return InputWebDocument(url=url, size=size, mime_type=mime_type, attributes=attributes)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        data.write(Int.getvalue(cls.size))
        data.write(String.getvalue(cls.mime_type))
        data.write(Vector().getvalue(cls.attributes))
        return data.getvalue()


class InputWebFileLocation(TL):
    ID = 0xc239d686

    def __init__(cls, url: str, access_hash: int):
        cls.url = url
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputWebFileLocation":
        url = String.read(data)
        access_hash = Long.read(data)
        return InputWebFileLocation(url=url, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class InputWebFileGeoPointLocation(TL):
    ID = 0x9f2221c9

    def __init__(cls, geo_point: TL, access_hash: int, w: int, h: int, zoom: int, scale: int):
        cls.geo_point = geo_point
        cls.access_hash = access_hash
        cls.w = w
        cls.h = h
        cls.zoom = zoom
        cls.scale = scale

    @staticmethod
    def read(data) -> "InputWebFileGeoPointLocation":
        geo_point = data.getobj()
        access_hash = Long.read(data)
        w = Int.read(data)
        h = Int.read(data)
        zoom = Int.read(data)
        scale = Int.read(data)
        return InputWebFileGeoPointLocation(geo_point=geo_point, access_hash=access_hash, w=w, h=h, zoom=zoom, scale=scale)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.geo_point.getvalue())
        data.write(Long.getvalue(cls.access_hash))
        data.write(Int.getvalue(cls.w))
        data.write(Int.getvalue(cls.h))
        data.write(Int.getvalue(cls.zoom))
        data.write(Int.getvalue(cls.scale))
        return data.getvalue()


class InputPaymentCredentialsSaved(TL):
    ID = 0xc10eb2cf

    def __init__(cls, id: str, tmp_password: bytes):
        cls.id = id
        cls.tmp_password = tmp_password

    @staticmethod
    def read(data) -> "InputPaymentCredentialsSaved":
        id = String.read(data)
        tmp_password = Bytes.read(data)
        return InputPaymentCredentialsSaved(id=id, tmp_password=tmp_password)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.id))
        data.write(Bytes.getvalue(cls.tmp_password))
        return data.getvalue()


class InputPaymentCredentials(TL):
    ID = 0x3417d728

    def __init__(cls, data: TL, save: bool = None):
        cls.save = save
        cls.data = data

    @staticmethod
    def read(data) -> "InputPaymentCredentials":
        flags = Int.read(data)
        save = True if flags & 1 else False
        data = data.getobj()
        return InputPaymentCredentials(save=save, data=data)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.save is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.data.getvalue())
        return data.getvalue()


class InputPaymentCredentialsApplePay(TL):
    ID = 0xaa1c39f

    def __init__(cls, payment_data: TL):
        cls.payment_data = payment_data

    @staticmethod
    def read(data) -> "InputPaymentCredentialsApplePay":
        payment_data = data.getobj()
        return InputPaymentCredentialsApplePay(payment_data=payment_data)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.payment_data.getvalue())
        return data.getvalue()


class InputPaymentCredentialsGooglePay(TL):
    ID = 0x8ac32801

    def __init__(cls, payment_token: TL):
        cls.payment_token = payment_token

    @staticmethod
    def read(data) -> "InputPaymentCredentialsGooglePay":
        payment_token = data.getobj()
        return InputPaymentCredentialsGooglePay(payment_token=payment_token)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.payment_token.getvalue())
        return data.getvalue()


class ShippingOption(TL):
    ID = 0xb6213cdf

    def __init__(cls, id: str, title: str, prices: List[TL]):
        cls.id = id
        cls.title = title
        cls.prices = prices

    @staticmethod
    def read(data) -> "ShippingOption":
        id = String.read(data)
        title = String.read(data)
        prices = data.getobj()
        return ShippingOption(id=id, title=title, prices=prices)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.id))
        data.write(String.getvalue(cls.title))
        data.write(Vector().getvalue(cls.prices))
        return data.getvalue()


class InputStickerSetItem(TL):
    ID = 0xffa0a496

    def __init__(cls, document: TL, emoji: str, mask_coords: TL = None):
        cls.document = document
        cls.emoji = emoji
        cls.mask_coords = mask_coords

    @staticmethod
    def read(data) -> "InputStickerSetItem":
        flags = Int.read(data)
        document = data.getobj()
        emoji = String.read(data)
        mask_coords = data.getobj() if flags & 1 else None
        return InputStickerSetItem(document=document, emoji=emoji, mask_coords=mask_coords)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.mask_coords is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.document.getvalue())
        data.write(String.getvalue(cls.emoji))
        
        if cls.mask_coords is not None:
            data.write(cls.mask_coords.getvalue())
        return data.getvalue()


class InputPhoneCall(TL):
    ID = 0x1e36fded

    def __init__(cls, id: int, access_hash: int):
        cls.id = id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputPhoneCall":
        id = Long.read(data)
        access_hash = Long.read(data)
        return InputPhoneCall(id=id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class PhoneCallEmpty(TL):
    ID = 0x5366c915

    def __init__(cls, id: int):
        cls.id = id

    @staticmethod
    def read(data) -> "PhoneCallEmpty":
        id = Long.read(data)
        return PhoneCallEmpty(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        return data.getvalue()


class PhoneCallWaiting(TL):
    ID = 0x1b8f4ad1

    def __init__(cls, id: int, access_hash: int, date: int, admin_id: int, participant_id: int, protocol: TL, video: bool = None, receive_date: int = None):
        cls.video = video
        cls.id = id
        cls.access_hash = access_hash
        cls.date = date
        cls.admin_id = admin_id
        cls.participant_id = participant_id
        cls.protocol = protocol
        cls.receive_date = receive_date

    @staticmethod
    def read(data) -> "PhoneCallWaiting":
        flags = Int.read(data)
        video = True if flags & 64 else False
        id = Long.read(data)
        access_hash = Long.read(data)
        date = Int.read(data)
        admin_id = Int.read(data)
        participant_id = Int.read(data)
        protocol = data.getobj()
        receive_date = Int.read(data) if flags & 1 else None
        return PhoneCallWaiting(video=video, id=id, access_hash=access_hash, date=date, admin_id=admin_id, participant_id=participant_id, protocol=protocol, receive_date=receive_date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 64 if cls.video is not None else 0
        flags |= 1 if cls.receive_date is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.admin_id))
        data.write(Int.getvalue(cls.participant_id))
        data.write(cls.protocol.getvalue())
        
        if cls.receive_date is not None:
            data.write(Int.getvalue(cls.receive_date))
        return data.getvalue()


class PhoneCallRequested(TL):
    ID = 0x87eabb53

    def __init__(cls, id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_a_hash: bytes, protocol: TL, video: bool = None):
        cls.video = video
        cls.id = id
        cls.access_hash = access_hash
        cls.date = date
        cls.admin_id = admin_id
        cls.participant_id = participant_id
        cls.g_a_hash = g_a_hash
        cls.protocol = protocol

    @staticmethod
    def read(data) -> "PhoneCallRequested":
        flags = Int.read(data)
        video = True if flags & 64 else False
        id = Long.read(data)
        access_hash = Long.read(data)
        date = Int.read(data)
        admin_id = Int.read(data)
        participant_id = Int.read(data)
        g_a_hash = Bytes.read(data)
        protocol = data.getobj()
        return PhoneCallRequested(video=video, id=id, access_hash=access_hash, date=date, admin_id=admin_id, participant_id=participant_id, g_a_hash=g_a_hash, protocol=protocol)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 64 if cls.video is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.admin_id))
        data.write(Int.getvalue(cls.participant_id))
        data.write(Bytes.getvalue(cls.g_a_hash))
        data.write(cls.protocol.getvalue())
        return data.getvalue()


class PhoneCallAccepted(TL):
    ID = 0x997c454a

    def __init__(cls, id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_b: bytes, protocol: TL, video: bool = None):
        cls.video = video
        cls.id = id
        cls.access_hash = access_hash
        cls.date = date
        cls.admin_id = admin_id
        cls.participant_id = participant_id
        cls.g_b = g_b
        cls.protocol = protocol

    @staticmethod
    def read(data) -> "PhoneCallAccepted":
        flags = Int.read(data)
        video = True if flags & 64 else False
        id = Long.read(data)
        access_hash = Long.read(data)
        date = Int.read(data)
        admin_id = Int.read(data)
        participant_id = Int.read(data)
        g_b = Bytes.read(data)
        protocol = data.getobj()
        return PhoneCallAccepted(video=video, id=id, access_hash=access_hash, date=date, admin_id=admin_id, participant_id=participant_id, g_b=g_b, protocol=protocol)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 64 if cls.video is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.admin_id))
        data.write(Int.getvalue(cls.participant_id))
        data.write(Bytes.getvalue(cls.g_b))
        data.write(cls.protocol.getvalue())
        return data.getvalue()


class PhoneCall(TL):
    ID = 0x8742ae7f

    def __init__(cls, id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_a_or_b: bytes, key_fingerprint: int, protocol: TL, connections: List[TL], start_date: int, p2p_allowed: bool = None, video: bool = None):
        cls.p2p_allowed = p2p_allowed
        cls.video = video
        cls.id = id
        cls.access_hash = access_hash
        cls.date = date
        cls.admin_id = admin_id
        cls.participant_id = participant_id
        cls.g_a_or_b = g_a_or_b
        cls.key_fingerprint = key_fingerprint
        cls.protocol = protocol
        cls.connections = connections
        cls.start_date = start_date

    @staticmethod
    def read(data) -> "PhoneCall":
        flags = Int.read(data)
        p2p_allowed = True if flags & 32 else False
        video = True if flags & 64 else False
        id = Long.read(data)
        access_hash = Long.read(data)
        date = Int.read(data)
        admin_id = Int.read(data)
        participant_id = Int.read(data)
        g_a_or_b = Bytes.read(data)
        key_fingerprint = Long.read(data)
        protocol = data.getobj()
        connections = data.getobj()
        start_date = Int.read(data)
        return PhoneCall(p2p_allowed=p2p_allowed, video=video, id=id, access_hash=access_hash, date=date, admin_id=admin_id, participant_id=participant_id, g_a_or_b=g_a_or_b, key_fingerprint=key_fingerprint, protocol=protocol, connections=connections, start_date=start_date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 32 if cls.p2p_allowed is not None else 0
        flags |= 64 if cls.video is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.admin_id))
        data.write(Int.getvalue(cls.participant_id))
        data.write(Bytes.getvalue(cls.g_a_or_b))
        data.write(Long.getvalue(cls.key_fingerprint))
        data.write(cls.protocol.getvalue())
        data.write(Vector().getvalue(cls.connections))
        data.write(Int.getvalue(cls.start_date))
        return data.getvalue()


class PhoneCallDiscarded(TL):
    ID = 0x50ca4de1

    def __init__(cls, id: int, need_rating: bool = None, need_debug: bool = None, video: bool = None, reason: TL = None, duration: int = None):
        cls.need_rating = need_rating
        cls.need_debug = need_debug
        cls.video = video
        cls.id = id
        cls.reason = reason
        cls.duration = duration

    @staticmethod
    def read(data) -> "PhoneCallDiscarded":
        flags = Int.read(data)
        need_rating = True if flags & 4 else False
        need_debug = True if flags & 8 else False
        video = True if flags & 64 else False
        id = Long.read(data)
        reason = data.getobj() if flags & 1 else None
        duration = Int.read(data) if flags & 2 else None
        return PhoneCallDiscarded(need_rating=need_rating, need_debug=need_debug, video=video, id=id, reason=reason, duration=duration)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 4 if cls.need_rating is not None else 0
        flags |= 8 if cls.need_debug is not None else 0
        flags |= 64 if cls.video is not None else 0
        flags |= 1 if cls.reason is not None else 0
        flags |= 2 if cls.duration is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.id))
        
        if cls.reason is not None:
            data.write(cls.reason.getvalue())
        
        if cls.duration is not None:
            data.write(Int.getvalue(cls.duration))
        return data.getvalue()


class PhoneConnection(TL):
    ID = 0x9d4c17c0

    def __init__(cls, id: int, ip: str, ipv6: str, port: int, peer_tag: bytes):
        cls.id = id
        cls.ip = ip
        cls.ipv6 = ipv6
        cls.port = port
        cls.peer_tag = peer_tag

    @staticmethod
    def read(data) -> "PhoneConnection":
        id = Long.read(data)
        ip = String.read(data)
        ipv6 = String.read(data)
        port = Int.read(data)
        peer_tag = Bytes.read(data)
        return PhoneConnection(id=id, ip=ip, ipv6=ipv6, port=port, peer_tag=peer_tag)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(String.getvalue(cls.ip))
        data.write(String.getvalue(cls.ipv6))
        data.write(Int.getvalue(cls.port))
        data.write(Bytes.getvalue(cls.peer_tag))
        return data.getvalue()


class PhoneConnectionWebrtc(TL):
    ID = 0x635fe375

    def __init__(cls, id: int, ip: str, ipv6: str, port: int, username: str, password: str, turn: bool = None, stun: bool = None):
        cls.turn = turn
        cls.stun = stun
        cls.id = id
        cls.ip = ip
        cls.ipv6 = ipv6
        cls.port = port
        cls.username = username
        cls.password = password

    @staticmethod
    def read(data) -> "PhoneConnectionWebrtc":
        flags = Int.read(data)
        turn = True if flags & 1 else False
        stun = True if flags & 2 else False
        id = Long.read(data)
        ip = String.read(data)
        ipv6 = String.read(data)
        port = Int.read(data)
        username = String.read(data)
        password = String.read(data)
        return PhoneConnectionWebrtc(turn=turn, stun=stun, id=id, ip=ip, ipv6=ipv6, port=port, username=username, password=password)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.turn is not None else 0
        flags |= 2 if cls.stun is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.id))
        data.write(String.getvalue(cls.ip))
        data.write(String.getvalue(cls.ipv6))
        data.write(Int.getvalue(cls.port))
        data.write(String.getvalue(cls.username))
        data.write(String.getvalue(cls.password))
        return data.getvalue()


class PhoneCallProtocol(TL):
    ID = 0xfc878fc8

    def __init__(cls, min_layer: int, max_layer: int, library_versions: List[str], udp_p2p: bool = None, udp_reflector: bool = None):
        cls.udp_p2p = udp_p2p
        cls.udp_reflector = udp_reflector
        cls.min_layer = min_layer
        cls.max_layer = max_layer
        cls.library_versions = library_versions

    @staticmethod
    def read(data) -> "PhoneCallProtocol":
        flags = Int.read(data)
        udp_p2p = True if flags & 1 else False
        udp_reflector = True if flags & 2 else False
        min_layer = Int.read(data)
        max_layer = Int.read(data)
        library_versions = data.getobj(String)
        return PhoneCallProtocol(udp_p2p=udp_p2p, udp_reflector=udp_reflector, min_layer=min_layer, max_layer=max_layer, library_versions=library_versions)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.udp_p2p is not None else 0
        flags |= 2 if cls.udp_reflector is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.min_layer))
        data.write(Int.getvalue(cls.max_layer))
        data.write(Vector().getvalue(cls.library_versions, String))
        return data.getvalue()


class CdnPublicKey(TL):
    ID = 0xc982eaba

    def __init__(cls, dc_id: int, public_key: str):
        cls.dc_id = dc_id
        cls.public_key = public_key

    @staticmethod
    def read(data) -> "CdnPublicKey":
        dc_id = Int.read(data)
        public_key = String.read(data)
        return CdnPublicKey(dc_id=dc_id, public_key=public_key)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.dc_id))
        data.write(String.getvalue(cls.public_key))
        return data.getvalue()


class CdnConfig(TL):
    ID = 0x5725e40a

    def __init__(cls, public_keys: List[TL]):
        cls.public_keys = public_keys

    @staticmethod
    def read(data) -> "CdnConfig":
        public_keys = data.getobj()
        return CdnConfig(public_keys=public_keys)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.public_keys))
        return data.getvalue()


class LangPackString(TL):
    ID = 0xcad181f6

    def __init__(cls, key: str, value: str):
        cls.key = key
        cls.value = value

    @staticmethod
    def read(data) -> "LangPackString":
        key = String.read(data)
        value = String.read(data)
        return LangPackString(key=key, value=value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.key))
        data.write(String.getvalue(cls.value))
        return data.getvalue()


class LangPackStringPluralized(TL):
    ID = 0x6c47ac9f

    def __init__(cls, key: str, other_value: str, zero_value: str = None, one_value: str = None, two_value: str = None, few_value: str = None, many_value: str = None):
        cls.key = key
        cls.zero_value = zero_value
        cls.one_value = one_value
        cls.two_value = two_value
        cls.few_value = few_value
        cls.many_value = many_value
        cls.other_value = other_value

    @staticmethod
    def read(data) -> "LangPackStringPluralized":
        flags = Int.read(data)
        key = String.read(data)
        zero_value = String.read(data) if flags & 1 else None
        one_value = String.read(data) if flags & 2 else None
        two_value = String.read(data) if flags & 4 else None
        few_value = String.read(data) if flags & 8 else None
        many_value = String.read(data) if flags & 16 else None
        other_value = String.read(data)
        return LangPackStringPluralized(key=key, zero_value=zero_value, one_value=one_value, two_value=two_value, few_value=few_value, many_value=many_value, other_value=other_value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.zero_value is not None else 0
        flags |= 2 if cls.one_value is not None else 0
        flags |= 4 if cls.two_value is not None else 0
        flags |= 8 if cls.few_value is not None else 0
        flags |= 16 if cls.many_value is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.key))
        
        if cls.zero_value is not None:
            data.write(String.getvalue(cls.zero_value))
        
        if cls.one_value is not None:
            data.write(String.getvalue(cls.one_value))
        
        if cls.two_value is not None:
            data.write(String.getvalue(cls.two_value))
        
        if cls.few_value is not None:
            data.write(String.getvalue(cls.few_value))
        
        if cls.many_value is not None:
            data.write(String.getvalue(cls.many_value))
        data.write(String.getvalue(cls.other_value))
        return data.getvalue()


class LangPackStringDeleted(TL):
    ID = 0x2979eeb2

    def __init__(cls, key: str):
        cls.key = key

    @staticmethod
    def read(data) -> "LangPackStringDeleted":
        key = String.read(data)
        return LangPackStringDeleted(key=key)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.key))
        return data.getvalue()


class LangPackDifference(TL):
    ID = 0xf385c1f6

    def __init__(cls, lang_code: str, from_version: int, version: int, strings: List[TL]):
        cls.lang_code = lang_code
        cls.from_version = from_version
        cls.version = version
        cls.strings = strings

    @staticmethod
    def read(data) -> "LangPackDifference":
        lang_code = String.read(data)
        from_version = Int.read(data)
        version = Int.read(data)
        strings = data.getobj()
        return LangPackDifference(lang_code=lang_code, from_version=from_version, version=version, strings=strings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.lang_code))
        data.write(Int.getvalue(cls.from_version))
        data.write(Int.getvalue(cls.version))
        data.write(Vector().getvalue(cls.strings))
        return data.getvalue()


class LangPackLanguage(TL):
    ID = 0xeeca5ce3

    def __init__(cls, name: str, native_name: str, lang_code: str, plural_code: str, strings_count: int, translated_count: int, translations_url: str, official: bool = None, rtl: bool = None, beta: bool = None, base_lang_code: str = None):
        cls.official = official
        cls.rtl = rtl
        cls.beta = beta
        cls.name = name
        cls.native_name = native_name
        cls.lang_code = lang_code
        cls.base_lang_code = base_lang_code
        cls.plural_code = plural_code
        cls.strings_count = strings_count
        cls.translated_count = translated_count
        cls.translations_url = translations_url

    @staticmethod
    def read(data) -> "LangPackLanguage":
        flags = Int.read(data)
        official = True if flags & 1 else False
        rtl = True if flags & 4 else False
        beta = True if flags & 8 else False
        name = String.read(data)
        native_name = String.read(data)
        lang_code = String.read(data)
        base_lang_code = String.read(data) if flags & 2 else None
        plural_code = String.read(data)
        strings_count = Int.read(data)
        translated_count = Int.read(data)
        translations_url = String.read(data)
        return LangPackLanguage(official=official, rtl=rtl, beta=beta, name=name, native_name=native_name, lang_code=lang_code, base_lang_code=base_lang_code, plural_code=plural_code, strings_count=strings_count, translated_count=translated_count, translations_url=translations_url)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.official is not None else 0
        flags |= 4 if cls.rtl is not None else 0
        flags |= 8 if cls.beta is not None else 0
        flags |= 2 if cls.base_lang_code is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.name))
        data.write(String.getvalue(cls.native_name))
        data.write(String.getvalue(cls.lang_code))
        
        if cls.base_lang_code is not None:
            data.write(String.getvalue(cls.base_lang_code))
        data.write(String.getvalue(cls.plural_code))
        data.write(Int.getvalue(cls.strings_count))
        data.write(Int.getvalue(cls.translated_count))
        data.write(String.getvalue(cls.translations_url))
        return data.getvalue()


class ChannelAdminLogEventActionChangeTitle(TL):
    ID = 0xe6dfb825

    def __init__(cls, prev_value: str, new_value: str):
        cls.prev_value = prev_value
        cls.new_value = new_value

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionChangeTitle":
        prev_value = String.read(data)
        new_value = String.read(data)
        return ChannelAdminLogEventActionChangeTitle(prev_value=prev_value, new_value=new_value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.prev_value))
        data.write(String.getvalue(cls.new_value))
        return data.getvalue()


class ChannelAdminLogEventActionChangeAbout(TL):
    ID = 0x55188a2e

    def __init__(cls, prev_value: str, new_value: str):
        cls.prev_value = prev_value
        cls.new_value = new_value

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionChangeAbout":
        prev_value = String.read(data)
        new_value = String.read(data)
        return ChannelAdminLogEventActionChangeAbout(prev_value=prev_value, new_value=new_value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.prev_value))
        data.write(String.getvalue(cls.new_value))
        return data.getvalue()


class ChannelAdminLogEventActionChangeUsername(TL):
    ID = 0x6a4afc38

    def __init__(cls, prev_value: str, new_value: str):
        cls.prev_value = prev_value
        cls.new_value = new_value

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionChangeUsername":
        prev_value = String.read(data)
        new_value = String.read(data)
        return ChannelAdminLogEventActionChangeUsername(prev_value=prev_value, new_value=new_value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.prev_value))
        data.write(String.getvalue(cls.new_value))
        return data.getvalue()


class ChannelAdminLogEventActionChangePhoto(TL):
    ID = 0x434bd2af

    def __init__(cls, prev_photo: TL, new_photo: TL):
        cls.prev_photo = prev_photo
        cls.new_photo = new_photo

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionChangePhoto":
        prev_photo = data.getobj()
        new_photo = data.getobj()
        return ChannelAdminLogEventActionChangePhoto(prev_photo=prev_photo, new_photo=new_photo)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.prev_photo.getvalue())
        data.write(cls.new_photo.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionToggleInvites(TL):
    ID = 0x1b7907ae

    def __init__(cls, new_value: bool):
        cls.new_value = new_value

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionToggleInvites":
        new_value = Bool.read(data)
        return ChannelAdminLogEventActionToggleInvites(new_value=new_value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bool.getvalue(cls.new_value))
        return data.getvalue()


class ChannelAdminLogEventActionToggleSignatures(TL):
    ID = 0x26ae0971

    def __init__(cls, new_value: bool):
        cls.new_value = new_value

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionToggleSignatures":
        new_value = Bool.read(data)
        return ChannelAdminLogEventActionToggleSignatures(new_value=new_value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bool.getvalue(cls.new_value))
        return data.getvalue()


class ChannelAdminLogEventActionUpdatePinned(TL):
    ID = 0xe9e82c18

    def __init__(cls, message: TL):
        cls.message = message

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionUpdatePinned":
        message = data.getobj()
        return ChannelAdminLogEventActionUpdatePinned(message=message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.message.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionEditMessage(TL):
    ID = 0x709b2405

    def __init__(cls, prev_message: TL, new_message: TL):
        cls.prev_message = prev_message
        cls.new_message = new_message

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionEditMessage":
        prev_message = data.getobj()
        new_message = data.getobj()
        return ChannelAdminLogEventActionEditMessage(prev_message=prev_message, new_message=new_message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.prev_message.getvalue())
        data.write(cls.new_message.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionDeleteMessage(TL):
    ID = 0x42e047bb

    def __init__(cls, message: TL):
        cls.message = message

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionDeleteMessage":
        message = data.getobj()
        return ChannelAdminLogEventActionDeleteMessage(message=message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.message.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionParticipantJoin(TL):
    ID = 0x183040d3

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionParticipantJoin":
        
        return ChannelAdminLogEventActionParticipantJoin()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ChannelAdminLogEventActionParticipantLeave(TL):
    ID = 0xf89777f2

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionParticipantLeave":
        
        return ChannelAdminLogEventActionParticipantLeave()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ChannelAdminLogEventActionParticipantInvite(TL):
    ID = 0xe31c34d8

    def __init__(cls, participant: TL):
        cls.participant = participant

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionParticipantInvite":
        participant = data.getobj()
        return ChannelAdminLogEventActionParticipantInvite(participant=participant)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.participant.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionParticipantToggleBan(TL):
    ID = 0xe6d83d7e

    def __init__(cls, prev_participant: TL, new_participant: TL):
        cls.prev_participant = prev_participant
        cls.new_participant = new_participant

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionParticipantToggleBan":
        prev_participant = data.getobj()
        new_participant = data.getobj()
        return ChannelAdminLogEventActionParticipantToggleBan(prev_participant=prev_participant, new_participant=new_participant)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.prev_participant.getvalue())
        data.write(cls.new_participant.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionParticipantToggleAdmin(TL):
    ID = 0xd5676710

    def __init__(cls, prev_participant: TL, new_participant: TL):
        cls.prev_participant = prev_participant
        cls.new_participant = new_participant

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionParticipantToggleAdmin":
        prev_participant = data.getobj()
        new_participant = data.getobj()
        return ChannelAdminLogEventActionParticipantToggleAdmin(prev_participant=prev_participant, new_participant=new_participant)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.prev_participant.getvalue())
        data.write(cls.new_participant.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionChangeStickerSet(TL):
    ID = 0xb1c3caa7

    def __init__(cls, prev_stickerset: TL, new_stickerset: TL):
        cls.prev_stickerset = prev_stickerset
        cls.new_stickerset = new_stickerset

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionChangeStickerSet":
        prev_stickerset = data.getobj()
        new_stickerset = data.getobj()
        return ChannelAdminLogEventActionChangeStickerSet(prev_stickerset=prev_stickerset, new_stickerset=new_stickerset)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.prev_stickerset.getvalue())
        data.write(cls.new_stickerset.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionTogglePreHistoryHidden(TL):
    ID = 0x5f5c95f1

    def __init__(cls, new_value: bool):
        cls.new_value = new_value

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionTogglePreHistoryHidden":
        new_value = Bool.read(data)
        return ChannelAdminLogEventActionTogglePreHistoryHidden(new_value=new_value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bool.getvalue(cls.new_value))
        return data.getvalue()


class ChannelAdminLogEventActionDefaultBannedRights(TL):
    ID = 0x2df5fc0a

    def __init__(cls, prev_banned_rights: TL, new_banned_rights: TL):
        cls.prev_banned_rights = prev_banned_rights
        cls.new_banned_rights = new_banned_rights

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionDefaultBannedRights":
        prev_banned_rights = data.getobj()
        new_banned_rights = data.getobj()
        return ChannelAdminLogEventActionDefaultBannedRights(prev_banned_rights=prev_banned_rights, new_banned_rights=new_banned_rights)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.prev_banned_rights.getvalue())
        data.write(cls.new_banned_rights.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionStopPoll(TL):
    ID = 0x8f079643

    def __init__(cls, message: TL):
        cls.message = message

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionStopPoll":
        message = data.getobj()
        return ChannelAdminLogEventActionStopPoll(message=message)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.message.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionChangeLinkedChat(TL):
    ID = 0xa26f881b

    def __init__(cls, prev_value: int, new_value: int):
        cls.prev_value = prev_value
        cls.new_value = new_value

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionChangeLinkedChat":
        prev_value = Int.read(data)
        new_value = Int.read(data)
        return ChannelAdminLogEventActionChangeLinkedChat(prev_value=prev_value, new_value=new_value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.prev_value))
        data.write(Int.getvalue(cls.new_value))
        return data.getvalue()


class ChannelAdminLogEventActionChangeLocation(TL):
    ID = 0xe6b76ae

    def __init__(cls, prev_value: TL, new_value: TL):
        cls.prev_value = prev_value
        cls.new_value = new_value

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionChangeLocation":
        prev_value = data.getobj()
        new_value = data.getobj()
        return ChannelAdminLogEventActionChangeLocation(prev_value=prev_value, new_value=new_value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.prev_value.getvalue())
        data.write(cls.new_value.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionToggleSlowMode(TL):
    ID = 0x53909779

    def __init__(cls, prev_value: int, new_value: int):
        cls.prev_value = prev_value
        cls.new_value = new_value

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionToggleSlowMode":
        prev_value = Int.read(data)
        new_value = Int.read(data)
        return ChannelAdminLogEventActionToggleSlowMode(prev_value=prev_value, new_value=new_value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.prev_value))
        data.write(Int.getvalue(cls.new_value))
        return data.getvalue()


class ChannelAdminLogEventActionStartGroupCall(TL):
    ID = 0x23209745

    def __init__(cls, call: TL):
        cls.call = call

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionStartGroupCall":
        call = data.getobj()
        return ChannelAdminLogEventActionStartGroupCall(call=call)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.call.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionDiscardGroupCall(TL):
    ID = 0xdb9f9140

    def __init__(cls, call: TL):
        cls.call = call

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionDiscardGroupCall":
        call = data.getobj()
        return ChannelAdminLogEventActionDiscardGroupCall(call=call)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.call.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionParticipantMute(TL):
    ID = 0xf92424d2

    def __init__(cls, participant: TL):
        cls.participant = participant

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionParticipantMute":
        participant = data.getobj()
        return ChannelAdminLogEventActionParticipantMute(participant=participant)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.participant.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionParticipantUnmute(TL):
    ID = 0xe64429c0

    def __init__(cls, participant: TL):
        cls.participant = participant

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionParticipantUnmute":
        participant = data.getobj()
        return ChannelAdminLogEventActionParticipantUnmute(participant=participant)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.participant.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionToggleGroupCallSetting(TL):
    ID = 0x56d6a247

    def __init__(cls, join_muted: bool):
        cls.join_muted = join_muted

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionToggleGroupCallSetting":
        join_muted = Bool.read(data)
        return ChannelAdminLogEventActionToggleGroupCallSetting(join_muted=join_muted)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bool.getvalue(cls.join_muted))
        return data.getvalue()


class ChannelAdminLogEventActionParticipantJoinByInvite(TL):
    ID = 0x5cdada77

    def __init__(cls, invite: TL):
        cls.invite = invite

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionParticipantJoinByInvite":
        invite = data.getobj()
        return ChannelAdminLogEventActionParticipantJoinByInvite(invite=invite)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.invite.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionExportedInviteDelete(TL):
    ID = 0x5a50fca4

    def __init__(cls, invite: TL):
        cls.invite = invite

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionExportedInviteDelete":
        invite = data.getobj()
        return ChannelAdminLogEventActionExportedInviteDelete(invite=invite)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.invite.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionExportedInviteRevoke(TL):
    ID = 0x410a134e

    def __init__(cls, invite: TL):
        cls.invite = invite

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionExportedInviteRevoke":
        invite = data.getobj()
        return ChannelAdminLogEventActionExportedInviteRevoke(invite=invite)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.invite.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionExportedInviteEdit(TL):
    ID = 0xe90ebb59

    def __init__(cls, prev_invite: TL, new_invite: TL):
        cls.prev_invite = prev_invite
        cls.new_invite = new_invite

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionExportedInviteEdit":
        prev_invite = data.getobj()
        new_invite = data.getobj()
        return ChannelAdminLogEventActionExportedInviteEdit(prev_invite=prev_invite, new_invite=new_invite)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.prev_invite.getvalue())
        data.write(cls.new_invite.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionParticipantVolume(TL):
    ID = 0x3e7f6847

    def __init__(cls, participant: TL):
        cls.participant = participant

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionParticipantVolume":
        participant = data.getobj()
        return ChannelAdminLogEventActionParticipantVolume(participant=participant)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.participant.getvalue())
        return data.getvalue()


class ChannelAdminLogEventActionChangeHistoryTTL(TL):
    ID = 0x6e941a38

    def __init__(cls, prev_value: int, new_value: int):
        cls.prev_value = prev_value
        cls.new_value = new_value

    @staticmethod
    def read(data) -> "ChannelAdminLogEventActionChangeHistoryTTL":
        prev_value = Int.read(data)
        new_value = Int.read(data)
        return ChannelAdminLogEventActionChangeHistoryTTL(prev_value=prev_value, new_value=new_value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.prev_value))
        data.write(Int.getvalue(cls.new_value))
        return data.getvalue()


class ChannelAdminLogEvent(TL):
    ID = 0x3b5a3e40

    def __init__(cls, id: int, date: int, user_id: int, action: TL):
        cls.id = id
        cls.date = date
        cls.user_id = user_id
        cls.action = action

    @staticmethod
    def read(data) -> "ChannelAdminLogEvent":
        id = Long.read(data)
        date = Int.read(data)
        user_id = Int.read(data)
        action = data.getobj()
        return ChannelAdminLogEvent(id=id, date=date, user_id=user_id, action=action)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.user_id))
        data.write(cls.action.getvalue())
        return data.getvalue()


class ChannelAdminLogEventsFilter(TL):
    ID = 0xea107ae4

    def __init__(cls, join: bool = None, leave: bool = None, invite: bool = None, ban: bool = None, unban: bool = None, kick: bool = None, unkick: bool = None, promote: bool = None, demote: bool = None, info: bool = None, settings: bool = None, pinned: bool = None, edit: bool = None, delete: bool = None, group_call: bool = None, invites: bool = None):
        cls.join = join
        cls.leave = leave
        cls.invite = invite
        cls.ban = ban
        cls.unban = unban
        cls.kick = kick
        cls.unkick = unkick
        cls.promote = promote
        cls.demote = demote
        cls.info = info
        cls.settings = settings
        cls.pinned = pinned
        cls.edit = edit
        cls.delete = delete
        cls.group_call = group_call
        cls.invites = invites

    @staticmethod
    def read(data) -> "ChannelAdminLogEventsFilter":
        flags = Int.read(data)
        join = True if flags & 1 else False
        leave = True if flags & 2 else False
        invite = True if flags & 4 else False
        ban = True if flags & 8 else False
        unban = True if flags & 16 else False
        kick = True if flags & 32 else False
        unkick = True if flags & 64 else False
        promote = True if flags & 128 else False
        demote = True if flags & 256 else False
        info = True if flags & 512 else False
        settings = True if flags & 1024 else False
        pinned = True if flags & 2048 else False
        edit = True if flags & 4096 else False
        delete = True if flags & 8192 else False
        group_call = True if flags & 16384 else False
        invites = True if flags & 32768 else False
        return ChannelAdminLogEventsFilter(join=join, leave=leave, invite=invite, ban=ban, unban=unban, kick=kick, unkick=unkick, promote=promote, demote=demote, info=info, settings=settings, pinned=pinned, edit=edit, delete=delete, group_call=group_call, invites=invites)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.join is not None else 0
        flags |= 2 if cls.leave is not None else 0
        flags |= 4 if cls.invite is not None else 0
        flags |= 8 if cls.ban is not None else 0
        flags |= 16 if cls.unban is not None else 0
        flags |= 32 if cls.kick is not None else 0
        flags |= 64 if cls.unkick is not None else 0
        flags |= 128 if cls.promote is not None else 0
        flags |= 256 if cls.demote is not None else 0
        flags |= 512 if cls.info is not None else 0
        flags |= 1024 if cls.settings is not None else 0
        flags |= 2048 if cls.pinned is not None else 0
        flags |= 4096 if cls.edit is not None else 0
        flags |= 8192 if cls.delete is not None else 0
        flags |= 16384 if cls.group_call is not None else 0
        flags |= 32768 if cls.invites is not None else 0
        data.write(Int.getvalue(flags))
        return data.getvalue()


class PopularContact(TL):
    ID = 0x5ce14175

    def __init__(cls, client_id: int, importers: int):
        cls.client_id = client_id
        cls.importers = importers

    @staticmethod
    def read(data) -> "PopularContact":
        client_id = Long.read(data)
        importers = Int.read(data)
        return PopularContact(client_id=client_id, importers=importers)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.client_id))
        data.write(Int.getvalue(cls.importers))
        return data.getvalue()


class RecentMeUrlUnknown(TL):
    ID = 0x46e1d13d

    def __init__(cls, url: str):
        cls.url = url

    @staticmethod
    def read(data) -> "RecentMeUrlUnknown":
        url = String.read(data)
        return RecentMeUrlUnknown(url=url)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        return data.getvalue()


class RecentMeUrlUser(TL):
    ID = 0x8dbc3336

    def __init__(cls, url: str, user_id: int):
        cls.url = url
        cls.user_id = user_id

    @staticmethod
    def read(data) -> "RecentMeUrlUser":
        url = String.read(data)
        user_id = Int.read(data)
        return RecentMeUrlUser(url=url, user_id=user_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        data.write(Int.getvalue(cls.user_id))
        return data.getvalue()


class RecentMeUrlChat(TL):
    ID = 0xa01b22f9

    def __init__(cls, url: str, chat_id: int):
        cls.url = url
        cls.chat_id = chat_id

    @staticmethod
    def read(data) -> "RecentMeUrlChat":
        url = String.read(data)
        chat_id = Int.read(data)
        return RecentMeUrlChat(url=url, chat_id=chat_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        data.write(Int.getvalue(cls.chat_id))
        return data.getvalue()


class RecentMeUrlChatInvite(TL):
    ID = 0xeb49081d

    def __init__(cls, url: str, chat_invite: TL):
        cls.url = url
        cls.chat_invite = chat_invite

    @staticmethod
    def read(data) -> "RecentMeUrlChatInvite":
        url = String.read(data)
        chat_invite = data.getobj()
        return RecentMeUrlChatInvite(url=url, chat_invite=chat_invite)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        data.write(cls.chat_invite.getvalue())
        return data.getvalue()


class RecentMeUrlStickerSet(TL):
    ID = 0xbc0a57dc

    def __init__(cls, url: str, set: TL):
        cls.url = url
        cls.set = set

    @staticmethod
    def read(data) -> "RecentMeUrlStickerSet":
        url = String.read(data)
        set = data.getobj()
        return RecentMeUrlStickerSet(url=url, set=set)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        data.write(cls.set.getvalue())
        return data.getvalue()


class InputSingleMedia(TL):
    ID = 0x1cc6e91f

    def __init__(cls, media: TL, random_id: int, message: str, entities: List[TL] = None):
        cls.media = media
        cls.random_id = random_id
        cls.message = message
        cls.entities = entities

    @staticmethod
    def read(data) -> "InputSingleMedia":
        flags = Int.read(data)
        media = data.getobj()
        random_id = Long.read(data)
        message = String.read(data)
        entities = data.getobj() if flags & 1 else []
        return InputSingleMedia(media=media, random_id=random_id, message=message, entities=entities)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.entities is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.media.getvalue())
        data.write(Long.getvalue(cls.random_id))
        data.write(String.getvalue(cls.message))
        
        if cls.entities is not None:
            data.write(Vector().getvalue(cls.entities))
        return data.getvalue()


class WebAuthorization(TL):
    ID = 0xcac943f2

    def __init__(cls, hash: int, bot_id: int, domain: str, browser: str, platform: str, date_created: int, date_active: int, ip: str, region: str):
        cls.hash = hash
        cls.bot_id = bot_id
        cls.domain = domain
        cls.browser = browser
        cls.platform = platform
        cls.date_created = date_created
        cls.date_active = date_active
        cls.ip = ip
        cls.region = region

    @staticmethod
    def read(data) -> "WebAuthorization":
        hash = Long.read(data)
        bot_id = Int.read(data)
        domain = String.read(data)
        browser = String.read(data)
        platform = String.read(data)
        date_created = Int.read(data)
        date_active = Int.read(data)
        ip = String.read(data)
        region = String.read(data)
        return WebAuthorization(hash=hash, bot_id=bot_id, domain=domain, browser=browser, platform=platform, date_created=date_created, date_active=date_active, ip=ip, region=region)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.hash))
        data.write(Int.getvalue(cls.bot_id))
        data.write(String.getvalue(cls.domain))
        data.write(String.getvalue(cls.browser))
        data.write(String.getvalue(cls.platform))
        data.write(Int.getvalue(cls.date_created))
        data.write(Int.getvalue(cls.date_active))
        data.write(String.getvalue(cls.ip))
        data.write(String.getvalue(cls.region))
        return data.getvalue()


class InputMessageID(TL):
    ID = 0xa676a322

    def __init__(cls, id: int):
        cls.id = id

    @staticmethod
    def read(data) -> "InputMessageID":
        id = Int.read(data)
        return InputMessageID(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.id))
        return data.getvalue()


class InputMessageReplyTo(TL):
    ID = 0xbad88395

    def __init__(cls, id: int):
        cls.id = id

    @staticmethod
    def read(data) -> "InputMessageReplyTo":
        id = Int.read(data)
        return InputMessageReplyTo(id=id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.id))
        return data.getvalue()


class InputMessagePinned(TL):
    ID = 0x86872538

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputMessagePinned":
        
        return InputMessagePinned()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputMessageCallbackQuery(TL):
    ID = 0xacfa1a7e

    def __init__(cls, id: int, query_id: int):
        cls.id = id
        cls.query_id = query_id

    @staticmethod
    def read(data) -> "InputMessageCallbackQuery":
        id = Int.read(data)
        query_id = Long.read(data)
        return InputMessageCallbackQuery(id=id, query_id=query_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.id))
        data.write(Long.getvalue(cls.query_id))
        return data.getvalue()


class InputDialogPeer(TL):
    ID = 0xfcaafeb7

    def __init__(cls, peer: TL):
        cls.peer = peer

    @staticmethod
    def read(data) -> "InputDialogPeer":
        peer = data.getobj()
        return InputDialogPeer(peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class InputDialogPeerFolder(TL):
    ID = 0x64600527

    def __init__(cls, folder_id: int):
        cls.folder_id = folder_id

    @staticmethod
    def read(data) -> "InputDialogPeerFolder":
        folder_id = Int.read(data)
        return InputDialogPeerFolder(folder_id=folder_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.folder_id))
        return data.getvalue()


class DialogPeer(TL):
    ID = 0xe56dbf05

    def __init__(cls, peer: TL):
        cls.peer = peer

    @staticmethod
    def read(data) -> "DialogPeer":
        peer = data.getobj()
        return DialogPeer(peer=peer)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        return data.getvalue()


class DialogPeerFolder(TL):
    ID = 0x514519e2

    def __init__(cls, folder_id: int):
        cls.folder_id = folder_id

    @staticmethod
    def read(data) -> "DialogPeerFolder":
        folder_id = Int.read(data)
        return DialogPeerFolder(folder_id=folder_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.folder_id))
        return data.getvalue()


class FileHash(TL):
    ID = 0x6242c773

    def __init__(cls, offset: int, limit: int, hash: bytes):
        cls.offset = offset
        cls.limit = limit
        cls.hash = hash

    @staticmethod
    def read(data) -> "FileHash":
        offset = Int.read(data)
        limit = Int.read(data)
        hash = Bytes.read(data)
        return FileHash(offset=offset, limit=limit, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.offset))
        data.write(Int.getvalue(cls.limit))
        data.write(Bytes.getvalue(cls.hash))
        return data.getvalue()


class InputClientProxy(TL):
    ID = 0x75588b3f

    def __init__(cls, address: str, port: int):
        cls.address = address
        cls.port = port

    @staticmethod
    def read(data) -> "InputClientProxy":
        address = String.read(data)
        port = Int.read(data)
        return InputClientProxy(address=address, port=port)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.address))
        data.write(Int.getvalue(cls.port))
        return data.getvalue()


class InputSecureFileUploaded(TL):
    ID = 0x3334b0f0

    def __init__(cls, id: int, parts: int, md5_checksum: str, file_hash: bytes, secret: bytes):
        cls.id = id
        cls.parts = parts
        cls.md5_checksum = md5_checksum
        cls.file_hash = file_hash
        cls.secret = secret

    @staticmethod
    def read(data) -> "InputSecureFileUploaded":
        id = Long.read(data)
        parts = Int.read(data)
        md5_checksum = String.read(data)
        file_hash = Bytes.read(data)
        secret = Bytes.read(data)
        return InputSecureFileUploaded(id=id, parts=parts, md5_checksum=md5_checksum, file_hash=file_hash, secret=secret)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Int.getvalue(cls.parts))
        data.write(String.getvalue(cls.md5_checksum))
        data.write(Bytes.getvalue(cls.file_hash))
        data.write(Bytes.getvalue(cls.secret))
        return data.getvalue()


class InputSecureFile(TL):
    ID = 0x5367e5be

    def __init__(cls, id: int, access_hash: int):
        cls.id = id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputSecureFile":
        id = Long.read(data)
        access_hash = Long.read(data)
        return InputSecureFile(id=id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class SecureFileEmpty(TL):
    ID = 0x64199744

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SecureFileEmpty":
        
        return SecureFileEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SecureFile(TL):
    ID = 0xe0277a62

    def __init__(cls, id: int, access_hash: int, size: int, dc_id: int, date: int, file_hash: bytes, secret: bytes):
        cls.id = id
        cls.access_hash = access_hash
        cls.size = size
        cls.dc_id = dc_id
        cls.date = date
        cls.file_hash = file_hash
        cls.secret = secret

    @staticmethod
    def read(data) -> "SecureFile":
        id = Long.read(data)
        access_hash = Long.read(data)
        size = Int.read(data)
        dc_id = Int.read(data)
        date = Int.read(data)
        file_hash = Bytes.read(data)
        secret = Bytes.read(data)
        return SecureFile(id=id, access_hash=access_hash, size=size, dc_id=dc_id, date=date, file_hash=file_hash, secret=secret)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Int.getvalue(cls.size))
        data.write(Int.getvalue(cls.dc_id))
        data.write(Int.getvalue(cls.date))
        data.write(Bytes.getvalue(cls.file_hash))
        data.write(Bytes.getvalue(cls.secret))
        return data.getvalue()


class SecureData(TL):
    ID = 0x8aeabec3

    def __init__(cls, data: bytes, data_hash: bytes, secret: bytes):
        cls.data = data
        cls.data_hash = data_hash
        cls.secret = secret

    @staticmethod
    def read(data) -> "SecureData":
        data = Bytes.read(data)
        data_hash = Bytes.read(data)
        secret = Bytes.read(data)
        return SecureData(data=data, data_hash=data_hash, secret=secret)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.data))
        data.write(Bytes.getvalue(cls.data_hash))
        data.write(Bytes.getvalue(cls.secret))
        return data.getvalue()


class SecurePlainPhone(TL):
    ID = 0x7d6099dd

    def __init__(cls, phone: str):
        cls.phone = phone

    @staticmethod
    def read(data) -> "SecurePlainPhone":
        phone = String.read(data)
        return SecurePlainPhone(phone=phone)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone))
        return data.getvalue()


class SecurePlainEmail(TL):
    ID = 0x21ec5a5f

    def __init__(cls, email: str):
        cls.email = email

    @staticmethod
    def read(data) -> "SecurePlainEmail":
        email = String.read(data)
        return SecurePlainEmail(email=email)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.email))
        return data.getvalue()


class SecureValueTypePersonalDetails(TL):
    ID = 0x9d2a81e3

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SecureValueTypePersonalDetails":
        
        return SecureValueTypePersonalDetails()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SecureValueTypePassport(TL):
    ID = 0x3dac6a00

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SecureValueTypePassport":
        
        return SecureValueTypePassport()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SecureValueTypeDriverLicense(TL):
    ID = 0x6e425c4

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SecureValueTypeDriverLicense":
        
        return SecureValueTypeDriverLicense()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SecureValueTypeIdentityCard(TL):
    ID = 0xa0d0744b

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SecureValueTypeIdentityCard":
        
        return SecureValueTypeIdentityCard()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SecureValueTypeInternalPassport(TL):
    ID = 0x99a48f23

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SecureValueTypeInternalPassport":
        
        return SecureValueTypeInternalPassport()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SecureValueTypeAddress(TL):
    ID = 0xcbe31e26

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SecureValueTypeAddress":
        
        return SecureValueTypeAddress()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SecureValueTypeUtilityBill(TL):
    ID = 0xfc36954e

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SecureValueTypeUtilityBill":
        
        return SecureValueTypeUtilityBill()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SecureValueTypeBankStatement(TL):
    ID = 0x89137c0d

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SecureValueTypeBankStatement":
        
        return SecureValueTypeBankStatement()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SecureValueTypeRentalAgreement(TL):
    ID = 0x8b883488

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SecureValueTypeRentalAgreement":
        
        return SecureValueTypeRentalAgreement()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SecureValueTypePassportRegistration(TL):
    ID = 0x99e3806a

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SecureValueTypePassportRegistration":
        
        return SecureValueTypePassportRegistration()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SecureValueTypeTemporaryRegistration(TL):
    ID = 0xea02ec33

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SecureValueTypeTemporaryRegistration":
        
        return SecureValueTypeTemporaryRegistration()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SecureValueTypePhone(TL):
    ID = 0xb320aadb

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SecureValueTypePhone":
        
        return SecureValueTypePhone()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SecureValueTypeEmail(TL):
    ID = 0x8e3ca7ee

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SecureValueTypeEmail":
        
        return SecureValueTypeEmail()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SecureValue(TL):
    ID = 0x187fa0ca

    def __init__(cls, type: TL, hash: bytes, data: TL = None, front_side: TL = None, reverse_side: TL = None, selfie: TL = None, translation: List[TL] = None, files: List[TL] = None, plain_data: TL = None):
        cls.type = type
        cls.data = data
        cls.front_side = front_side
        cls.reverse_side = reverse_side
        cls.selfie = selfie
        cls.translation = translation
        cls.files = files
        cls.plain_data = plain_data
        cls.hash = hash

    @staticmethod
    def read(data) -> "SecureValue":
        flags = Int.read(data)
        type = data.getobj()
        data = data.getobj() if flags & 1 else None
        front_side = data.getobj() if flags & 2 else None
        reverse_side = data.getobj() if flags & 4 else None
        selfie = data.getobj() if flags & 8 else None
        translation = data.getobj() if flags & 64 else []
        files = data.getobj() if flags & 16 else []
        plain_data = data.getobj() if flags & 32 else None
        hash = Bytes.read(data)
        return SecureValue(type=type, data=data, front_side=front_side, reverse_side=reverse_side, selfie=selfie, translation=translation, files=files, plain_data=plain_data, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.data is not None else 0
        flags |= 2 if cls.front_side is not None else 0
        flags |= 4 if cls.reverse_side is not None else 0
        flags |= 8 if cls.selfie is not None else 0
        flags |= 64 if cls.translation is not None else 0
        flags |= 16 if cls.files is not None else 0
        flags |= 32 if cls.plain_data is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.type.getvalue())
        
        if cls.data is not None:
            data.write(cls.data.getvalue())
        
        if cls.front_side is not None:
            data.write(cls.front_side.getvalue())
        
        if cls.reverse_side is not None:
            data.write(cls.reverse_side.getvalue())
        
        if cls.selfie is not None:
            data.write(cls.selfie.getvalue())
        
        if cls.translation is not None:
            data.write(Vector().getvalue(cls.translation))
        
        if cls.files is not None:
            data.write(Vector().getvalue(cls.files))
        
        if cls.plain_data is not None:
            data.write(cls.plain_data.getvalue())
        data.write(Bytes.getvalue(cls.hash))
        return data.getvalue()


class InputSecureValue(TL):
    ID = 0xdb21d0a7

    def __init__(cls, type: TL, data: TL = None, front_side: TL = None, reverse_side: TL = None, selfie: TL = None, translation: List[TL] = None, files: List[TL] = None, plain_data: TL = None):
        cls.type = type
        cls.data = data
        cls.front_side = front_side
        cls.reverse_side = reverse_side
        cls.selfie = selfie
        cls.translation = translation
        cls.files = files
        cls.plain_data = plain_data

    @staticmethod
    def read(data) -> "InputSecureValue":
        flags = Int.read(data)
        type = data.getobj()
        data = data.getobj() if flags & 1 else None
        front_side = data.getobj() if flags & 2 else None
        reverse_side = data.getobj() if flags & 4 else None
        selfie = data.getobj() if flags & 8 else None
        translation = data.getobj() if flags & 64 else []
        files = data.getobj() if flags & 16 else []
        plain_data = data.getobj() if flags & 32 else None
        return InputSecureValue(type=type, data=data, front_side=front_side, reverse_side=reverse_side, selfie=selfie, translation=translation, files=files, plain_data=plain_data)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.data is not None else 0
        flags |= 2 if cls.front_side is not None else 0
        flags |= 4 if cls.reverse_side is not None else 0
        flags |= 8 if cls.selfie is not None else 0
        flags |= 64 if cls.translation is not None else 0
        flags |= 16 if cls.files is not None else 0
        flags |= 32 if cls.plain_data is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.type.getvalue())
        
        if cls.data is not None:
            data.write(cls.data.getvalue())
        
        if cls.front_side is not None:
            data.write(cls.front_side.getvalue())
        
        if cls.reverse_side is not None:
            data.write(cls.reverse_side.getvalue())
        
        if cls.selfie is not None:
            data.write(cls.selfie.getvalue())
        
        if cls.translation is not None:
            data.write(Vector().getvalue(cls.translation))
        
        if cls.files is not None:
            data.write(Vector().getvalue(cls.files))
        
        if cls.plain_data is not None:
            data.write(cls.plain_data.getvalue())
        return data.getvalue()


class SecureValueHash(TL):
    ID = 0xed1ecdb0

    def __init__(cls, type: TL, hash: bytes):
        cls.type = type
        cls.hash = hash

    @staticmethod
    def read(data) -> "SecureValueHash":
        type = data.getobj()
        hash = Bytes.read(data)
        return SecureValueHash(type=type, hash=hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.type.getvalue())
        data.write(Bytes.getvalue(cls.hash))
        return data.getvalue()


class SecureValueErrorData(TL):
    ID = 0xe8a40bd9

    def __init__(cls, type: TL, data_hash: bytes, field: str, text: str):
        cls.type = type
        cls.data_hash = data_hash
        cls.field = field
        cls.text = text

    @staticmethod
    def read(data) -> "SecureValueErrorData":
        type = data.getobj()
        data_hash = Bytes.read(data)
        field = String.read(data)
        text = String.read(data)
        return SecureValueErrorData(type=type, data_hash=data_hash, field=field, text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.type.getvalue())
        data.write(Bytes.getvalue(cls.data_hash))
        data.write(String.getvalue(cls.field))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class SecureValueErrorFrontSide(TL):
    ID = 0xbe3dfa

    def __init__(cls, type: TL, file_hash: bytes, text: str):
        cls.type = type
        cls.file_hash = file_hash
        cls.text = text

    @staticmethod
    def read(data) -> "SecureValueErrorFrontSide":
        type = data.getobj()
        file_hash = Bytes.read(data)
        text = String.read(data)
        return SecureValueErrorFrontSide(type=type, file_hash=file_hash, text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.type.getvalue())
        data.write(Bytes.getvalue(cls.file_hash))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class SecureValueErrorReverseSide(TL):
    ID = 0x868a2aa5

    def __init__(cls, type: TL, file_hash: bytes, text: str):
        cls.type = type
        cls.file_hash = file_hash
        cls.text = text

    @staticmethod
    def read(data) -> "SecureValueErrorReverseSide":
        type = data.getobj()
        file_hash = Bytes.read(data)
        text = String.read(data)
        return SecureValueErrorReverseSide(type=type, file_hash=file_hash, text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.type.getvalue())
        data.write(Bytes.getvalue(cls.file_hash))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class SecureValueErrorSelfie(TL):
    ID = 0xe537ced6

    def __init__(cls, type: TL, file_hash: bytes, text: str):
        cls.type = type
        cls.file_hash = file_hash
        cls.text = text

    @staticmethod
    def read(data) -> "SecureValueErrorSelfie":
        type = data.getobj()
        file_hash = Bytes.read(data)
        text = String.read(data)
        return SecureValueErrorSelfie(type=type, file_hash=file_hash, text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.type.getvalue())
        data.write(Bytes.getvalue(cls.file_hash))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class SecureValueErrorFile(TL):
    ID = 0x7a700873

    def __init__(cls, type: TL, file_hash: bytes, text: str):
        cls.type = type
        cls.file_hash = file_hash
        cls.text = text

    @staticmethod
    def read(data) -> "SecureValueErrorFile":
        type = data.getobj()
        file_hash = Bytes.read(data)
        text = String.read(data)
        return SecureValueErrorFile(type=type, file_hash=file_hash, text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.type.getvalue())
        data.write(Bytes.getvalue(cls.file_hash))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class SecureValueErrorFiles(TL):
    ID = 0x666220e9

    def __init__(cls, type: TL, file_hash: List[bytes], text: str):
        cls.type = type
        cls.file_hash = file_hash
        cls.text = text

    @staticmethod
    def read(data) -> "SecureValueErrorFiles":
        type = data.getobj()
        file_hash = data.getobj(Bytes)
        text = String.read(data)
        return SecureValueErrorFiles(type=type, file_hash=file_hash, text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.type.getvalue())
        data.write(Vector().getvalue(cls.file_hash, Bytes))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class SecureValueError(TL):
    ID = 0x869d758f

    def __init__(cls, type: TL, hash: bytes, text: str):
        cls.type = type
        cls.hash = hash
        cls.text = text

    @staticmethod
    def read(data) -> "SecureValueError":
        type = data.getobj()
        hash = Bytes.read(data)
        text = String.read(data)
        return SecureValueError(type=type, hash=hash, text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.type.getvalue())
        data.write(Bytes.getvalue(cls.hash))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class SecureValueErrorTranslationFile(TL):
    ID = 0xa1144770

    def __init__(cls, type: TL, file_hash: bytes, text: str):
        cls.type = type
        cls.file_hash = file_hash
        cls.text = text

    @staticmethod
    def read(data) -> "SecureValueErrorTranslationFile":
        type = data.getobj()
        file_hash = Bytes.read(data)
        text = String.read(data)
        return SecureValueErrorTranslationFile(type=type, file_hash=file_hash, text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.type.getvalue())
        data.write(Bytes.getvalue(cls.file_hash))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class SecureValueErrorTranslationFiles(TL):
    ID = 0x34636dd8

    def __init__(cls, type: TL, file_hash: List[bytes], text: str):
        cls.type = type
        cls.file_hash = file_hash
        cls.text = text

    @staticmethod
    def read(data) -> "SecureValueErrorTranslationFiles":
        type = data.getobj()
        file_hash = data.getobj(Bytes)
        text = String.read(data)
        return SecureValueErrorTranslationFiles(type=type, file_hash=file_hash, text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.type.getvalue())
        data.write(Vector().getvalue(cls.file_hash, Bytes))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class SecureCredentialsEncrypted(TL):
    ID = 0x33f0ea47

    def __init__(cls, data: bytes, hash: bytes, secret: bytes):
        cls.data = data
        cls.hash = hash
        cls.secret = secret

    @staticmethod
    def read(data) -> "SecureCredentialsEncrypted":
        data = Bytes.read(data)
        hash = Bytes.read(data)
        secret = Bytes.read(data)
        return SecureCredentialsEncrypted(data=data, hash=hash, secret=secret)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.data))
        data.write(Bytes.getvalue(cls.hash))
        data.write(Bytes.getvalue(cls.secret))
        return data.getvalue()


class SavedPhoneContact(TL):
    ID = 0x1142bd56

    def __init__(cls, phone: str, first_name: str, last_name: str, date: int):
        cls.phone = phone
        cls.first_name = first_name
        cls.last_name = last_name
        cls.date = date

    @staticmethod
    def read(data) -> "SavedPhoneContact":
        phone = String.read(data)
        first_name = String.read(data)
        last_name = String.read(data)
        date = Int.read(data)
        return SavedPhoneContact(phone=phone, first_name=first_name, last_name=last_name, date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.phone))
        data.write(String.getvalue(cls.first_name))
        data.write(String.getvalue(cls.last_name))
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class PasswordKdfAlgoUnknown(TL):
    ID = 0xd45ab096

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "PasswordKdfAlgoUnknown":
        
        return PasswordKdfAlgoUnknown()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow(TL):
    ID = 0x3a912d4a

    def __init__(cls, salt1: bytes, salt2: bytes, g: int, p: bytes):
        cls.salt1 = salt1
        cls.salt2 = salt2
        cls.g = g
        cls.p = p

    @staticmethod
    def read(data) -> "PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow":
        salt1 = Bytes.read(data)
        salt2 = Bytes.read(data)
        g = Int.read(data)
        p = Bytes.read(data)
        return PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow(salt1=salt1, salt2=salt2, g=g, p=p)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.salt1))
        data.write(Bytes.getvalue(cls.salt2))
        data.write(Int.getvalue(cls.g))
        data.write(Bytes.getvalue(cls.p))
        return data.getvalue()


class SecurePasswordKdfAlgoUnknown(TL):
    ID = 0x4a8537

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "SecurePasswordKdfAlgoUnknown":
        
        return SecurePasswordKdfAlgoUnknown()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000(TL):
    ID = 0xbbf2dda0

    def __init__(cls, salt: bytes):
        cls.salt = salt

    @staticmethod
    def read(data) -> "SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000":
        salt = Bytes.read(data)
        return SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000(salt=salt)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.salt))
        return data.getvalue()


class SecurePasswordKdfAlgoSHA512(TL):
    ID = 0x86471d92

    def __init__(cls, salt: bytes):
        cls.salt = salt

    @staticmethod
    def read(data) -> "SecurePasswordKdfAlgoSHA512":
        salt = Bytes.read(data)
        return SecurePasswordKdfAlgoSHA512(salt=salt)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bytes.getvalue(cls.salt))
        return data.getvalue()


class SecureSecretSettings(TL):
    ID = 0x1527bcac

    def __init__(cls, secure_algo: TL, secure_secret: bytes, secure_secret_id: int):
        cls.secure_algo = secure_algo
        cls.secure_secret = secure_secret
        cls.secure_secret_id = secure_secret_id

    @staticmethod
    def read(data) -> "SecureSecretSettings":
        secure_algo = data.getobj()
        secure_secret = Bytes.read(data)
        secure_secret_id = Long.read(data)
        return SecureSecretSettings(secure_algo=secure_algo, secure_secret=secure_secret, secure_secret_id=secure_secret_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.secure_algo.getvalue())
        data.write(Bytes.getvalue(cls.secure_secret))
        data.write(Long.getvalue(cls.secure_secret_id))
        return data.getvalue()


class InputCheckPasswordEmpty(TL):
    ID = 0x9880f658

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputCheckPasswordEmpty":
        
        return InputCheckPasswordEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputCheckPasswordSRP(TL):
    ID = 0xd27ff082

    def __init__(cls, srp_id: int, A: bytes, M1: bytes):
        cls.srp_id = srp_id
        cls.A = A
        cls.M1 = M1

    @staticmethod
    def read(data) -> "InputCheckPasswordSRP":
        srp_id = Long.read(data)
        A = Bytes.read(data)
        M1 = Bytes.read(data)
        return InputCheckPasswordSRP(srp_id=srp_id, A=A, M1=M1)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.srp_id))
        data.write(Bytes.getvalue(cls.A))
        data.write(Bytes.getvalue(cls.M1))
        return data.getvalue()


class SecureRequiredType(TL):
    ID = 0x829d99da

    def __init__(cls, type: TL, native_names: bool = None, selfie_required: bool = None, translation_required: bool = None):
        cls.native_names = native_names
        cls.selfie_required = selfie_required
        cls.translation_required = translation_required
        cls.type = type

    @staticmethod
    def read(data) -> "SecureRequiredType":
        flags = Int.read(data)
        native_names = True if flags & 1 else False
        selfie_required = True if flags & 2 else False
        translation_required = True if flags & 4 else False
        type = data.getobj()
        return SecureRequiredType(native_names=native_names, selfie_required=selfie_required, translation_required=translation_required, type=type)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.native_names is not None else 0
        flags |= 2 if cls.selfie_required is not None else 0
        flags |= 4 if cls.translation_required is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.type.getvalue())
        return data.getvalue()


class SecureRequiredTypeOneOf(TL):
    ID = 0x27477b4

    def __init__(cls, types: List[TL]):
        cls.types = types

    @staticmethod
    def read(data) -> "SecureRequiredTypeOneOf":
        types = data.getobj()
        return SecureRequiredTypeOneOf(types=types)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.types))
        return data.getvalue()


class InputAppEvent(TL):
    ID = 0x1d1b1245

    def __init__(cls, time: float, type: str, peer: int, data: TL):
        cls.time = time
        cls.type = type
        cls.peer = peer
        cls.data = data

    @staticmethod
    def read(data) -> "InputAppEvent":
        time = Double.read(data)
        type = String.read(data)
        peer = Long.read(data)
        data = data.getobj()
        return InputAppEvent(time=time, type=type, peer=peer, data=data)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Double.getvalue(cls.time))
        data.write(String.getvalue(cls.type))
        data.write(Long.getvalue(cls.peer))
        data.write(cls.data.getvalue())
        return data.getvalue()


class JsonObjectValue(TL):
    ID = 0xc0de1bd9

    def __init__(cls, key: str, value: TL):
        cls.key = key
        cls.value = value

    @staticmethod
    def read(data) -> "JsonObjectValue":
        key = String.read(data)
        value = data.getobj()
        return JsonObjectValue(key=key, value=value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.key))
        data.write(cls.value.getvalue())
        return data.getvalue()


class JsonNull(TL):
    ID = 0x3f6d7b68

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "JsonNull":
        
        return JsonNull()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class JsonBool(TL):
    ID = 0xc7345e6a

    def __init__(cls, value: bool):
        cls.value = value

    @staticmethod
    def read(data) -> "JsonBool":
        value = Bool.read(data)
        return JsonBool(value=value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Bool.getvalue(cls.value))
        return data.getvalue()


class JsonNumber(TL):
    ID = 0x2be0dfa4

    def __init__(cls, value: float):
        cls.value = value

    @staticmethod
    def read(data) -> "JsonNumber":
        value = Double.read(data)
        return JsonNumber(value=value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Double.getvalue(cls.value))
        return data.getvalue()


class JsonString(TL):
    ID = 0xb71e767a

    def __init__(cls, value: str):
        cls.value = value

    @staticmethod
    def read(data) -> "JsonString":
        value = String.read(data)
        return JsonString(value=value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.value))
        return data.getvalue()


class JsonArray(TL):
    ID = 0xf7444763

    def __init__(cls, value: List[TL]):
        cls.value = value

    @staticmethod
    def read(data) -> "JsonArray":
        value = data.getobj()
        return JsonArray(value=value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.value))
        return data.getvalue()


class JsonObject(TL):
    ID = 0x99c1d49d

    def __init__(cls, value: List[TL]):
        cls.value = value

    @staticmethod
    def read(data) -> "JsonObject":
        value = data.getobj()
        return JsonObject(value=value)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.value))
        return data.getvalue()


class PageTableCell(TL):
    ID = 0x34566b6a

    def __init__(cls, header: bool = None, align_center: bool = None, align_right: bool = None, valign_middle: bool = None, valign_bottom: bool = None, text: TL = None, colspan: int = None, rowspan: int = None):
        cls.header = header
        cls.align_center = align_center
        cls.align_right = align_right
        cls.valign_middle = valign_middle
        cls.valign_bottom = valign_bottom
        cls.text = text
        cls.colspan = colspan
        cls.rowspan = rowspan

    @staticmethod
    def read(data) -> "PageTableCell":
        flags = Int.read(data)
        header = True if flags & 1 else False
        align_center = True if flags & 8 else False
        align_right = True if flags & 16 else False
        valign_middle = True if flags & 32 else False
        valign_bottom = True if flags & 64 else False
        text = data.getobj() if flags & 128 else None
        colspan = Int.read(data) if flags & 2 else None
        rowspan = Int.read(data) if flags & 4 else None
        return PageTableCell(header=header, align_center=align_center, align_right=align_right, valign_middle=valign_middle, valign_bottom=valign_bottom, text=text, colspan=colspan, rowspan=rowspan)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.header is not None else 0
        flags |= 8 if cls.align_center is not None else 0
        flags |= 16 if cls.align_right is not None else 0
        flags |= 32 if cls.valign_middle is not None else 0
        flags |= 64 if cls.valign_bottom is not None else 0
        flags |= 128 if cls.text is not None else 0
        flags |= 2 if cls.colspan is not None else 0
        flags |= 4 if cls.rowspan is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.text is not None:
            data.write(cls.text.getvalue())
        
        if cls.colspan is not None:
            data.write(Int.getvalue(cls.colspan))
        
        if cls.rowspan is not None:
            data.write(Int.getvalue(cls.rowspan))
        return data.getvalue()


class PageTableRow(TL):
    ID = 0xe0c0c5e5

    def __init__(cls, cells: List[TL]):
        cls.cells = cells

    @staticmethod
    def read(data) -> "PageTableRow":
        cells = data.getobj()
        return PageTableRow(cells=cells)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.cells))
        return data.getvalue()


class PageCaption(TL):
    ID = 0x6f747657

    def __init__(cls, text: TL, credit: TL):
        cls.text = text
        cls.credit = credit

    @staticmethod
    def read(data) -> "PageCaption":
        text = data.getobj()
        credit = data.getobj()
        return PageCaption(text=text, credit=credit)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        data.write(cls.credit.getvalue())
        return data.getvalue()


class PageListItemText(TL):
    ID = 0xb92fb6cd

    def __init__(cls, text: TL):
        cls.text = text

    @staticmethod
    def read(data) -> "PageListItemText":
        text = data.getobj()
        return PageListItemText(text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.text.getvalue())
        return data.getvalue()


class PageListItemBlocks(TL):
    ID = 0x25e073fc

    def __init__(cls, blocks: List[TL]):
        cls.blocks = blocks

    @staticmethod
    def read(data) -> "PageListItemBlocks":
        blocks = data.getobj()
        return PageListItemBlocks(blocks=blocks)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.blocks))
        return data.getvalue()


class PageListOrderedItemText(TL):
    ID = 0x5e068047

    def __init__(cls, num: str, text: TL):
        cls.num = num
        cls.text = text

    @staticmethod
    def read(data) -> "PageListOrderedItemText":
        num = String.read(data)
        text = data.getobj()
        return PageListOrderedItemText(num=num, text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.num))
        data.write(cls.text.getvalue())
        return data.getvalue()


class PageListOrderedItemBlocks(TL):
    ID = 0x98dd8936

    def __init__(cls, num: str, blocks: List[TL]):
        cls.num = num
        cls.blocks = blocks

    @staticmethod
    def read(data) -> "PageListOrderedItemBlocks":
        num = String.read(data)
        blocks = data.getobj()
        return PageListOrderedItemBlocks(num=num, blocks=blocks)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.num))
        data.write(Vector().getvalue(cls.blocks))
        return data.getvalue()


class PageRelatedArticle(TL):
    ID = 0xb390dc08

    def __init__(cls, url: str, webpage_id: int, title: str = None, description: str = None, photo_id: int = None, author: str = None, published_date: int = None):
        cls.url = url
        cls.webpage_id = webpage_id
        cls.title = title
        cls.description = description
        cls.photo_id = photo_id
        cls.author = author
        cls.published_date = published_date

    @staticmethod
    def read(data) -> "PageRelatedArticle":
        flags = Int.read(data)
        url = String.read(data)
        webpage_id = Long.read(data)
        title = String.read(data) if flags & 1 else None
        description = String.read(data) if flags & 2 else None
        photo_id = Long.read(data) if flags & 4 else None
        author = String.read(data) if flags & 8 else None
        published_date = Int.read(data) if flags & 16 else None
        return PageRelatedArticle(url=url, webpage_id=webpage_id, title=title, description=description, photo_id=photo_id, author=author, published_date=published_date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.title is not None else 0
        flags |= 2 if cls.description is not None else 0
        flags |= 4 if cls.photo_id is not None else 0
        flags |= 8 if cls.author is not None else 0
        flags |= 16 if cls.published_date is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.url))
        data.write(Long.getvalue(cls.webpage_id))
        
        if cls.title is not None:
            data.write(String.getvalue(cls.title))
        
        if cls.description is not None:
            data.write(String.getvalue(cls.description))
        
        if cls.photo_id is not None:
            data.write(Long.getvalue(cls.photo_id))
        
        if cls.author is not None:
            data.write(String.getvalue(cls.author))
        
        if cls.published_date is not None:
            data.write(Int.getvalue(cls.published_date))
        return data.getvalue()


class Page(TL):
    ID = 0x98657f0d

    def __init__(cls, url: str, blocks: List[TL], photos: List[TL], documents: List[TL], part: bool = None, rtl: bool = None, v2: bool = None, views: int = None):
        cls.part = part
        cls.rtl = rtl
        cls.v2 = v2
        cls.url = url
        cls.blocks = blocks
        cls.photos = photos
        cls.documents = documents
        cls.views = views

    @staticmethod
    def read(data) -> "Page":
        flags = Int.read(data)
        part = True if flags & 1 else False
        rtl = True if flags & 2 else False
        v2 = True if flags & 4 else False
        url = String.read(data)
        blocks = data.getobj()
        photos = data.getobj()
        documents = data.getobj()
        views = Int.read(data) if flags & 8 else None
        return Page(part=part, rtl=rtl, v2=v2, url=url, blocks=blocks, photos=photos, documents=documents, views=views)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.part is not None else 0
        flags |= 2 if cls.rtl is not None else 0
        flags |= 4 if cls.v2 is not None else 0
        flags |= 8 if cls.views is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.url))
        data.write(Vector().getvalue(cls.blocks))
        data.write(Vector().getvalue(cls.photos))
        data.write(Vector().getvalue(cls.documents))
        
        if cls.views is not None:
            data.write(Int.getvalue(cls.views))
        return data.getvalue()


class PollAnswer(TL):
    ID = 0x6ca9c2e9

    def __init__(cls, text: str, option: bytes):
        cls.text = text
        cls.option = option

    @staticmethod
    def read(data) -> "PollAnswer":
        text = String.read(data)
        option = Bytes.read(data)
        return PollAnswer(text=text, option=option)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.text))
        data.write(Bytes.getvalue(cls.option))
        return data.getvalue()


class Poll(TL):
    ID = 0x86e18161

    def __init__(cls, id: int, question: str, answers: List[TL], closed: bool = None, public_voters: bool = None, multiple_choice: bool = None, quiz: bool = None, close_period: int = None, close_date: int = None):
        cls.id = id
        cls.closed = closed
        cls.public_voters = public_voters
        cls.multiple_choice = multiple_choice
        cls.quiz = quiz
        cls.question = question
        cls.answers = answers
        cls.close_period = close_period
        cls.close_date = close_date

    @staticmethod
    def read(data) -> "Poll":
        id = Long.read(data)
        flags = Int.read(data)
        closed = True if flags & 1 else False
        public_voters = True if flags & 2 else False
        multiple_choice = True if flags & 4 else False
        quiz = True if flags & 8 else False
        question = String.read(data)
        answers = data.getobj()
        close_period = Int.read(data) if flags & 16 else None
        close_date = Int.read(data) if flags & 32 else None
        return Poll(id=id, closed=closed, public_voters=public_voters, multiple_choice=multiple_choice, quiz=quiz, question=question, answers=answers, close_period=close_period, close_date=close_date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.closed is not None else 0
        flags |= 2 if cls.public_voters is not None else 0
        flags |= 4 if cls.multiple_choice is not None else 0
        flags |= 8 if cls.quiz is not None else 0
        flags |= 16 if cls.close_period is not None else 0
        flags |= 32 if cls.close_date is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.id))
        data.write(String.getvalue(cls.question))
        data.write(Vector().getvalue(cls.answers))
        
        if cls.close_period is not None:
            data.write(Int.getvalue(cls.close_period))
        
        if cls.close_date is not None:
            data.write(Int.getvalue(cls.close_date))
        return data.getvalue()


class PollAnswerVoters(TL):
    ID = 0x3b6ddad2

    def __init__(cls, option: bytes, voters: int, chosen: bool = None, correct: bool = None):
        cls.chosen = chosen
        cls.correct = correct
        cls.option = option
        cls.voters = voters

    @staticmethod
    def read(data) -> "PollAnswerVoters":
        flags = Int.read(data)
        chosen = True if flags & 1 else False
        correct = True if flags & 2 else False
        option = Bytes.read(data)
        voters = Int.read(data)
        return PollAnswerVoters(chosen=chosen, correct=correct, option=option, voters=voters)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.chosen is not None else 0
        flags |= 2 if cls.correct is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Bytes.getvalue(cls.option))
        data.write(Int.getvalue(cls.voters))
        return data.getvalue()


class PollResults(TL):
    ID = 0xbadcc1a3

    def __init__(cls, min: bool = None, results: List[TL] = None, total_voters: int = None, recent_voters: List[int] = None, solution: str = None, solution_entities: List[TL] = None):
        cls.min = min
        cls.results = results
        cls.total_voters = total_voters
        cls.recent_voters = recent_voters
        cls.solution = solution
        cls.solution_entities = solution_entities

    @staticmethod
    def read(data) -> "PollResults":
        flags = Int.read(data)
        min = True if flags & 1 else False
        results = data.getobj() if flags & 2 else []
        total_voters = Int.read(data) if flags & 4 else None
        recent_voters = Int.read(data) if flags & 8 else None
        solution = String.read(data) if flags & 16 else None
        solution_entities = data.getobj() if flags & 16 else []
        return PollResults(min=min, results=results, total_voters=total_voters, recent_voters=recent_voters, solution=solution, solution_entities=solution_entities)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.min is not None else 0
        flags |= 2 if cls.results is not None else 0
        flags |= 4 if cls.total_voters is not None else 0
        flags |= 8 if cls.recent_voters is not None else 0
        flags |= 16 if cls.solution is not None else 0
        flags |= 16 if cls.solution_entities is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.results is not None:
            data.write(Vector().getvalue(cls.results))
        
        if cls.total_voters is not None:
            data.write(Int.getvalue(cls.total_voters))
        
        if cls.recent_voters is not None:
            data.write(Vector().getvalue(cls.recent_voters, Int))
        
        if cls.solution is not None:
            data.write(String.getvalue(cls.solution))
        
        if cls.solution_entities is not None:
            data.write(Vector().getvalue(cls.solution_entities))
        return data.getvalue()


class ChatOnlines(TL):
    ID = 0xf041e250

    def __init__(cls, onlines: int):
        cls.onlines = onlines

    @staticmethod
    def read(data) -> "ChatOnlines":
        onlines = Int.read(data)
        return ChatOnlines(onlines=onlines)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.onlines))
        return data.getvalue()


class StatsURL(TL):
    ID = 0x47a971e0

    def __init__(cls, url: str):
        cls.url = url

    @staticmethod
    def read(data) -> "StatsURL":
        url = String.read(data)
        return StatsURL(url=url)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        return data.getvalue()


class ChatAdminRights(TL):
    ID = 0x5fb224d5

    def __init__(cls, change_info: bool = None, post_messages: bool = None, edit_messages: bool = None, delete_messages: bool = None, ban_users: bool = None, invite_users: bool = None, pin_messages: bool = None, add_admins: bool = None, anonymous: bool = None, manage_call: bool = None, other: bool = None):
        cls.change_info = change_info
        cls.post_messages = post_messages
        cls.edit_messages = edit_messages
        cls.delete_messages = delete_messages
        cls.ban_users = ban_users
        cls.invite_users = invite_users
        cls.pin_messages = pin_messages
        cls.add_admins = add_admins
        cls.anonymous = anonymous
        cls.manage_call = manage_call
        cls.other = other

    @staticmethod
    def read(data) -> "ChatAdminRights":
        flags = Int.read(data)
        change_info = True if flags & 1 else False
        post_messages = True if flags & 2 else False
        edit_messages = True if flags & 4 else False
        delete_messages = True if flags & 8 else False
        ban_users = True if flags & 16 else False
        invite_users = True if flags & 32 else False
        pin_messages = True if flags & 128 else False
        add_admins = True if flags & 512 else False
        anonymous = True if flags & 1024 else False
        manage_call = True if flags & 2048 else False
        other = True if flags & 4096 else False
        return ChatAdminRights(change_info=change_info, post_messages=post_messages, edit_messages=edit_messages, delete_messages=delete_messages, ban_users=ban_users, invite_users=invite_users, pin_messages=pin_messages, add_admins=add_admins, anonymous=anonymous, manage_call=manage_call, other=other)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.change_info is not None else 0
        flags |= 2 if cls.post_messages is not None else 0
        flags |= 4 if cls.edit_messages is not None else 0
        flags |= 8 if cls.delete_messages is not None else 0
        flags |= 16 if cls.ban_users is not None else 0
        flags |= 32 if cls.invite_users is not None else 0
        flags |= 128 if cls.pin_messages is not None else 0
        flags |= 512 if cls.add_admins is not None else 0
        flags |= 1024 if cls.anonymous is not None else 0
        flags |= 2048 if cls.manage_call is not None else 0
        flags |= 4096 if cls.other is not None else 0
        data.write(Int.getvalue(flags))
        return data.getvalue()


class ChatBannedRights(TL):
    ID = 0x9f120418

    def __init__(cls, until_date: int, view_messages: bool = None, send_messages: bool = None, send_media: bool = None, send_stickers: bool = None, send_gifs: bool = None, send_games: bool = None, send_inline: bool = None, embed_links: bool = None, send_polls: bool = None, change_info: bool = None, invite_users: bool = None, pin_messages: bool = None):
        cls.view_messages = view_messages
        cls.send_messages = send_messages
        cls.send_media = send_media
        cls.send_stickers = send_stickers
        cls.send_gifs = send_gifs
        cls.send_games = send_games
        cls.send_inline = send_inline
        cls.embed_links = embed_links
        cls.send_polls = send_polls
        cls.change_info = change_info
        cls.invite_users = invite_users
        cls.pin_messages = pin_messages
        cls.until_date = until_date

    @staticmethod
    def read(data) -> "ChatBannedRights":
        flags = Int.read(data)
        view_messages = True if flags & 1 else False
        send_messages = True if flags & 2 else False
        send_media = True if flags & 4 else False
        send_stickers = True if flags & 8 else False
        send_gifs = True if flags & 16 else False
        send_games = True if flags & 32 else False
        send_inline = True if flags & 64 else False
        embed_links = True if flags & 128 else False
        send_polls = True if flags & 256 else False
        change_info = True if flags & 1024 else False
        invite_users = True if flags & 32768 else False
        pin_messages = True if flags & 131072 else False
        until_date = Int.read(data)
        return ChatBannedRights(view_messages=view_messages, send_messages=send_messages, send_media=send_media, send_stickers=send_stickers, send_gifs=send_gifs, send_games=send_games, send_inline=send_inline, embed_links=embed_links, send_polls=send_polls, change_info=change_info, invite_users=invite_users, pin_messages=pin_messages, until_date=until_date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.view_messages is not None else 0
        flags |= 2 if cls.send_messages is not None else 0
        flags |= 4 if cls.send_media is not None else 0
        flags |= 8 if cls.send_stickers is not None else 0
        flags |= 16 if cls.send_gifs is not None else 0
        flags |= 32 if cls.send_games is not None else 0
        flags |= 64 if cls.send_inline is not None else 0
        flags |= 128 if cls.embed_links is not None else 0
        flags |= 256 if cls.send_polls is not None else 0
        flags |= 1024 if cls.change_info is not None else 0
        flags |= 32768 if cls.invite_users is not None else 0
        flags |= 131072 if cls.pin_messages is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.until_date))
        return data.getvalue()


class InputWallPaper(TL):
    ID = 0xe630b979

    def __init__(cls, id: int, access_hash: int):
        cls.id = id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputWallPaper":
        id = Long.read(data)
        access_hash = Long.read(data)
        return InputWallPaper(id=id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class InputWallPaperSlug(TL):
    ID = 0x72091c80

    def __init__(cls, slug: str):
        cls.slug = slug

    @staticmethod
    def read(data) -> "InputWallPaperSlug":
        slug = String.read(data)
        return InputWallPaperSlug(slug=slug)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.slug))
        return data.getvalue()


class InputWallPaperNoFile(TL):
    ID = 0x8427bbac

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InputWallPaperNoFile":
        
        return InputWallPaperNoFile()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class CodeSettings(TL):
    ID = 0xdebebe83

    def __init__(cls, allow_flashcall: bool = None, current_number: bool = None, allow_app_hash: bool = None):
        cls.allow_flashcall = allow_flashcall
        cls.current_number = current_number
        cls.allow_app_hash = allow_app_hash

    @staticmethod
    def read(data) -> "CodeSettings":
        flags = Int.read(data)
        allow_flashcall = True if flags & 1 else False
        current_number = True if flags & 2 else False
        allow_app_hash = True if flags & 16 else False
        return CodeSettings(allow_flashcall=allow_flashcall, current_number=current_number, allow_app_hash=allow_app_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.allow_flashcall is not None else 0
        flags |= 2 if cls.current_number is not None else 0
        flags |= 16 if cls.allow_app_hash is not None else 0
        data.write(Int.getvalue(flags))
        return data.getvalue()


class WallPaperSettings(TL):
    ID = 0x5086cf8

    def __init__(cls, blur: bool = None, motion: bool = None, background_color: int = None, second_background_color: int = None, intensity: int = None, rotation: int = None):
        cls.blur = blur
        cls.motion = motion
        cls.background_color = background_color
        cls.second_background_color = second_background_color
        cls.intensity = intensity
        cls.rotation = rotation

    @staticmethod
    def read(data) -> "WallPaperSettings":
        flags = Int.read(data)
        blur = True if flags & 2 else False
        motion = True if flags & 4 else False
        background_color = Int.read(data) if flags & 1 else None
        second_background_color = Int.read(data) if flags & 16 else None
        intensity = Int.read(data) if flags & 8 else None
        rotation = Int.read(data) if flags & 16 else None
        return WallPaperSettings(blur=blur, motion=motion, background_color=background_color, second_background_color=second_background_color, intensity=intensity, rotation=rotation)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.blur is not None else 0
        flags |= 4 if cls.motion is not None else 0
        flags |= 1 if cls.background_color is not None else 0
        flags |= 16 if cls.second_background_color is not None else 0
        flags |= 8 if cls.intensity is not None else 0
        flags |= 16 if cls.rotation is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.background_color is not None:
            data.write(Int.getvalue(cls.background_color))
        
        if cls.second_background_color is not None:
            data.write(Int.getvalue(cls.second_background_color))
        
        if cls.intensity is not None:
            data.write(Int.getvalue(cls.intensity))
        
        if cls.rotation is not None:
            data.write(Int.getvalue(cls.rotation))
        return data.getvalue()


class AutoDownloadSettings(TL):
    ID = 0xe04232f3

    def __init__(cls, photo_size_max: int, video_size_max: int, file_size_max: int, video_upload_maxbitrate: int, disabled: bool = None, video_preload_large: bool = None, audio_preload_next: bool = None, phonecalls_less_data: bool = None):
        cls.disabled = disabled
        cls.video_preload_large = video_preload_large
        cls.audio_preload_next = audio_preload_next
        cls.phonecalls_less_data = phonecalls_less_data
        cls.photo_size_max = photo_size_max
        cls.video_size_max = video_size_max
        cls.file_size_max = file_size_max
        cls.video_upload_maxbitrate = video_upload_maxbitrate

    @staticmethod
    def read(data) -> "AutoDownloadSettings":
        flags = Int.read(data)
        disabled = True if flags & 1 else False
        video_preload_large = True if flags & 2 else False
        audio_preload_next = True if flags & 4 else False
        phonecalls_less_data = True if flags & 8 else False
        photo_size_max = Int.read(data)
        video_size_max = Int.read(data)
        file_size_max = Int.read(data)
        video_upload_maxbitrate = Int.read(data)
        return AutoDownloadSettings(disabled=disabled, video_preload_large=video_preload_large, audio_preload_next=audio_preload_next, phonecalls_less_data=phonecalls_less_data, photo_size_max=photo_size_max, video_size_max=video_size_max, file_size_max=file_size_max, video_upload_maxbitrate=video_upload_maxbitrate)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.disabled is not None else 0
        flags |= 2 if cls.video_preload_large is not None else 0
        flags |= 4 if cls.audio_preload_next is not None else 0
        flags |= 8 if cls.phonecalls_less_data is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.photo_size_max))
        data.write(Int.getvalue(cls.video_size_max))
        data.write(Int.getvalue(cls.file_size_max))
        data.write(Int.getvalue(cls.video_upload_maxbitrate))
        return data.getvalue()


class EmojiKeyword(TL):
    ID = 0xd5b3b9f9

    def __init__(cls, keyword: str, emoticons: List[str]):
        cls.keyword = keyword
        cls.emoticons = emoticons

    @staticmethod
    def read(data) -> "EmojiKeyword":
        keyword = String.read(data)
        emoticons = data.getobj(String)
        return EmojiKeyword(keyword=keyword, emoticons=emoticons)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.keyword))
        data.write(Vector().getvalue(cls.emoticons, String))
        return data.getvalue()


class EmojiKeywordDeleted(TL):
    ID = 0x236df622

    def __init__(cls, keyword: str, emoticons: List[str]):
        cls.keyword = keyword
        cls.emoticons = emoticons

    @staticmethod
    def read(data) -> "EmojiKeywordDeleted":
        keyword = String.read(data)
        emoticons = data.getobj(String)
        return EmojiKeywordDeleted(keyword=keyword, emoticons=emoticons)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.keyword))
        data.write(Vector().getvalue(cls.emoticons, String))
        return data.getvalue()


class EmojiKeywordsDifference(TL):
    ID = 0x5cc761bd

    def __init__(cls, lang_code: str, from_version: int, version: int, keywords: List[TL]):
        cls.lang_code = lang_code
        cls.from_version = from_version
        cls.version = version
        cls.keywords = keywords

    @staticmethod
    def read(data) -> "EmojiKeywordsDifference":
        lang_code = String.read(data)
        from_version = Int.read(data)
        version = Int.read(data)
        keywords = data.getobj()
        return EmojiKeywordsDifference(lang_code=lang_code, from_version=from_version, version=version, keywords=keywords)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.lang_code))
        data.write(Int.getvalue(cls.from_version))
        data.write(Int.getvalue(cls.version))
        data.write(Vector().getvalue(cls.keywords))
        return data.getvalue()


class EmojiURL(TL):
    ID = 0xa575739d

    def __init__(cls, url: str):
        cls.url = url

    @staticmethod
    def read(data) -> "EmojiURL":
        url = String.read(data)
        return EmojiURL(url=url)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        return data.getvalue()


class EmojiLanguage(TL):
    ID = 0xb3fb5361

    def __init__(cls, lang_code: str):
        cls.lang_code = lang_code

    @staticmethod
    def read(data) -> "EmojiLanguage":
        lang_code = String.read(data)
        return EmojiLanguage(lang_code=lang_code)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.lang_code))
        return data.getvalue()


class FileLocationToBeDeprecated(TL):
    ID = 0xbc7fc6cd

    def __init__(cls, volume_id: int, local_id: int):
        cls.volume_id = volume_id
        cls.local_id = local_id

    @staticmethod
    def read(data) -> "FileLocationToBeDeprecated":
        volume_id = Long.read(data)
        local_id = Int.read(data)
        return FileLocationToBeDeprecated(volume_id=volume_id, local_id=local_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.volume_id))
        data.write(Int.getvalue(cls.local_id))
        return data.getvalue()


class Folder(TL):
    ID = 0xff544e65

    def __init__(cls, id: int, title: str, autofill_new_broadcasts: bool = None, autofill_public_groups: bool = None, autofill_new_correspondents: bool = None, photo: TL = None):
        cls.autofill_new_broadcasts = autofill_new_broadcasts
        cls.autofill_public_groups = autofill_public_groups
        cls.autofill_new_correspondents = autofill_new_correspondents
        cls.id = id
        cls.title = title
        cls.photo = photo

    @staticmethod
    def read(data) -> "Folder":
        flags = Int.read(data)
        autofill_new_broadcasts = True if flags & 1 else False
        autofill_public_groups = True if flags & 2 else False
        autofill_new_correspondents = True if flags & 4 else False
        id = Int.read(data)
        title = String.read(data)
        photo = data.getobj() if flags & 8 else None
        return Folder(autofill_new_broadcasts=autofill_new_broadcasts, autofill_public_groups=autofill_public_groups, autofill_new_correspondents=autofill_new_correspondents, id=id, title=title, photo=photo)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.autofill_new_broadcasts is not None else 0
        flags |= 2 if cls.autofill_public_groups is not None else 0
        flags |= 4 if cls.autofill_new_correspondents is not None else 0
        flags |= 8 if cls.photo is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        data.write(String.getvalue(cls.title))
        
        if cls.photo is not None:
            data.write(cls.photo.getvalue())
        return data.getvalue()


class InputFolderPeer(TL):
    ID = 0xfbd2c296

    def __init__(cls, peer: TL, folder_id: int):
        cls.peer = peer
        cls.folder_id = folder_id

    @staticmethod
    def read(data) -> "InputFolderPeer":
        peer = data.getobj()
        folder_id = Int.read(data)
        return InputFolderPeer(peer=peer, folder_id=folder_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.folder_id))
        return data.getvalue()


class FolderPeer(TL):
    ID = 0xe9baa668

    def __init__(cls, peer: TL, folder_id: int):
        cls.peer = peer
        cls.folder_id = folder_id

    @staticmethod
    def read(data) -> "FolderPeer":
        peer = data.getobj()
        folder_id = Int.read(data)
        return FolderPeer(peer=peer, folder_id=folder_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.folder_id))
        return data.getvalue()


class UrlAuthResultRequest(TL):
    ID = 0x92d33a0e

    def __init__(cls, bot: TL, domain: str, request_write_access: bool = None):
        cls.request_write_access = request_write_access
        cls.bot = bot
        cls.domain = domain

    @staticmethod
    def read(data) -> "UrlAuthResultRequest":
        flags = Int.read(data)
        request_write_access = True if flags & 1 else False
        bot = data.getobj()
        domain = String.read(data)
        return UrlAuthResultRequest(request_write_access=request_write_access, bot=bot, domain=domain)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.request_write_access is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.bot.getvalue())
        data.write(String.getvalue(cls.domain))
        return data.getvalue()


class UrlAuthResultAccepted(TL):
    ID = 0x8f8c0e4e

    def __init__(cls, url: str):
        cls.url = url

    @staticmethod
    def read(data) -> "UrlAuthResultAccepted":
        url = String.read(data)
        return UrlAuthResultAccepted(url=url)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        return data.getvalue()


class UrlAuthResultDefault(TL):
    ID = 0xa9d6db1f

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "UrlAuthResultDefault":
        
        return UrlAuthResultDefault()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ChannelLocationEmpty(TL):
    ID = 0xbfb5ad8b

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "ChannelLocationEmpty":
        
        return ChannelLocationEmpty()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ChannelLocation(TL):
    ID = 0x209b82db

    def __init__(cls, geo_point: TL, address: str):
        cls.geo_point = geo_point
        cls.address = address

    @staticmethod
    def read(data) -> "ChannelLocation":
        geo_point = data.getobj()
        address = String.read(data)
        return ChannelLocation(geo_point=geo_point, address=address)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.geo_point.getvalue())
        data.write(String.getvalue(cls.address))
        return data.getvalue()


class PeerLocated(TL):
    ID = 0xca461b5d

    def __init__(cls, peer: TL, expires: int, distance: int):
        cls.peer = peer
        cls.expires = expires
        cls.distance = distance

    @staticmethod
    def read(data) -> "PeerLocated":
        peer = data.getobj()
        expires = Int.read(data)
        distance = Int.read(data)
        return PeerLocated(peer=peer, expires=expires, distance=distance)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer.getvalue())
        data.write(Int.getvalue(cls.expires))
        data.write(Int.getvalue(cls.distance))
        return data.getvalue()


class PeerSelfLocated(TL):
    ID = 0xf8ec284b

    def __init__(cls, expires: int):
        cls.expires = expires

    @staticmethod
    def read(data) -> "PeerSelfLocated":
        expires = Int.read(data)
        return PeerSelfLocated(expires=expires)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.expires))
        return data.getvalue()


class RestrictionReason(TL):
    ID = 0xd072acb4

    def __init__(cls, platform: str, reason: str, text: str):
        cls.platform = platform
        cls.reason = reason
        cls.text = text

    @staticmethod
    def read(data) -> "RestrictionReason":
        platform = String.read(data)
        reason = String.read(data)
        text = String.read(data)
        return RestrictionReason(platform=platform, reason=reason, text=text)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.platform))
        data.write(String.getvalue(cls.reason))
        data.write(String.getvalue(cls.text))
        return data.getvalue()


class InputTheme(TL):
    ID = 0x3c5693e9

    def __init__(cls, id: int, access_hash: int):
        cls.id = id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputTheme":
        id = Long.read(data)
        access_hash = Long.read(data)
        return InputTheme(id=id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class InputThemeSlug(TL):
    ID = 0xf5890df1

    def __init__(cls, slug: str):
        cls.slug = slug

    @staticmethod
    def read(data) -> "InputThemeSlug":
        slug = String.read(data)
        return InputThemeSlug(slug=slug)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.slug))
        return data.getvalue()


class Theme(TL):
    ID = 0x28f1114

    def __init__(cls, id: int, access_hash: int, slug: str, title: str, installs_count: int, creator: bool = None, default: bool = None, document: TL = None, settings: TL = None):
        cls.creator = creator
        cls.default = default
        cls.id = id
        cls.access_hash = access_hash
        cls.slug = slug
        cls.title = title
        cls.document = document
        cls.settings = settings
        cls.installs_count = installs_count

    @staticmethod
    def read(data) -> "Theme":
        flags = Int.read(data)
        creator = True if flags & 1 else False
        default = True if flags & 2 else False
        id = Long.read(data)
        access_hash = Long.read(data)
        slug = String.read(data)
        title = String.read(data)
        document = data.getobj() if flags & 4 else None
        settings = data.getobj() if flags & 8 else None
        installs_count = Int.read(data)
        return Theme(creator=creator, default=default, id=id, access_hash=access_hash, slug=slug, title=title, document=document, settings=settings, installs_count=installs_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.creator is not None else 0
        flags |= 2 if cls.default is not None else 0
        flags |= 4 if cls.document is not None else 0
        flags |= 8 if cls.settings is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(String.getvalue(cls.slug))
        data.write(String.getvalue(cls.title))
        
        if cls.document is not None:
            data.write(cls.document.getvalue())
        
        if cls.settings is not None:
            data.write(cls.settings.getvalue())
        data.write(Int.getvalue(cls.installs_count))
        return data.getvalue()


class BaseThemeClassic(TL):
    ID = 0xc3a12462

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "BaseThemeClassic":
        
        return BaseThemeClassic()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class BaseThemeDay(TL):
    ID = 0xfbd81688

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "BaseThemeDay":
        
        return BaseThemeDay()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class BaseThemeNight(TL):
    ID = 0xb7b31ea8

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "BaseThemeNight":
        
        return BaseThemeNight()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class BaseThemeTinted(TL):
    ID = 0x6d5f77ee

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "BaseThemeTinted":
        
        return BaseThemeTinted()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class BaseThemeArctic(TL):
    ID = 0x5b11125a

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "BaseThemeArctic":
        
        return BaseThemeArctic()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InputThemeSettings(TL):
    ID = 0xbd507cd1

    def __init__(cls, base_theme: TL, accent_color: int, message_top_color: int = None, message_bottom_color: int = None, wallpaper: TL = None, wallpaper_settings: TL = None):
        cls.base_theme = base_theme
        cls.accent_color = accent_color
        cls.message_top_color = message_top_color
        cls.message_bottom_color = message_bottom_color
        cls.wallpaper = wallpaper
        cls.wallpaper_settings = wallpaper_settings

    @staticmethod
    def read(data) -> "InputThemeSettings":
        flags = Int.read(data)
        base_theme = data.getobj()
        accent_color = Int.read(data)
        message_top_color = Int.read(data) if flags & 1 else None
        message_bottom_color = Int.read(data) if flags & 1 else None
        wallpaper = data.getobj() if flags & 2 else None
        wallpaper_settings = data.getobj() if flags & 2 else None
        return InputThemeSettings(base_theme=base_theme, accent_color=accent_color, message_top_color=message_top_color, message_bottom_color=message_bottom_color, wallpaper=wallpaper, wallpaper_settings=wallpaper_settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.message_top_color is not None else 0
        flags |= 1 if cls.message_bottom_color is not None else 0
        flags |= 2 if cls.wallpaper is not None else 0
        flags |= 2 if cls.wallpaper_settings is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.base_theme.getvalue())
        data.write(Int.getvalue(cls.accent_color))
        
        if cls.message_top_color is not None:
            data.write(Int.getvalue(cls.message_top_color))
        
        if cls.message_bottom_color is not None:
            data.write(Int.getvalue(cls.message_bottom_color))
        
        if cls.wallpaper is not None:
            data.write(cls.wallpaper.getvalue())
        
        if cls.wallpaper_settings is not None:
            data.write(cls.wallpaper_settings.getvalue())
        return data.getvalue()


class ThemeSettings(TL):
    ID = 0x9c14984a

    def __init__(cls, base_theme: TL, accent_color: int, message_top_color: int = None, message_bottom_color: int = None, wallpaper: TL = None):
        cls.base_theme = base_theme
        cls.accent_color = accent_color
        cls.message_top_color = message_top_color
        cls.message_bottom_color = message_bottom_color
        cls.wallpaper = wallpaper

    @staticmethod
    def read(data) -> "ThemeSettings":
        flags = Int.read(data)
        base_theme = data.getobj()
        accent_color = Int.read(data)
        message_top_color = Int.read(data) if flags & 1 else None
        message_bottom_color = Int.read(data) if flags & 1 else None
        wallpaper = data.getobj() if flags & 2 else None
        return ThemeSettings(base_theme=base_theme, accent_color=accent_color, message_top_color=message_top_color, message_bottom_color=message_bottom_color, wallpaper=wallpaper)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.message_top_color is not None else 0
        flags |= 1 if cls.message_bottom_color is not None else 0
        flags |= 2 if cls.wallpaper is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.base_theme.getvalue())
        data.write(Int.getvalue(cls.accent_color))
        
        if cls.message_top_color is not None:
            data.write(Int.getvalue(cls.message_top_color))
        
        if cls.message_bottom_color is not None:
            data.write(Int.getvalue(cls.message_bottom_color))
        
        if cls.wallpaper is not None:
            data.write(cls.wallpaper.getvalue())
        return data.getvalue()


class WebPageAttributeTheme(TL):
    ID = 0x54b56617

    def __init__(cls, documents: List[TL] = None, settings: TL = None):
        cls.documents = documents
        cls.settings = settings

    @staticmethod
    def read(data) -> "WebPageAttributeTheme":
        flags = Int.read(data)
        documents = data.getobj() if flags & 1 else []
        settings = data.getobj() if flags & 2 else None
        return WebPageAttributeTheme(documents=documents, settings=settings)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.documents is not None else 0
        flags |= 2 if cls.settings is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.documents is not None:
            data.write(Vector().getvalue(cls.documents))
        
        if cls.settings is not None:
            data.write(cls.settings.getvalue())
        return data.getvalue()


class MessageUserVote(TL):
    ID = 0xa28e5559

    def __init__(cls, user_id: int, option: bytes, date: int):
        cls.user_id = user_id
        cls.option = option
        cls.date = date

    @staticmethod
    def read(data) -> "MessageUserVote":
        user_id = Int.read(data)
        option = Bytes.read(data)
        date = Int.read(data)
        return MessageUserVote(user_id=user_id, option=option, date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Bytes.getvalue(cls.option))
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class MessageUserVoteInputOption(TL):
    ID = 0x36377430

    def __init__(cls, user_id: int, date: int):
        cls.user_id = user_id
        cls.date = date

    @staticmethod
    def read(data) -> "MessageUserVoteInputOption":
        user_id = Int.read(data)
        date = Int.read(data)
        return MessageUserVoteInputOption(user_id=user_id, date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class MessageUserVoteMultiple(TL):
    ID = 0xe8fe0de

    def __init__(cls, user_id: int, options: List[bytes], date: int):
        cls.user_id = user_id
        cls.options = options
        cls.date = date

    @staticmethod
    def read(data) -> "MessageUserVoteMultiple":
        user_id = Int.read(data)
        options = data.getobj(Bytes)
        date = Int.read(data)
        return MessageUserVoteMultiple(user_id=user_id, options=options, date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Vector().getvalue(cls.options, Bytes))
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class BankCardOpenUrl(TL):
    ID = 0xf568028a

    def __init__(cls, url: str, name: str):
        cls.url = url
        cls.name = name

    @staticmethod
    def read(data) -> "BankCardOpenUrl":
        url = String.read(data)
        name = String.read(data)
        return BankCardOpenUrl(url=url, name=name)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        data.write(String.getvalue(cls.name))
        return data.getvalue()


class DialogFilter(TL):
    ID = 0x7438f7e8

    def __init__(cls, id: int, title: str, pinned_peers: List[TL], include_peers: List[TL], exclude_peers: List[TL], contacts: bool = None, non_contacts: bool = None, groups: bool = None, broadcasts: bool = None, bots: bool = None, exclude_muted: bool = None, exclude_read: bool = None, exclude_archived: bool = None, emoticon: str = None):
        cls.contacts = contacts
        cls.non_contacts = non_contacts
        cls.groups = groups
        cls.broadcasts = broadcasts
        cls.bots = bots
        cls.exclude_muted = exclude_muted
        cls.exclude_read = exclude_read
        cls.exclude_archived = exclude_archived
        cls.id = id
        cls.title = title
        cls.emoticon = emoticon
        cls.pinned_peers = pinned_peers
        cls.include_peers = include_peers
        cls.exclude_peers = exclude_peers

    @staticmethod
    def read(data) -> "DialogFilter":
        flags = Int.read(data)
        contacts = True if flags & 1 else False
        non_contacts = True if flags & 2 else False
        groups = True if flags & 4 else False
        broadcasts = True if flags & 8 else False
        bots = True if flags & 16 else False
        exclude_muted = True if flags & 2048 else False
        exclude_read = True if flags & 4096 else False
        exclude_archived = True if flags & 8192 else False
        id = Int.read(data)
        title = String.read(data)
        emoticon = String.read(data) if flags & 33554432 else None
        pinned_peers = data.getobj()
        include_peers = data.getobj()
        exclude_peers = data.getobj()
        return DialogFilter(contacts=contacts, non_contacts=non_contacts, groups=groups, broadcasts=broadcasts, bots=bots, exclude_muted=exclude_muted, exclude_read=exclude_read, exclude_archived=exclude_archived, id=id, title=title, emoticon=emoticon, pinned_peers=pinned_peers, include_peers=include_peers, exclude_peers=exclude_peers)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.contacts is not None else 0
        flags |= 2 if cls.non_contacts is not None else 0
        flags |= 4 if cls.groups is not None else 0
        flags |= 8 if cls.broadcasts is not None else 0
        flags |= 16 if cls.bots is not None else 0
        flags |= 2048 if cls.exclude_muted is not None else 0
        flags |= 4096 if cls.exclude_read is not None else 0
        flags |= 8192 if cls.exclude_archived is not None else 0
        flags |= 33554432 if cls.emoticon is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.id))
        data.write(String.getvalue(cls.title))
        
        if cls.emoticon is not None:
            data.write(String.getvalue(cls.emoticon))
        data.write(Vector().getvalue(cls.pinned_peers))
        data.write(Vector().getvalue(cls.include_peers))
        data.write(Vector().getvalue(cls.exclude_peers))
        return data.getvalue()


class DialogFilterSuggested(TL):
    ID = 0x77744d4a

    def __init__(cls, filter: TL, description: str):
        cls.filter = filter
        cls.description = description

    @staticmethod
    def read(data) -> "DialogFilterSuggested":
        filter = data.getobj()
        description = String.read(data)
        return DialogFilterSuggested(filter=filter, description=description)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.filter.getvalue())
        data.write(String.getvalue(cls.description))
        return data.getvalue()


class StatsDateRangeDays(TL):
    ID = 0xb637edaf

    def __init__(cls, min_date: int, max_date: int):
        cls.min_date = min_date
        cls.max_date = max_date

    @staticmethod
    def read(data) -> "StatsDateRangeDays":
        min_date = Int.read(data)
        max_date = Int.read(data)
        return StatsDateRangeDays(min_date=min_date, max_date=max_date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.min_date))
        data.write(Int.getvalue(cls.max_date))
        return data.getvalue()


class StatsAbsValueAndPrev(TL):
    ID = 0xcb43acde

    def __init__(cls, current: float, previous: float):
        cls.current = current
        cls.previous = previous

    @staticmethod
    def read(data) -> "StatsAbsValueAndPrev":
        current = Double.read(data)
        previous = Double.read(data)
        return StatsAbsValueAndPrev(current=current, previous=previous)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Double.getvalue(cls.current))
        data.write(Double.getvalue(cls.previous))
        return data.getvalue()


class StatsPercentValue(TL):
    ID = 0xcbce2fe0

    def __init__(cls, part: float, total: float):
        cls.part = part
        cls.total = total

    @staticmethod
    def read(data) -> "StatsPercentValue":
        part = Double.read(data)
        total = Double.read(data)
        return StatsPercentValue(part=part, total=total)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Double.getvalue(cls.part))
        data.write(Double.getvalue(cls.total))
        return data.getvalue()


class StatsGraphAsync(TL):
    ID = 0x4a27eb2d

    def __init__(cls, token: str):
        cls.token = token

    @staticmethod
    def read(data) -> "StatsGraphAsync":
        token = String.read(data)
        return StatsGraphAsync(token=token)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.token))
        return data.getvalue()


class StatsGraphError(TL):
    ID = 0xbedc9822

    def __init__(cls, error: str):
        cls.error = error

    @staticmethod
    def read(data) -> "StatsGraphError":
        error = String.read(data)
        return StatsGraphError(error=error)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.error))
        return data.getvalue()


class StatsGraph(TL):
    ID = 0x8ea464b6

    def __init__(cls, json: TL, zoom_token: str = None):
        cls.json = json
        cls.zoom_token = zoom_token

    @staticmethod
    def read(data) -> "StatsGraph":
        flags = Int.read(data)
        json = data.getobj()
        zoom_token = String.read(data) if flags & 1 else None
        return StatsGraph(json=json, zoom_token=zoom_token)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.zoom_token is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.json.getvalue())
        
        if cls.zoom_token is not None:
            data.write(String.getvalue(cls.zoom_token))
        return data.getvalue()


class MessageInteractionCounters(TL):
    ID = 0xad4fc9bd

    def __init__(cls, msg_id: int, views: int, forwards: int):
        cls.msg_id = msg_id
        cls.views = views
        cls.forwards = forwards

    @staticmethod
    def read(data) -> "MessageInteractionCounters":
        msg_id = Int.read(data)
        views = Int.read(data)
        forwards = Int.read(data)
        return MessageInteractionCounters(msg_id=msg_id, views=views, forwards=forwards)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.msg_id))
        data.write(Int.getvalue(cls.views))
        data.write(Int.getvalue(cls.forwards))
        return data.getvalue()


class VideoSize(TL):
    ID = 0xe831c556

    def __init__(cls, type: str, location: TL, w: int, h: int, size: int, video_start_ts: float = None):
        cls.type = type
        cls.location = location
        cls.w = w
        cls.h = h
        cls.size = size
        cls.video_start_ts = video_start_ts

    @staticmethod
    def read(data) -> "VideoSize":
        flags = Int.read(data)
        type = String.read(data)
        location = data.getobj()
        w = Int.read(data)
        h = Int.read(data)
        size = Int.read(data)
        video_start_ts = Double.read(data) if flags & 1 else None
        return VideoSize(type=type, location=location, w=w, h=h, size=size, video_start_ts=video_start_ts)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.video_start_ts is not None else 0
        data.write(Int.getvalue(flags))
        data.write(String.getvalue(cls.type))
        data.write(cls.location.getvalue())
        data.write(Int.getvalue(cls.w))
        data.write(Int.getvalue(cls.h))
        data.write(Int.getvalue(cls.size))
        
        if cls.video_start_ts is not None:
            data.write(Double.getvalue(cls.video_start_ts))
        return data.getvalue()


class StatsGroupTopPoster(TL):
    ID = 0x18f3d0f7

    def __init__(cls, user_id: int, messages: int, avg_chars: int):
        cls.user_id = user_id
        cls.messages = messages
        cls.avg_chars = avg_chars

    @staticmethod
    def read(data) -> "StatsGroupTopPoster":
        user_id = Int.read(data)
        messages = Int.read(data)
        avg_chars = Int.read(data)
        return StatsGroupTopPoster(user_id=user_id, messages=messages, avg_chars=avg_chars)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Int.getvalue(cls.messages))
        data.write(Int.getvalue(cls.avg_chars))
        return data.getvalue()


class StatsGroupTopAdmin(TL):
    ID = 0x6014f412

    def __init__(cls, user_id: int, deleted: int, kicked: int, banned: int):
        cls.user_id = user_id
        cls.deleted = deleted
        cls.kicked = kicked
        cls.banned = banned

    @staticmethod
    def read(data) -> "StatsGroupTopAdmin":
        user_id = Int.read(data)
        deleted = Int.read(data)
        kicked = Int.read(data)
        banned = Int.read(data)
        return StatsGroupTopAdmin(user_id=user_id, deleted=deleted, kicked=kicked, banned=banned)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Int.getvalue(cls.deleted))
        data.write(Int.getvalue(cls.kicked))
        data.write(Int.getvalue(cls.banned))
        return data.getvalue()


class StatsGroupTopInviter(TL):
    ID = 0x31962a4c

    def __init__(cls, user_id: int, invitations: int):
        cls.user_id = user_id
        cls.invitations = invitations

    @staticmethod
    def read(data) -> "StatsGroupTopInviter":
        user_id = Int.read(data)
        invitations = Int.read(data)
        return StatsGroupTopInviter(user_id=user_id, invitations=invitations)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Int.getvalue(cls.invitations))
        return data.getvalue()


class GlobalPrivacySettings(TL):
    ID = 0xbea2f424

    def __init__(cls, archive_and_mute_new_noncontact_peers: bool = None):
        cls.archive_and_mute_new_noncontact_peers = archive_and_mute_new_noncontact_peers

    @staticmethod
    def read(data) -> "GlobalPrivacySettings":
        flags = Int.read(data)
        archive_and_mute_new_noncontact_peers = Bool.read(data) if flags & 1 else None
        return GlobalPrivacySettings(archive_and_mute_new_noncontact_peers=archive_and_mute_new_noncontact_peers)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.archive_and_mute_new_noncontact_peers is not None else 0
        data.write(Int.getvalue(flags))
        return data.getvalue()


class MessageViews(TL):
    ID = 0x455b853d

    def __init__(cls, views: int = None, forwards: int = None, replies: TL = None):
        cls.views = views
        cls.forwards = forwards
        cls.replies = replies

    @staticmethod
    def read(data) -> "MessageViews":
        flags = Int.read(data)
        views = Int.read(data) if flags & 1 else None
        forwards = Int.read(data) if flags & 2 else None
        replies = data.getobj() if flags & 4 else None
        return MessageViews(views=views, forwards=forwards, replies=replies)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.views is not None else 0
        flags |= 2 if cls.forwards is not None else 0
        flags |= 4 if cls.replies is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.views is not None:
            data.write(Int.getvalue(cls.views))
        
        if cls.forwards is not None:
            data.write(Int.getvalue(cls.forwards))
        
        if cls.replies is not None:
            data.write(cls.replies.getvalue())
        return data.getvalue()


class MessageReplyHeader(TL):
    ID = 0xa6d57763

    def __init__(cls, reply_to_msg_id: int, reply_to_peer_id: TL = None, reply_to_top_id: int = None):
        cls.reply_to_msg_id = reply_to_msg_id
        cls.reply_to_peer_id = reply_to_peer_id
        cls.reply_to_top_id = reply_to_top_id

    @staticmethod
    def read(data) -> "MessageReplyHeader":
        flags = Int.read(data)
        reply_to_msg_id = Int.read(data)
        reply_to_peer_id = data.getobj() if flags & 1 else None
        reply_to_top_id = Int.read(data) if flags & 2 else None
        return MessageReplyHeader(reply_to_msg_id=reply_to_msg_id, reply_to_peer_id=reply_to_peer_id, reply_to_top_id=reply_to_top_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.reply_to_peer_id is not None else 0
        flags |= 2 if cls.reply_to_top_id is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.reply_to_msg_id))
        
        if cls.reply_to_peer_id is not None:
            data.write(cls.reply_to_peer_id.getvalue())
        
        if cls.reply_to_top_id is not None:
            data.write(Int.getvalue(cls.reply_to_top_id))
        return data.getvalue()


class MessageReplies(TL):
    ID = 0x4128faac

    def __init__(cls, replies: int, replies_pts: int, comments: bool = None, recent_repliers: List[TL] = None, channel_id: int = None, max_id: int = None, read_max_id: int = None):
        cls.comments = comments
        cls.replies = replies
        cls.replies_pts = replies_pts
        cls.recent_repliers = recent_repliers
        cls.channel_id = channel_id
        cls.max_id = max_id
        cls.read_max_id = read_max_id

    @staticmethod
    def read(data) -> "MessageReplies":
        flags = Int.read(data)
        comments = True if flags & 1 else False
        replies = Int.read(data)
        replies_pts = Int.read(data)
        recent_repliers = data.getobj() if flags & 2 else []
        channel_id = Int.read(data) if flags & 1 else None
        max_id = Int.read(data) if flags & 4 else None
        read_max_id = Int.read(data) if flags & 8 else None
        return MessageReplies(comments=comments, replies=replies, replies_pts=replies_pts, recent_repliers=recent_repliers, channel_id=channel_id, max_id=max_id, read_max_id=read_max_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.comments is not None else 0
        flags |= 2 if cls.recent_repliers is not None else 0
        flags |= 1 if cls.channel_id is not None else 0
        flags |= 4 if cls.max_id is not None else 0
        flags |= 8 if cls.read_max_id is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.replies))
        data.write(Int.getvalue(cls.replies_pts))
        
        if cls.recent_repliers is not None:
            data.write(Vector().getvalue(cls.recent_repliers))
        
        if cls.channel_id is not None:
            data.write(Int.getvalue(cls.channel_id))
        
        if cls.max_id is not None:
            data.write(Int.getvalue(cls.max_id))
        
        if cls.read_max_id is not None:
            data.write(Int.getvalue(cls.read_max_id))
        return data.getvalue()


class PeerBlocked(TL):
    ID = 0xe8fd8014

    def __init__(cls, peer_id: TL, date: int):
        cls.peer_id = peer_id
        cls.date = date

    @staticmethod
    def read(data) -> "PeerBlocked":
        peer_id = data.getobj()
        date = Int.read(data)
        return PeerBlocked(peer_id=peer_id, date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.peer_id.getvalue())
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class GroupCallDiscarded(TL):
    ID = 0x7780bcb4

    def __init__(cls, id: int, access_hash: int, duration: int):
        cls.id = id
        cls.access_hash = access_hash
        cls.duration = duration

    @staticmethod
    def read(data) -> "GroupCallDiscarded":
        id = Long.read(data)
        access_hash = Long.read(data)
        duration = Int.read(data)
        return GroupCallDiscarded(id=id, access_hash=access_hash, duration=duration)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Int.getvalue(cls.duration))
        return data.getvalue()


class GroupCall(TL):
    ID = 0x55903081

    def __init__(cls, id: int, access_hash: int, participants_count: int, version: int, join_muted: bool = None, can_change_join_muted: bool = None, params: TL = None):
        cls.join_muted = join_muted
        cls.can_change_join_muted = can_change_join_muted
        cls.id = id
        cls.access_hash = access_hash
        cls.participants_count = participants_count
        cls.params = params
        cls.version = version

    @staticmethod
    def read(data) -> "GroupCall":
        flags = Int.read(data)
        join_muted = True if flags & 2 else False
        can_change_join_muted = True if flags & 4 else False
        id = Long.read(data)
        access_hash = Long.read(data)
        participants_count = Int.read(data)
        params = data.getobj() if flags & 1 else None
        version = Int.read(data)
        return GroupCall(join_muted=join_muted, can_change_join_muted=can_change_join_muted, id=id, access_hash=access_hash, participants_count=participants_count, params=params, version=version)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.join_muted is not None else 0
        flags |= 4 if cls.can_change_join_muted is not None else 0
        flags |= 1 if cls.params is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        data.write(Int.getvalue(cls.participants_count))
        
        if cls.params is not None:
            data.write(cls.params.getvalue())
        data.write(Int.getvalue(cls.version))
        return data.getvalue()


class InputGroupCall(TL):
    ID = 0xd8aa840f

    def __init__(cls, id: int, access_hash: int):
        cls.id = id
        cls.access_hash = access_hash

    @staticmethod
    def read(data) -> "InputGroupCall":
        id = Long.read(data)
        access_hash = Long.read(data)
        return InputGroupCall(id=id, access_hash=access_hash)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.id))
        data.write(Long.getvalue(cls.access_hash))
        return data.getvalue()


class GroupCallParticipant(TL):
    ID = 0x64c62a15

    def __init__(cls, user_id: int, date: int, source: int, muted: bool = None, left: bool = None, can_self_unmute: bool = None, just_joined: bool = None, versioned: bool = None, min: bool = None, muted_by_you: bool = None, volume_by_admin: bool = None, active_date: int = None, volume: int = None):
        cls.muted = muted
        cls.left = left
        cls.can_self_unmute = can_self_unmute
        cls.just_joined = just_joined
        cls.versioned = versioned
        cls.min = min
        cls.muted_by_you = muted_by_you
        cls.volume_by_admin = volume_by_admin
        cls.user_id = user_id
        cls.date = date
        cls.active_date = active_date
        cls.source = source
        cls.volume = volume

    @staticmethod
    def read(data) -> "GroupCallParticipant":
        flags = Int.read(data)
        muted = True if flags & 1 else False
        left = True if flags & 2 else False
        can_self_unmute = True if flags & 4 else False
        just_joined = True if flags & 16 else False
        versioned = True if flags & 32 else False
        min = True if flags & 256 else False
        muted_by_you = True if flags & 512 else False
        volume_by_admin = True if flags & 1024 else False
        user_id = Int.read(data)
        date = Int.read(data)
        active_date = Int.read(data) if flags & 8 else None
        source = Int.read(data)
        volume = Int.read(data) if flags & 128 else None
        return GroupCallParticipant(muted=muted, left=left, can_self_unmute=can_self_unmute, just_joined=just_joined, versioned=versioned, min=min, muted_by_you=muted_by_you, volume_by_admin=volume_by_admin, user_id=user_id, date=date, active_date=active_date, source=source, volume=volume)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.muted is not None else 0
        flags |= 2 if cls.left is not None else 0
        flags |= 4 if cls.can_self_unmute is not None else 0
        flags |= 16 if cls.just_joined is not None else 0
        flags |= 32 if cls.versioned is not None else 0
        flags |= 256 if cls.min is not None else 0
        flags |= 512 if cls.muted_by_you is not None else 0
        flags |= 1024 if cls.volume_by_admin is not None else 0
        flags |= 8 if cls.active_date is not None else 0
        flags |= 128 if cls.volume is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.user_id))
        data.write(Int.getvalue(cls.date))
        
        if cls.active_date is not None:
            data.write(Int.getvalue(cls.active_date))
        data.write(Int.getvalue(cls.source))
        
        if cls.volume is not None:
            data.write(Int.getvalue(cls.volume))
        return data.getvalue()


class InlineQueryPeerTypeSameBotPM(TL):
    ID = 0x3081ed9d

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InlineQueryPeerTypeSameBotPM":
        
        return InlineQueryPeerTypeSameBotPM()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InlineQueryPeerTypePM(TL):
    ID = 0x833c0fac

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InlineQueryPeerTypePM":
        
        return InlineQueryPeerTypePM()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InlineQueryPeerTypeChat(TL):
    ID = 0xd766c50a

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InlineQueryPeerTypeChat":
        
        return InlineQueryPeerTypeChat()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InlineQueryPeerTypeMegagroup(TL):
    ID = 0x5ec4be43

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InlineQueryPeerTypeMegagroup":
        
        return InlineQueryPeerTypeMegagroup()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class InlineQueryPeerTypeBroadcast(TL):
    ID = 0x6334ee9a

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "InlineQueryPeerTypeBroadcast":
        
        return InlineQueryPeerTypeBroadcast()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ChatInviteImporter(TL):
    ID = 0x1e3e6680

    def __init__(cls, user_id: int, date: int):
        cls.user_id = user_id
        cls.date = date

    @staticmethod
    def read(data) -> "ChatInviteImporter":
        user_id = Int.read(data)
        date = Int.read(data)
        return ChatInviteImporter(user_id=user_id, date=date)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.user_id))
        data.write(Int.getvalue(cls.date))
        return data.getvalue()


class ChatAdminWithInvites(TL):
    ID = 0xdfd2330f

    def __init__(cls, admin_id: int, invites_count: int, revoked_invites_count: int):
        cls.admin_id = admin_id
        cls.invites_count = invites_count
        cls.revoked_invites_count = revoked_invites_count

    @staticmethod
    def read(data) -> "ChatAdminWithInvites":
        admin_id = Int.read(data)
        invites_count = Int.read(data)
        revoked_invites_count = Int.read(data)
        return ChatAdminWithInvites(admin_id=admin_id, invites_count=invites_count, revoked_invites_count=revoked_invites_count)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.admin_id))
        data.write(Int.getvalue(cls.invites_count))
        data.write(Int.getvalue(cls.revoked_invites_count))
        return data.getvalue()
