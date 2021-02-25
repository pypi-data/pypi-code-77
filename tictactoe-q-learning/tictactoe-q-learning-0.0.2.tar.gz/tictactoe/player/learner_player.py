import numpy as np
import pickle
from contextlib import suppress
from typing import Dict, List
from tictactoe.player import Player, Symbol


def create_state_hash(state: np.ndarray) -> str:
    return str(state)


class LearnerPlayer(Player):
    greed_rate: float
    states_hashes: List[str]
    q_values: Dict[str, float]

    def __init__(self, symbol: Symbol, name: str, randomness: float = 0.7) -> None:
        super().__init__(symbol, name)
        self.greed_rate = randomness

        self.states_hashes = []
        self.lr = 0.2
        self.decay_gamma = 0.9
        self.q_values = {}
        self.__load_policy()

    def add_state(self, state: np.ndarray):
        state_hash = create_state_hash(state)
        self.states_hashes.append(state_hash)

    def __random_action(self, state: np.ndarray, available_positions: List[int]) -> int:
        return np.random.choice(available_positions)

    def __update_q_value(self, state_hash: str, reward: float):
        q = self.q_values[state_hash]
        q += self.lr * (self.decay_gamma * reward - q)
        self.q_values[state_hash] = q

    def __feed_reward(self, reward: float):
        for state_hash in reversed(self.states_hashes):
            if self.q_values.get(state_hash) is None:
                self.q_values[state_hash] = 0
            self.__update_q_value(state_hash, reward)
        self.states_hashes = []

    def action(self, state: np.ndarray, available_positions: List[int]) -> int:
        if np.random.uniform(0, 1) <= self.greed_rate:
            action = self.__random_action(state, available_positions)
        else:
            q_max: float = 0
            first_run: bool = True
            for position in available_positions:
                next_state = state.copy()
                next_state[position] = self.value
                next_state_hash = create_state_hash(next_state)
                q = self.q_values.get(next_state_hash) or 0
                if first_run or q >= q_max:
                    first_run = False
                    q_max = q
                    action = position
        return action

    def give_reward(self, reward: float):
        self.__feed_reward(reward)

    def save_policy(self):
        with open(f"{self.name}.policy", 'wb') as f:
            pickle.dump(self.q_values, f)

    def __load_policy(self):
        with suppress(FileNotFoundError):
            with open(f"{self.name}.policy", 'rb') as f:
                self.q_values = pickle.load(f)
                print(f'Política de "{self.name}" carregada com sucesso!')
                input('Pressione Enter para continuar...')
