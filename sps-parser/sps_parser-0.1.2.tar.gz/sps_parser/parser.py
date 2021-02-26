from PIL.Image import Image

from sps_parser.models import *
from sps_parser.utils import rgb_as_str, Pixel


def parse_metadata(image: Image) -> SkinMetadata:
    race = PonyRace.get(image, Pixel.RACE)
    if race == PonyRace.HUMAN:
        # NO HUMANS ALLOWED, early exit
        return DEFAULT_METADATA

    size = SkinSize.get(image, Pixel.SIZE)
    tail_length = TailLength.get(image, Pixel.TAIL_LENGTH)
    gender = PonyGender.get(image, Pixel.GENDER)
    wearable = Wearable.get(image, Pixel.WEARABLE)

    if race in HORNY_RACES:
        magic_color = rgb_as_str(image.getpixel(Pixel.MAGIC_COLOR.value))
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
