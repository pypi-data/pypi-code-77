from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class GetPaymentForm(TL):
    ID = 0x99f09745

    def __init__(cls, msg_id: int):
        cls.msg_id = msg_id

    @staticmethod
    def read(data) -> "GetPaymentForm":
        msg_id = Int.read(data)
        return GetPaymentForm(msg_id=msg_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.msg_id))
        return data.getvalue()


class GetPaymentReceipt(TL):
    ID = 0xa092a980

    def __init__(cls, msg_id: int):
        cls.msg_id = msg_id

    @staticmethod
    def read(data) -> "GetPaymentReceipt":
        msg_id = Int.read(data)
        return GetPaymentReceipt(msg_id=msg_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.msg_id))
        return data.getvalue()


class ValidateRequestedInfo(TL):
    ID = 0x770a8e74

    def __init__(cls, msg_id: int, info: TL, save: bool = None):
        cls.save = save
        cls.msg_id = msg_id
        cls.info = info

    @staticmethod
    def read(data) -> "ValidateRequestedInfo":
        flags = Int.read(data)
        save = True if flags & 1 else False
        msg_id = Int.read(data)
        info = data.getobj()
        return ValidateRequestedInfo(save=save, msg_id=msg_id, info=info)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.save is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.msg_id))
        data.write(cls.info.getvalue())
        return data.getvalue()


class SendPaymentForm(TL):
    ID = 0x2b8879b3

    def __init__(cls, msg_id: int, credentials: TL, requested_info_id: str = None, shipping_option_id: str = None):
        cls.msg_id = msg_id
        cls.requested_info_id = requested_info_id
        cls.shipping_option_id = shipping_option_id
        cls.credentials = credentials

    @staticmethod
    def read(data) -> "SendPaymentForm":
        flags = Int.read(data)
        msg_id = Int.read(data)
        requested_info_id = String.read(data) if flags & 1 else None
        shipping_option_id = String.read(data) if flags & 2 else None
        credentials = data.getobj()
        return SendPaymentForm(msg_id=msg_id, requested_info_id=requested_info_id, shipping_option_id=shipping_option_id, credentials=credentials)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.requested_info_id is not None else 0
        flags |= 2 if cls.shipping_option_id is not None else 0
        data.write(Int.getvalue(flags))
        data.write(Int.getvalue(cls.msg_id))
        
        if cls.requested_info_id is not None:
            data.write(String.getvalue(cls.requested_info_id))
        
        if cls.shipping_option_id is not None:
            data.write(String.getvalue(cls.shipping_option_id))
        data.write(cls.credentials.getvalue())
        return data.getvalue()


class GetSavedInfo(TL):
    ID = 0x227d824b

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "GetSavedInfo":
        
        return GetSavedInfo()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class ClearSavedInfo(TL):
    ID = 0xd83d70c1

    def __init__(cls, credentials: bool = None, info: bool = None):
        cls.credentials = credentials
        cls.info = info

    @staticmethod
    def read(data) -> "ClearSavedInfo":
        flags = Int.read(data)
        credentials = True if flags & 1 else False
        info = True if flags & 2 else False
        return ClearSavedInfo(credentials=credentials, info=info)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.credentials is not None else 0
        flags |= 2 if cls.info is not None else 0
        data.write(Int.getvalue(flags))
        return data.getvalue()


class GetBankCardData(TL):
    ID = 0x2e79d779

    def __init__(cls, number: str):
        cls.number = number

    @staticmethod
    def read(data) -> "GetBankCardData":
        number = String.read(data)
        return GetBankCardData(number=number)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.number))
        return data.getvalue()
