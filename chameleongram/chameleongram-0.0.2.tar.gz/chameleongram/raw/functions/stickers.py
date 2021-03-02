from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class CreateStickerSet(TL):
    ID = 0xf1036780

    def __init__(cls, user_id: TL, title: str, short_name: str, stickers: List[TL], masks: bool = None, animated: bool = None, thumb: TL = None):
        cls.masks = masks
        cls.animated = animated
        cls.user_id = user_id
        cls.title = title
        cls.short_name = short_name
        cls.thumb = thumb
        cls.stickers = stickers

    @staticmethod
    def read(data) -> "CreateStickerSet":
        flags = Int.read(data)
        masks = True if flags & 1 else False
        animated = True if flags & 2 else False
        user_id = data.getobj()
        title = String.read(data)
        short_name = String.read(data)
        thumb = data.getobj() if flags & 4 else None
        stickers = data.getobj()
        return CreateStickerSet(masks=masks, animated=animated, user_id=user_id, title=title, short_name=short_name, thumb=thumb, stickers=stickers)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        flags = 0
        flags |= 1 if cls.masks is not None else 0
        flags |= 2 if cls.animated is not None else 0
        flags |= 4 if cls.thumb is not None else 0
        data.write(Int.getvalue(flags))
        data.write(cls.user_id.getvalue())
        data.write(String.getvalue(cls.title))
        data.write(String.getvalue(cls.short_name))
        
        if cls.thumb is not None:
            data.write(cls.thumb.getvalue())
        data.write(Vector().getvalue(cls.stickers))
        return data.getvalue()


class RemoveStickerFromSet(TL):
    ID = 0xf7760f51

    def __init__(cls, sticker: TL):
        cls.sticker = sticker

    @staticmethod
    def read(data) -> "RemoveStickerFromSet":
        sticker = data.getobj()
        return RemoveStickerFromSet(sticker=sticker)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.sticker.getvalue())
        return data.getvalue()


class ChangeStickerPosition(TL):
    ID = 0xffb6d4ca

    def __init__(cls, sticker: TL, position: int):
        cls.sticker = sticker
        cls.position = position

    @staticmethod
    def read(data) -> "ChangeStickerPosition":
        sticker = data.getobj()
        position = Int.read(data)
        return ChangeStickerPosition(sticker=sticker, position=position)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.sticker.getvalue())
        data.write(Int.getvalue(cls.position))
        return data.getvalue()


class AddStickerToSet(TL):
    ID = 0x8653febe

    def __init__(cls, stickerset: TL, sticker: TL):
        cls.stickerset = stickerset
        cls.sticker = sticker

    @staticmethod
    def read(data) -> "AddStickerToSet":
        stickerset = data.getobj()
        sticker = data.getobj()
        return AddStickerToSet(stickerset=stickerset, sticker=sticker)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.stickerset.getvalue())
        data.write(cls.sticker.getvalue())
        return data.getvalue()


class SetStickerSetThumb(TL):
    ID = 0x9a364e30

    def __init__(cls, stickerset: TL, thumb: TL):
        cls.stickerset = stickerset
        cls.thumb = thumb

    @staticmethod
    def read(data) -> "SetStickerSetThumb":
        stickerset = data.getobj()
        thumb = data.getobj()
        return SetStickerSetThumb(stickerset=stickerset, thumb=thumb)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.stickerset.getvalue())
        data.write(cls.thumb.getvalue())
        return data.getvalue()
