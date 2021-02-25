from abc import ABC, abstractmethod


class Action(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
