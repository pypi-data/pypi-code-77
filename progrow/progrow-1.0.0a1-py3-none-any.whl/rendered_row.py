from functools import cached_property

import colorama

from progrow.bar import bar
from progrow.layout import Layout
from progrow.row import Row
from progrow.style import Style


class RenderedRow:
    def __init__(
        self,
        layout: Layout,
        row: Row,
        style: Style = Style(),
    ) -> None:
        colorama.init()
        self.layout = layout
        self.row = row
        self.style = style

    @cached_property
    def name(self) -> str:
        name = self.row.name[0 : self.layout.name_width]  # Trim
        name = name.ljust(self.layout.name_width)  # Pad
        return name

    @cached_property
    def bar_width(self) -> int:
        width = self.style.width
        width -= self.layout.name_width
        width -= len(self.style.name_post)

        if self.style.show_fraction:
            width -= len(self.style.pre_fraction_str)
            width -= self.layout.current_width
            width -= len(self.style.mid_fraction_str)
            width -= self.layout.maximum_width

        if self.style.show_percent:
            width -= len(self.style.pre_percent_str)
            width -= self.layout.percent_width

        return width

    @cached_property
    def filled_bar(self) -> str:
        return bar(width=self.bar_width, percent=self.row.percent)

    def __str__(self) -> str:
        s = ""

        if self.style.color:
            s += str(colorama.Fore.YELLOW)

        s += self.name

        if self.style.color:
            s += str(colorama.Fore.RESET)

        s += self.style.name_post

        if self.style.color:
            s += str(colorama.Fore.GREEN)

        s += self.filled_bar

        if self.style.color:
            s += str(colorama.Fore.RESET)

        if self.style.show_fraction:
            s += self.style.pre_fraction_str

            if self.style.color:
                s += str(colorama.Fore.LIGHTBLUE_EX)

            s += self.row.human_current.rjust(self.layout.current_width)

            if self.style.color:
                s += str(colorama.Fore.RESET)

            s += self.style.mid_fraction_str

            if self.style.color:
                s += str(colorama.Fore.LIGHTBLUE_EX)

            s += self.row.human_maximum.rjust(self.layout.maximum_width)

            if self.style.color:
                s += str(colorama.Fore.RESET)

        if self.style.show_percent:
            s += self.style.pre_percent_str

            if self.style.color:
                s += str(colorama.Fore.CYAN)

            s += self.row.human_percent.rjust(self.layout.percent_width)

            if self.style.color:
                s += str(colorama.Fore.RESET)

        return s.rstrip()
