from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class PaymentForm(TL):
    ID = 0x3f56aea3

    def __init__(cls, bot_id: int, invoice: TL, provider_id: int, url: str, users: List[TL], can_save_credentials: bool = None, password_missing: bool = None, native_provider: str = None, native_params: TL = None, saved_info: TL = None, saved_credentials: TL = None):
        cls.can_save_credentials = can_save_credentials
        cls.password_missing = password_missing
        cls.bot_id = bot_id
        cls.invoice = invoice
        cls.provider_id = provider_id
        cls.url = url
        cls.native_provider = native_provider
        cls.native_params = native_params
        cls.saved_info = saved_info
        cls.saved_credentials = saved_credentials
        cls.users = users

    @staticmethod
    def read(data) -> "PaymentForm":
        flags = Int.read(data)
        can_save_credentials = True if flags & 4 else False
        password_missing = True if flags & 8 else False
        bot_id = Int.read(data)
        invoice = data.getobj()
        provider_id = Int.read(data)
        url = String.read(data)
        native_provider = String.read(data) if flags & 16 else None
        native_params = data.getobj() if flags & 16 else None
        saved_info = data.getobj() if flags & 1 else None
        saved_credentials = data.getobj() if flags & 2 else None
        users = data.getobj()
        return PaymentForm(can_save_credentials=can_save_credentials, password_missing=password_missing, bot_id=bot_id, invoice=invoice, provider_id=provider_id, url=url, native_provider=native_provider, native_params=native_params, saved_info=saved_info, saved_credentials=saved_credentials, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 4 if cls.can_save_credentials is not None else 0
        flags |= 8 if cls.password_missing is not None else 0
        flags |= 16 if cls.native_provider is not None else 0
        flags |= 16 if cls.native_params is not None else 0
        flags |= 1 if cls.saved_info is not None else 0
        flags |= 2 if cls.saved_credentials is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.bot_id))
        data.write(cls.invoice.getvalue())
        data.write(Int.getvalue(cls.provider_id))
        data.write(String.getvalue(cls.url))
        
        if cls.native_provider is not None:
            data.write(String.getvalue(cls.native_provider))
        
        if cls.native_params is not None:
            data.write(cls.native_params.getvalue())
        
        if cls.saved_info is not None:
            data.write(cls.saved_info.getvalue())
        
        if cls.saved_credentials is not None:
            data.write(cls.saved_credentials.getvalue())
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class ValidatedRequestedInfo(TL):
    ID = 0xd1451883

    def __init__(cls, id: str = None, shipping_options: List[TL] = None):
        cls.id = id
        cls.shipping_options = shipping_options

    @staticmethod
    def read(data) -> "ValidatedRequestedInfo":
        flags = Int.read(data)
        id = String.read(data) if flags & 1 else None
        shipping_options = data.getobj() if flags & 2 else []
        return ValidatedRequestedInfo(id=id, shipping_options=shipping_options)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.id is not None else 0
        flags |= 2 if cls.shipping_options is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.id is not None:
            data.write(String.getvalue(cls.id))
        
        if cls.shipping_options is not None:
            data.write(Vector().getvalue(cls.shipping_options))
        return data.getvalue()


class PaymentResult(TL):
    ID = 0x4e5f810d

    def __init__(cls, updates: TL):
        cls.updates = updates

    @staticmethod
    def read(data) -> "PaymentResult":
        updates = data.getobj()
        return PaymentResult(updates=updates)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.updates.getvalue())
        return data.getvalue()


class PaymentVerificationNeeded(TL):
    ID = 0xd8411139

    def __init__(cls, url: str):
        cls.url = url

    @staticmethod
    def read(data) -> "PaymentVerificationNeeded":
        url = String.read(data)
        return PaymentVerificationNeeded(url=url)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.url))
        return data.getvalue()


class PaymentReceipt(TL):
    ID = 0x500911e1

    def __init__(cls, date: int, bot_id: int, invoice: TL, provider_id: int, currency: str, total_amount: int, credentials_title: str, users: List[TL], info: TL = None, shipping: TL = None):
        cls.date = date
        cls.bot_id = bot_id
        cls.invoice = invoice
        cls.provider_id = provider_id
        cls.info = info
        cls.shipping = shipping
        cls.currency = currency
        cls.total_amount = total_amount
        cls.credentials_title = credentials_title
        cls.users = users

    @staticmethod
    def read(data) -> "PaymentReceipt":
        flags = Int.read(data)
        date = Int.read(data)
        bot_id = Int.read(data)
        invoice = data.getobj()
        provider_id = Int.read(data)
        info = data.getobj() if flags & 1 else None
        shipping = data.getobj() if flags & 2 else None
        currency = String.read(data)
        total_amount = Long.read(data)
        credentials_title = String.read(data)
        users = data.getobj()
        return PaymentReceipt(date=date, bot_id=bot_id, invoice=invoice, provider_id=provider_id, info=info, shipping=shipping, currency=currency, total_amount=total_amount, credentials_title=credentials_title, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.info is not None else 0
        flags |= 2 if cls.shipping is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.date))
        data.write(Int.getvalue(cls.bot_id))
        data.write(cls.invoice.getvalue())
        data.write(Int.getvalue(cls.provider_id))
        
        if cls.info is not None:
            data.write(cls.info.getvalue())
        
        if cls.shipping is not None:
            data.write(cls.shipping.getvalue())
        data.write(String.getvalue(cls.currency))
        data.write(Long.getvalue(cls.total_amount))
        data.write(String.getvalue(cls.credentials_title))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class SavedInfo(TL):
    ID = 0xfb8fe43c

    def __init__(cls, has_saved_credentials: bool = None, saved_info: TL = None):
        cls.has_saved_credentials = has_saved_credentials
        cls.saved_info = saved_info

    @staticmethod
    def read(data) -> "SavedInfo":
        flags = Int.read(data)
        has_saved_credentials = True if flags & 2 else False
        saved_info = data.getobj() if flags & 1 else None
        return SavedInfo(has_saved_credentials=has_saved_credentials, saved_info=saved_info)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 2 if cls.has_saved_credentials is not None else 0
        flags |= 1 if cls.saved_info is not None else 0
        data.write(Int.getvalue(flags))
        
        if cls.saved_info is not None:
            data.write(cls.saved_info.getvalue())
        return data.getvalue()


class BankCardData(TL):
    ID = 0x3e24e573

    def __init__(cls, title: str, open_urls: List[TL]):
        cls.title = title
        cls.open_urls = open_urls

    @staticmethod
    def read(data) -> "BankCardData":
        title = String.read(data)
        open_urls = data.getobj()
        return BankCardData(title=title, open_urls=open_urls)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.title))
        data.write(Vector().getvalue(cls.open_urls))
        return data.getvalue()
