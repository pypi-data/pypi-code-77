from play import Play
from tictactoe.board import Board
from tictactoe.game import TicTacToe
from tictactoe.player import Symbol
from tictactoe.player.human_player import HumanPlayer
from tictactoe.player.learner_player import LearnerPlayer


class HumanTrainPlay(Play):
    def __str__(self) -> str:
        return 'Treinamento da CPU com humano'

    def __call__(self):
        greed_rate = float(input('Aleatoriedade da CPU: '))
        human_player = HumanPlayer(Symbol.x, 'Human')
        learner_player = LearnerPlayer(Symbol.o, 'cpu3', greed_rate=greed_rate)
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
                learner_player.add_state(tictactoe.state)
                winner = tictactoe.winner()
                self.clear()
                tictactoe.print_board()
                if is_end:
                    reward: float = 100 if winner == learner_player else - \
                        100 if winner == human_player else 0
                    learner_player.give_reward(reward)
                    learner_player.save_policy()
                    if winner is not None:
                        print(winner.name, 'venceu!')
                    else:
                        print('Empate!')
                    input('Pressione enter para jogar novamente...')
                    break
