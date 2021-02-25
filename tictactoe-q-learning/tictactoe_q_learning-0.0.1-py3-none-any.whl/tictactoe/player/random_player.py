from typing import List
import numpy as np
from tictactoe.player import Player


def valid_actions(state: np.ndarray) -> List[int]:
    actions = np.where(state == 0)[0].tolist()
    return actions


class RandomPlayer(Player):
    def action(self, state: np.ndarray) -> int:
        return np.random.choice(valid_actions(state))
