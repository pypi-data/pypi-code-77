import math
from play import Play
from tictactoe.board import Board
from tictactoe.game import TicTacToe
from tictactoe.player import Symbol
from tictactoe.player.learner_player import LearnerPlayer


class CPUTrainPlay(Play):
    def __str__(self) -> str:
        return 'Treinamento da CPU com CPU'

    def __call__(self):
        greed_rate_1 = float(input('Aleatoriedade CPU1: '))
        greed_rate_2 = float(input('Aleatoriedade CPU2: '))
        learner_player_1 = LearnerPlayer(
            Symbol.x, 'cpu1', greed_rate=greed_rate_1)
        learner_player_2 = LearnerPlayer(
            Symbol.o, 'cpu2', greed_rate=greed_rate_2)
        board = Board()
        tictactoe = TicTacToe(learner_player_1, learner_player_2, board)

        trains = int(input('Número de treinos: '))

        old_progress: int = -1
        for i in range(trains):
            tictactoe.play(print_board=False)
            for turn in range(9):
                if turn % 2 == 0:
                    position = learner_player_1.action(tictactoe.state)
                else:
                    position = learner_player_2.action(tictactoe.state)
                is_end = tictactoe.make_play(position)
                learner_player_1.add_state(tictactoe.state)
                learner_player_2.add_state(tictactoe.state)
                winner = tictactoe.winner()
                if is_end:
                    reward_2: float = 1 if winner == learner_player_2 else - \
                        1 if winner == learner_player_1 else 0
                    reward_1 = reward_2 * -1
                    learner_player_1.give_reward(reward_1)
                    learner_player_2.give_reward(reward_2)

                    if i > 0:
                        progress = math.floor((i + 1) * 100 / trains)
                        if progress > old_progress:
                            old_progress = progress
                            self.clear()
                            print(f"{progress}%")
                    break

        learner_player_1.save_policy()
        learner_player_2.save_policy()

        print('Treinamento finalizado!')
