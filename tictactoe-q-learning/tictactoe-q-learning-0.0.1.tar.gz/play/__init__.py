import os
from abc import ABC, abstractmethod


class Play(ABC):
    @staticmethod
    def clear():
        os.system('cls')

    @abstractmethod
    def __call__(self): pass
