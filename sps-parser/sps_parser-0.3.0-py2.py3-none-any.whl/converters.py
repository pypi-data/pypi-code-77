from typing import Tuple, Union

Color = Tuple[int, int, int]


def rgb_as_hex(color: Union[Color, int]) -> int:
    if isinstance(color, int):
        # 8-bit colormap files, broken by now
        return 0
    if len(color) > 3:
        # Strip alpha-channel
        color = color[0:3]
    return (color[0] << 16) | (color[1] << 8) | color[2]


def rgb_as_str(color: Color) -> str:
    value = rgb_as_hex(color)
    padding = 8
    return f"{value:#0{padding}x}"
