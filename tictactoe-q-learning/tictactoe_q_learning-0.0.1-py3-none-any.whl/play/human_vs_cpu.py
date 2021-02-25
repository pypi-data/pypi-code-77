from play import Play
from tictactoe.board import Board
from tictactoe.game import TicTacToe
from tictactoe.player import Symbol
from tictactoe.player.human_player import HumanPlayer
from tictactoe.player.learner_player import LearnerPlayer


class HumanVsCPUPlay(Play):
    def __str__(self) -> str:
        return 'Humano vs CPU'

    def __call__(self):
        policy = input('Digite o nome da CPU adversária: ')
        human_player = HumanPlayer(Symbol.x, 'Human')
        learner_player = LearnerPlayer(Symbol.o, policy, greed_rate=0)
        board = Board()
        tictactoe = TicTacToe(human_player, learner_player, board)

        while True:
            self.clear()
            tictactoe.play()
            for turn in range(9):
                if turn % 2 == 0:
                    print()
                    position = human_player.action(
                        tictactoe.available_positions())
                else:
                    position = learner_player.action(tictactoe.state)
                is_end = tictactoe.make_play(position)
                winner = tictactoe.winner()
                self.clear()
                tictactoe.print_board()
                if is_end:
                    if winner is not None:
                        print(winner.name, 'venceu!')
                    else:
                        print('Empate!')
                    input('Pressione enter para jogar novamente...')
                    break
