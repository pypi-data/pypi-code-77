import numpy as np
from typing import List
from enum import Enum
from abc import ABC, abstractmethod
from tictactoe.styledprint import Color, stylize


class Symbol(Enum):
    x = 1
    o = -1


class Player(ABC):
    name: str
    symbol: str
    value: int

    def __init__(self, symbol: Symbol, name: str) -> None:
        self.name = name
        self.symbol = self.__stylize_symbol(symbol)
        self.value = symbol.value

    def __stylize_symbol(self, symbol: Symbol) -> str:
        if symbol == Symbol.x:
            color = Color.GREEN
        elif symbol == Symbol.o:
            color = Color.RED
        return stylize(symbol.name, color=color)

    @abstractmethod
    def action(self, state: np.ndarray, available_positions: List[int]) -> int:
        pass

    def on_new_action(self, state: np.ndarray):
        pass

    def on_win(self):
        pass

    def on_draw(self):
        pass

    def on_lose(self):
        pass

    def on_end(self):
        pass
