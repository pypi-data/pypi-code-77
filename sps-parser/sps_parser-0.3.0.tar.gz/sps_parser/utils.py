from PIL.Image import Image

from sps_parser.converters import rgb_as_str
from sps_parser.models import Wearable, Pixel


def get_magic_color(image: Image) -> str:
    return rgb_as_str(image.getpixel(Pixel.MAGIC_COLOR.value))


def get_wearable(image: Image) -> Wearable:
    def _get(value: int) -> Wearable:
        try:
            return Wearable(value)
        except ValueError:
            return Wearable.NONE

    raw_values = image.getpixel(Pixel.WEARABLE.value)
    available_accessories = [_get(accessory) for accessory in raw_values if accessory is not Wearable.NONE]
    if not available_accessories:
        return Wearable.NONE

    return available_accessories[0]
