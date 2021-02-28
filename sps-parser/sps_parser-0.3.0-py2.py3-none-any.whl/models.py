from enum import IntEnum, Enum
from typing import Optional

from PIL.Image import Image
from pydantic import BaseModel

from sps_parser.converters import rgb_as_hex

DEFAULT_MAGIC_COLOR = "0x4444aa"


class Pixel(Enum):
    RACE = (0, 0)
    TAIL_LENGTH = (1, 0)
    GENDER = (2, 0)
    SIZE = (3, 0)

    MAGIC_COLOR = (0, 1)
    WEARABLE = (1, 1)


class Parseable(IntEnum):
    _DEFAULT: int

    @classmethod
    def get(cls, image: Image, pixel: Pixel):
        color = image.getpixel(pixel.value)
        converted = rgb_as_hex(color)
        try:
            return cls(converted)
        except ValueError:
            return cls._DEFAULT


class SkinSize(Parseable):
    NORMAL = 0
    TALL = 0x534b76
    BULKY = 0xce3254
    LANKY = 0x3254ce
    YEARLING = 0x53beff
    FOAL = 0xffbe53

    _DEFAULT = NORMAL


class PonyRace(Parseable):
    HUMAN = 0
    EARTH = 0xf9b131
    PEGASUS = 0x88caf0
    UNICORN = 0xd19fe4
    ALICORN = 0xfef9fc
    CHANGELING = 0x282b29
    ZEBRA = 0xd0cccf
    REFORMED_CHANGELING = 0xcaed5a
    GRIFFIN = 0xae9145
    HIPPOGRIFF = 0xd6ddac
    KIRIN = 0xfa88af
    BATPONY = 0xeeeeee
    SEAPONY = 0x3655dd

    _DEFAULT = HUMAN


class TailLength(Parseable):
    FULL = 0
    STUB = 0x425844
    QUARTER = 0xd19fe4
    HALF = 0x534b76
    THREE_QUARTERS = 0x8a6b7f

    _DEFAULT = FULL


class PonyGender(Parseable):
    MARE = 0
    STALLION = 0xffffff
    ABOMONATION = 0x888888

    _DEFAULT = MARE


class Wearable(IntEnum):
    NONE = 0
    MUFFIN = 0x32
    HAT = 0x64
    SADDLE_BAGS = 0xc8
    STETSON = 0xfa


class SkinMetadata(BaseModel):
    size: SkinSize = SkinSize.NORMAL
    race: PonyRace = PonyRace.HUMAN
    tail_length: TailLength = TailLength.FULL
    gender: PonyGender = PonyGender.MARE
    magic_color: str = DEFAULT_MAGIC_COLOR
    wearable: Optional[Wearable] = Wearable.NONE


DEFAULT_METADATA = SkinMetadata()
# BONK
HORNY_RACES = frozenset([PonyRace.UNICORN, PonyRace.ALICORN, PonyRace.KIRIN])
