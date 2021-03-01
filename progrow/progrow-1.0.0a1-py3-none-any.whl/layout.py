from typing import Iterable

from progrow.row import Row


class Layout:
    def __init__(self, rows: Iterable[Row]) -> None:
        self.current_width = 0
        self.maximum_width = 0
        self.name_width = 0
        self.percent_width = 0

        for row in rows:
            self.current_width = max(self.current_width, len(row.human_current))
            self.maximum_width = max(self.maximum_width, len(row.human_maximum))
            self.name_width = max(self.name_width, len(row.name))
            self.percent_width = max(self.percent_width, len(row.human_percent))
