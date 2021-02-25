import re
import textwrap
import termcolor
from typing import List
from enum import Enum


class Color(Enum):
    GREY = 'grey'
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'
    MAGENTA = 'magenta'
    CYAN = 'cyan'
    WHITE = 'white'


class Highlight(Enum):
    GREY = 'on_grey'
    RED = 'on_red'
    GREEN = 'on_green'
    YELLOW = 'on_yellow'
    BLUE = 'on_blue'
    MAGENTA = 'on_magenta'
    CYAN = 'on_cyan'
    WHITE = 'on_white'


class Attribute(Enum):
    BOLD = 'bold'
    DARK = 'dark'
    UNDERLINE = 'underline'
    BLINK = 'blink'
    REVERSE = 'reverse'
    CONCEALED = 'concealed'


def indent(text: str, color: Color = None, highlight: Highlight = None, attrs: List[Attribute] = None) -> str:
    text = textwrap.dedent(text)
    text = re.sub(r'^\n+', '', text)
    text = re.sub(r'\n+$', '', text)
    return stylize(text, color, highlight, attrs)


def styled_print(
        *args: str,
        sep=' ',
        end='\n', file=None,
        color: Color = None,
        highlight: Highlight = None,
        attrs: List[Attribute] = None):
    args_ = [stylize(arg, color=color, highlight=highlight, attrs=attrs)
             for arg in args]
    print(*args_, sep=sep, end=end, file=file)


def stylize(
        text: str,
        color: Color = None,
        highlight: Highlight = None,
        attrs: List[Attribute] = None,
) -> str:
    color_ = color.value if color is not None else None
    highlight_ = highlight.value if highlight is not None else None
    attrs_ = [attr.value for attr in attrs] if attrs is not None else None

    return termcolor.colored(
        text,
        color=color_,
        on_color=highlight_,
        attrs=attrs_
    )
