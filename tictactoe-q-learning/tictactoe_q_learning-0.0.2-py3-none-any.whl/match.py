import os
from contextlib import suppress
from tictactoe.player import Player
from tictactoe import TicTacToe


class Match:
    tictactoe: TicTacToe
    switch_players: bool
    number_of_matches: int
    has_clean_screen: bool
    player1: Player
    player2: Player

    def __init__(
        self,
        tictactoe: TicTacToe,
        switch_players: bool = True,
        number_of_matches: int = 0,
        has_clean_screen: bool = True,
    ) -> None:
        self.tictactoe = tictactoe
        self.switch_players = switch_players
        self.number_of_matches = number_of_matches
        self.has_clean_screen = has_clean_screen
        self.player1 = tictactoe.player1
        self.player2 = tictactoe.player2

    def __clear_screen(self):
        with suppress(Exception):
            os.system('clear')
        with suppress(Exception):
            os.system('cls')

    def __conditional_clear_screen(self):
        if self.has_clean_screen:
            self.__clear_screen()

    def __get_current_player_by_turn(self, turn: int) -> Player:
        if turn % 2 == 0:
            return self.player1
        else:
            return self.player2

    def start(self):
        match_count = 0
        while match_count <= self.number_of_matches or self.number_of_matches == 0:
            match_count += 1
            self.__conditional_clear_screen()
            self.tictactoe.play()
            for turn in range(9):
                current_player = self.__get_current_player_by_turn(turn)
                position = current_player.action(
                    self.tictactoe.state,
                    self.tictactoe.available_positions()
                )

                self.player1.on_new_action(self.tictactoe.state)
                self.player2.on_new_action(self.tictactoe.state)

                is_end = self.tictactoe.make_play(position)
                self.__conditional_clear_screen()
                self.tictactoe.print_board()

                if is_end:
                    winner = self.tictactoe.winner()
                    loser = self.tictactoe.loser()

                    if winner == None or loser == None:
                        self.player1.on_draw()
                        self.player2.on_draw()
                    else:
                        winner.on_win()
                        loser.on_lose()

                    self.player1.on_end()
                    self.player2.on_end()
                    break
