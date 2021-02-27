from typing import Optional, Union
from exchangeratesapi.currency import Currency
from exchangeratesapi.functions import _load_history, _load_rates


class Rates:
    def __init__(self, date: Optional[str] = "latest", base: Optional[Union[str, Currency]] = Currency.EUR):
        self._state = _load_rates(date, base)

    @property
    def base(self) -> str:
        return self._state["base"]

    @property
    def date(self) -> str:
        return self._state["date"]

    @property
    def rates(self) -> dict:
        return self._state["rates"]

    def __repr__(self):
        return f'{self.__class__.__name__}(date="{self.date}", base="{self.base}")'

    def __getitem__(self, item: Union[Currency, str]) -> float:
        cur_name = item if isinstance(item, str) else item.name
        return self._state["rates"].get(cur_name, 0.0) if cur_name != self.base else 1.0


class HistoryRates:
    def __init__(self, start_at: str, end_at: str, base: Optional[Union[str, Currency]] = Currency.EUR):
        self._state = _load_history(start_at, end_at, base)

    @property
    def base(self) -> str:
        return self._state["base"]

    @property
    def start_at(self) -> str:
        return self._state["start_at"]

    @property
    def end_at(self) -> str:
        return self._state["end_at"]

    def rates(self, date: Optional[str] = None) -> dict:
        if date:
            if self.start_at <= date <= self.end_at:
                return self._state["rates"].get(date, {})
            return {}
        return self._state["rates"]

    def __repr__(self):
        return f'{self.__class__.__name__}(start_at="{self.start_at}", end_at="{self.end_at}", base="{self.base}")'

    def __getitem__(self, item: Union[Currency, str]) -> dict:
        cur_name = item if isinstance(item, str) else item.name
        default_value = 1.0 if cur_name == self.base else 0.0
        return {date: rates.get(cur_name, default_value) for date, rates in self._state["rates"].items()}


def latest():
    return _load_rates()


def history(start_at, end_at, base="EUR"):
    return _load_history(start_at, end_at, base)
