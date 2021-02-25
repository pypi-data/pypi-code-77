from typing import List
from tictactoe.player import Player


def invert_position(position: int) -> int:
    assert position >= 0 and position <= 8
    if position <= 2:
        position += 6
    elif position >= 6:
        position -= 6
    return position


class HumanPlayer(Player):
    def action(self, valid_positions: List[int]) -> int:
        while True:
            position_str = input('Posição: ')
            if position_str.isnumeric():
                position = int(position_str) - 1
                if position >= 0 and position <= 8:
                    position = invert_position(position)
                    if valid_positions.__contains__(position):
                        return position
            print('Posição inválida')
