from enum import Enum, IntEnum
from typing import Tuple

from PIL.Image import Image

Color = Tuple[int, int, int]


def rgb_as_hex(color: Color) -> int:
    if len(color) > 3:
        # Strip alpha-channel
        color = color[0:3]
    return (color[0] << 16) | (color[1] << 8) | color[2]


def rgb_as_str(color: Color) -> str:
    return f"0x{rgb_as_hex(color):0.2X}"


class Pixel(Enum):
    RACE = (0, 0)
    TAIL_LENGTH = (1, 0)
    GENDER = (2, 0)
    SIZE = (3, 0)

    MAGIC_COLOR = (0, 1)
    WEARABLE = (1, 1)


class Parseable(IntEnum):
    @classmethod
    def get(cls, image: Image, pixel: Pixel):
        color = image.getpixel(pixel.value)
        converted = rgb_as_hex(color)
        try:
            return cls(converted)
        except ValueError:
            return cls._DEFAULT
