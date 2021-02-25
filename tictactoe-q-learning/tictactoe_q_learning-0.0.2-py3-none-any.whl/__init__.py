import numpy as np
from typing import List, Optional
from tictactoe.board import Board
from tictactoe.player import Player


class TicTacToe:
    def __init__(self, player1: Player, player2: Player, board: Board = Board()):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.reset_players()

    def reset_players(self):
        self.current_player = self.player1
        self.waiting_player = self.player2

    def play(self, print_board: bool = True):
        self.reset_players()
        self.board.reset()
        if print_board:
            self.print_board()

    def print_board(self):
        self.board.print(
            symbol1=self.player1.symbol,
            symbol2=self.player2.symbol,
            void_symbol=' '
        )

    def available_positions(self) -> List[int]:
        actions = np.where(self.state == 0)[0].tolist()
        return actions

    @property
    def state(self) -> np.ndarray:
        return self.board.state

    def toggle_player(self):
        self.current_player, self.waiting_player = self.waiting_player, self.current_player

    def position_to_row_column(self, position: int):
        row = int(np.ceil((position + 1) / 3)) - 1
        column = position % 3
        return row, column

    def is_empty_position(self, position: int) -> bool:
        return self.state[position] == 0

    def make_play(self, position: int) -> bool:
        assert self.is_empty_position(position)
        row, column = self.position_to_row_column(position)
        player = self.current_player
        self.board.set_value(row, column, player.value)
        end = self.is_end()
        if end:
            self.reset_players()
        else:
            self.toggle_player()
        return end

    def is_end(self) -> bool:
        return self.is_win() or np.sum(self.state != 0) == 9

    def is_win(self) -> bool:
        return self.winner() is not None

    def winner(self) -> Optional[Player]:
        win = self.board.winner()
        if win == 0:
            return None
        elif win == 1:
            return self.player1
        elif win == -1:
            return self.player2
        else:
            return None

    def loser(self) -> Optional[Player]:
        winner = self.winner()
        if winner is None:
            return None
        if winner == self.player1:
            return self.player2
        else:
            return self.player1
