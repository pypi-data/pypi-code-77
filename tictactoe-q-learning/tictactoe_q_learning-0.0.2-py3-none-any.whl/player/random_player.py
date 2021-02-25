from typing import List
import numpy as np
from tictactoe.player import Player


class RandomPlayer(Player):
    def action(self, state: np.ndarray, available_positions: List[int]) -> int:
        return np.random.choice(available_positions)
