from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class SendCustomRequest(TL):
    ID = 0xaa2769ed

    def __init__(cls, custom_method: str, params: TL):
        cls.custom_method = custom_method
        cls.params = params

    @staticmethod
    def read(data) -> "SendCustomRequest":
        custom_method = String.read(data)
        params = data.getobj()
        return SendCustomRequest(custom_method=custom_method, params=params)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(String.getvalue(cls.custom_method))
        data.write(cls.params.getvalue())
        return data.getvalue()


class AnswerWebhookJSONQuery(TL):
    ID = 0xe6213f4d

    def __init__(cls, query_id: int, data: TL):
        cls.query_id = query_id
        cls.data = data

    @staticmethod
    def read(data) -> "AnswerWebhookJSONQuery":
        query_id = Long.read(data)
        data = data.getobj()
        return AnswerWebhookJSONQuery(query_id=query_id, data=data)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Long.getvalue(cls.query_id))
        data.write(cls.data.getvalue())
        return data.getvalue()


class SetBotCommands(TL):
    ID = 0x805d46f6

    def __init__(cls, commands: List[TL]):
        cls.commands = commands

    @staticmethod
    def read(data) -> "SetBotCommands":
        commands = data.getobj()
        return SetBotCommands(commands=commands)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.commands))
        return data.getvalue()
