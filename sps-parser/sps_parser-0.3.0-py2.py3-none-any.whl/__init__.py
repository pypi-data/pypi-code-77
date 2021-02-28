from PIL.Image import Image

from sps_parser.models import (
    HORNY_RACES,
    DEFAULT_MAGIC_COLOR,
    DEFAULT_METADATA,
    Pixel,
    SkinSize,
    PonyRace,
    SkinMetadata,
    TailLength,
    PonyGender
)
from sps_parser.utils import get_magic_color, get_wearable


def parse_metadata(image: Image) -> SkinMetadata:
    race = PonyRace.get(image, Pixel.RACE)
    if race == PonyRace.HUMAN:
        # NO HUMANS ALLOWED, early exit
        return DEFAULT_METADATA

    size = SkinSize.get(image, Pixel.SIZE)
    tail_length = TailLength.get(image, Pixel.TAIL_LENGTH)
    gender = PonyGender.get(image, Pixel.GENDER)
    wearable = get_wearable(image)

    if race in HORNY_RACES:
        magic_color = get_magic_color(image)
    else:
        magic_color = DEFAULT_MAGIC_COLOR

    return SkinMetadata(
        size=size,
        race=race,
        tail_length=tail_length,
        gender=gender,
        wearable=wearable,
        magic_color=magic_color
    )
