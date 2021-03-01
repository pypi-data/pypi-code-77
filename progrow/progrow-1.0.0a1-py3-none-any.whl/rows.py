from typing import List

from progrow.layout import Layout
from progrow.rendered_row import RenderedRow
from progrow.row import Row
from progrow.style import Style


class Rows:
    def __init__(self, rows: List[Row] = []) -> None:
        self.rows = rows

    def append(self, name: str, current: float, maximum: float) -> None:
        self.rows.append(Row(name=name, maximum=maximum, current=current))

    def render(self, style: Style = Style()) -> str:
        layout = Layout(self.rows)
        rendered = ""
        for row in self.rows:
            rendered += str(RenderedRow(layout, row, style)) + "\n"
        return rendered
