from typing import Tuple

Color = Tuple[int, int, int]


def rgb_as_hex(color: Color) -> int:
    if len(color) > 3:
        # Strip alpha-channel
        color = color[0:3]
    return (color[0] << 16) | (color[1] << 8) | color[2]


def rgb_as_str(color: Color) -> str:
    return f"0x{rgb_as_hex(color):0.2X}"
