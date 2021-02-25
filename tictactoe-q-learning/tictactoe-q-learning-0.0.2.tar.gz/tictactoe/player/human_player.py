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
    def action(self, state, available_positions: List[int]) -> int:
        while True:
            position_str = input('Posição: ')
            if position_str.isnumeric():
                position = int(position_str) - 1
                if position >= 0 and position <= 8:
                    position = invert_position(position)
                    if available_positions.__contains__(position):
                        return position
            print('Posição inválida')

    def on_win(self):
        print('Você venceu')

    def on_lose(self):
        print('Você perdeu')

    def on_draw(self):
        print('Empate')

    def on_end(self):
        input('Pressione Enter para jogar novamente...')
