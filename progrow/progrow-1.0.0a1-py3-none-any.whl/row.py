from math import floor


class Row:
    def __init__(self, name: str, maximum: float, current: float) -> None:
        self.name = name
        self.maximum = maximum
        self.current = current

    @property
    def human_percent(self) -> str:
        return str(floor(self.percent * 100)) + "%"

    @property
    def percent(self) -> float:
        return (1.0 / self.maximum) * self.current

    @property
    def human_current(self) -> str:
        return f"{self.current:n}"

    @property
    def human_maximum(self) -> str:
        return f"{self.maximum:n}"
