from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO
from .auth import SendCode, SignUp, SignIn, LogOut, ResetAuthorizations, ExportAuthorization, ImportAuthorization, BindTempAuthKey, ImportBotAuthorization, CheckPassword, RequestPasswordRecovery, RecoverPassword, ResendCode, CancelCode, DropTempAuthKeys, ExportLoginToken, ImportLoginToken, AcceptLoginToken
from .account import RegisterDevice, UnregisterDevice, UpdateNotifySettings, GetNotifySettings, ResetNotifySettings, UpdateProfile, UpdateStatus, GetWallPapers, ReportPeer, CheckUsername, UpdateUsername, GetPrivacy, SetPrivacy, DeleteAccount, GetAccountTTL, SetAccountTTL, SendChangePhoneCode, ChangePhone, UpdateDeviceLocked, GetAuthorizations, ResetAuthorization, GetPassword, GetPasswordSettings, UpdatePasswordSettings, SendConfirmPhoneCode, ConfirmPhone, GetTmpPassword, GetWebAuthorizations, ResetWebAuthorization, ResetWebAuthorizations, GetAllSecureValues, GetSecureValue, SaveSecureValue, DeleteSecureValue, GetAuthorizationForm, AcceptAuthorization, SendVerifyPhoneCode, VerifyPhone, SendVerifyEmailCode, VerifyEmail, InitTakeoutSession, FinishTakeoutSession, ConfirmPasswordEmail, ResendPasswordEmail, CancelPasswordEmail, GetContactSignUpNotification, SetContactSignUpNotification, GetNotifyExceptions, GetWallPaper, UploadWallPaper, SaveWallPaper, InstallWallPaper, ResetWallPapers, GetAutoDownloadSettings, SaveAutoDownloadSettings, UploadTheme, CreateTheme, UpdateTheme, SaveTheme, InstallTheme, GetTheme, GetThemes, SetContentSettings, GetContentSettings, GetMultiWallPapers, GetGlobalPrivacySettings, SetGlobalPrivacySettings, ReportProfilePhoto
from .users import GetUsers, GetFullUser, SetSecureValueErrors
from .contacts import GetContactIDs, GetStatuses, GetContacts, ImportContacts, DeleteContacts, DeleteByPhones, Block, Unblock, GetBlocked, Search, ResolveUsername, GetTopPeers, ResetTopPeerRating, ResetSaved, GetSaved, ToggleTopPeers, AddContact, AcceptContact, GetLocated, BlockFromReplies
from .messages import GetMessages, GetDialogs, GetHistory, Search, ReadHistory, DeleteHistory, DeleteMessages, ReceivedMessages, SetTyping, SendMessage, SendMedia, ForwardMessages, ReportSpam, GetPeerSettings, Report, GetChats, GetFullChat, EditChatTitle, EditChatPhoto, AddChatUser, DeleteChatUser, CreateChat, GetDhConfig, RequestEncryption, AcceptEncryption, DiscardEncryption, SetEncryptedTyping, ReadEncryptedHistory, SendEncrypted, SendEncryptedFile, SendEncryptedService, ReceivedQueue, ReportEncryptedSpam, ReadMessageContents, GetStickers, GetAllStickers, GetWebPagePreview, ExportChatInvite, CheckChatInvite, ImportChatInvite, GetStickerSet, InstallStickerSet, UninstallStickerSet, StartBot, GetMessagesViews, EditChatAdmin, MigrateChat, SearchGlobal, ReorderStickerSets, GetDocumentByHash, GetSavedGifs, SaveGif, GetInlineBotResults, SetInlineBotResults, SendInlineBotResult, GetMessageEditData, EditMessage, EditInlineBotMessage, GetBotCallbackAnswer, SetBotCallbackAnswer, GetPeerDialogs, SaveDraft, GetAllDrafts, GetFeaturedStickers, ReadFeaturedStickers, GetRecentStickers, SaveRecentSticker, ClearRecentStickers, GetArchivedStickers, GetMaskStickers, GetAttachedStickers, SetGameScore, SetInlineGameScore, GetGameHighScores, GetInlineGameHighScores, GetCommonChats, GetAllChats, GetWebPage, ToggleDialogPin, ReorderPinnedDialogs, GetPinnedDialogs, SetBotShippingResults, SetBotPrecheckoutResults, UploadMedia, SendScreenshotNotification, GetFavedStickers, FaveSticker, GetUnreadMentions, ReadMentions, GetRecentLocations, SendMultiMedia, UploadEncryptedFile, SearchStickerSets, GetSplitRanges, MarkDialogUnread, GetDialogUnreadMarks, ClearAllDrafts, UpdatePinnedMessage, SendVote, GetPollResults, GetOnlines, GetStatsURL, EditChatAbout, EditChatDefaultBannedRights, GetEmojiKeywords, GetEmojiKeywordsDifference, GetEmojiKeywordsLanguages, GetEmojiURL, GetSearchCounters, RequestUrlAuth, AcceptUrlAuth, HidePeerSettingsBar, GetScheduledHistory, GetScheduledMessages, SendScheduledMessages, DeleteScheduledMessages, GetPollVotes, ToggleStickerSets, GetDialogFilters, GetSuggestedDialogFilters, UpdateDialogFilter, UpdateDialogFiltersOrder, GetOldFeaturedStickers, GetReplies, GetDiscussionMessage, ReadDiscussion, UnpinAllMessages, DeleteChat, DeletePhoneCallHistory, CheckHistoryImport, InitHistoryImport, UploadImportedMedia, StartHistoryImport, GetExportedChatInvites, EditExportedChatInvite, DeleteRevokedExportedChatInvites, DeleteExportedChatInvite, GetAdminsWithInvites, GetChatInviteImporters, SetHistoryTTL
from .updates import GetState, GetDifference, GetChannelDifference
from .photos import UpdateProfilePhoto, UploadProfilePhoto, DeletePhotos, GetUserPhotos
from .upload import SaveFilePart, GetFile, SaveBigFilePart, GetWebFile, GetCdnFile, ReuploadCdnFile, GetCdnFileHashes, GetFileHashes
from .help import GetConfig, GetNearestDc, GetAppUpdate, GetInviteText, GetSupport, GetAppChangelog, SetBotUpdatesStatus, GetCdnConfig, GetRecentMeUrls, GetTermsOfServiceUpdate, AcceptTermsOfService, GetDeepLinkInfo, GetAppConfig, SaveAppLog, GetPassportConfig, GetSupportName, GetUserInfo, EditUserInfo, GetPromoData, HidePromoData, DismissSuggestion, GetCountriesList
from .channels import ReadHistory, DeleteMessages, DeleteUserHistory, ReportSpam, GetMessages, GetParticipants, GetParticipant, GetChannels, GetFullChannel, CreateChannel, EditAdmin, EditTitle, EditPhoto, CheckUsername, UpdateUsername, JoinChannel, LeaveChannel, InviteToChannel, DeleteChannel, ExportMessageLink, ToggleSignatures, GetAdminedPublicChannels, EditBanned, GetAdminLog, SetStickers, ReadMessageContents, DeleteHistory, TogglePreHistoryHidden, GetLeftChannels, GetGroupsForDiscussion, SetDiscussionGroup, EditCreator, EditLocation, ToggleSlowMode, GetInactiveChannels, ConvertToGigagroup
from .bots import SendCustomRequest, AnswerWebhookJSONQuery, SetBotCommands
from .payments import GetPaymentForm, GetPaymentReceipt, ValidateRequestedInfo, SendPaymentForm, GetSavedInfo, ClearSavedInfo, GetBankCardData
from .stickers import CreateStickerSet, RemoveStickerFromSet, ChangeStickerPosition, AddStickerToSet, SetStickerSetThumb
from .phone import GetCallConfig, RequestCall, AcceptCall, ConfirmCall, ReceivedCall, DiscardCall, SetCallRating, SaveCallDebug, SendSignalingData, CreateGroupCall, JoinGroupCall, LeaveGroupCall, EditGroupCallMember, InviteToGroupCall, DiscardGroupCall, ToggleGroupCallSettings, GetGroupCall, GetGroupParticipants, CheckGroupCall
from .langpack import GetLangPack, GetStrings, GetDifference, GetLanguages, GetLanguage
from .folders import EditPeerFolders, DeleteFolder
from .stats import GetBroadcastStats, LoadAsyncGraph, GetMegagroupStats, GetMessagePublicForwards, GetMessageStats

class InvokeAfterMsg(TL):
    ID = 0xcb9f372d

    def __init__(cls, msg_id: int, query: TL):
        cls.msg_id = msg_id
        cls.query = query

    @staticmethod
    def read(data) -> "InvokeAfterMsg":
        msg_id = Long.read(data)
        query = data.getobj()
        return InvokeAfterMsg(msg_id=msg_id, query=query)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.msg_id))
        data.write(cls.query.getvalue())
        return data.getvalue()


class InvokeAfterMsgs(TL):
    ID = 0x3dc4b4f0

    def __init__(cls, msg_ids: List[int], query: TL):
        cls.msg_ids = msg_ids
        cls.query = query

    @staticmethod
    def read(data) -> "InvokeAfterMsgs":
        msg_ids = data.getobj(Long)
        query = data.getobj()
        return InvokeAfterMsgs(msg_ids=msg_ids, query=query)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.msg_ids, Long))
        data.write(cls.query.getvalue())
        return data.getvalue()


class InitConnection(TL):
    ID = 0xc1cd5ea9

    def __init__(cls, api_id: int, device_model: str, system_version: str, app_version: str, system_lang_code: str, lang_pack: str, lang_code: str, query: TL, proxy: TL = None, params: TL = None):
        cls.api_id = api_id
        cls.device_model = device_model
        cls.system_version = system_version
        cls.app_version = app_version
        cls.system_lang_code = system_lang_code
        cls.lang_pack = lang_pack
        cls.lang_code = lang_code
        cls.proxy = proxy
        cls.params = params
        cls.query = query

    @staticmethod
    def read(data) -> "InitConnection":
        flags = Int.read(data)
        api_id = Int.read(data)
        device_model = String.read(data)
        system_version = String.read(data)
        app_version = String.read(data)
        system_lang_code = String.read(data)
        lang_pack = String.read(data)
        lang_code = String.read(data)
        proxy = data.getobj() if flags & 1 else None
        params = data.getobj() if flags & 2 else None
        query = data.getobj()
        return InitConnection(api_id=api_id, device_model=device_model, system_version=system_version, app_version=app_version, system_lang_code=system_lang_code, lang_pack=lang_pack, lang_code=lang_code, proxy=proxy, params=params, query=query)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.proxy is not None else 0
        flags |= 2 if cls.params is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.api_id))
        data.write(String.getvalue(cls.device_model))
        data.write(String.getvalue(cls.system_version))
        data.write(String.getvalue(cls.app_version))
        data.write(String.getvalue(cls.system_lang_code))
        data.write(String.getvalue(cls.lang_pack))
        data.write(String.getvalue(cls.lang_code))
        
        if cls.proxy is not None:
            data.write(cls.proxy.getvalue())
        
        if cls.params is not None:
            data.write(cls.params.getvalue())
        data.write(cls.query.getvalue())
        return data.getvalue()


class InvokeWithLayer(TL):
    ID = 0xda9b0d0d

    def __init__(cls, layer: int, query: TL):
        cls.layer = layer
        cls.query = query

    @staticmethod
    def read(data) -> "InvokeWithLayer":
        layer = Int.read(data)
        query = data.getobj()
        return InvokeWithLayer(layer=layer, query=query)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.layer))
        data.write(cls.query.getvalue())
        return data.getvalue()


class InvokeWithoutUpdates(TL):
    ID = 0xbf9459b7

    def __init__(cls, query: TL):
        cls.query = query

    @staticmethod
    def read(data) -> "InvokeWithoutUpdates":
        query = data.getobj()
        return InvokeWithoutUpdates(query=query)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.query.getvalue())
        return data.getvalue()


class InvokeWithMessagesRange(TL):
    ID = 0x365275f2

    def __init__(cls, range: TL, query: TL):
        cls.range = range
        cls.query = query

    @staticmethod
    def read(data) -> "InvokeWithMessagesRange":
        range = data.getobj()
        query = data.getobj()
        return InvokeWithMessagesRange(range=range, query=query)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.range.getvalue())
        data.write(cls.query.getvalue())
        return data.getvalue()


class InvokeWithTakeout(TL):
    ID = 0xaca9fd2e

    def __init__(cls, takeout_id: int, query: TL):
        cls.takeout_id = takeout_id
        cls.query = query

    @staticmethod
    def read(data) -> "InvokeWithTakeout":
        takeout_id = Long.read(data)
        query = data.getobj()
        return InvokeWithTakeout(takeout_id=takeout_id, query=query)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.takeout_id))
        data.write(cls.query.getvalue())
        return data.getvalue()
