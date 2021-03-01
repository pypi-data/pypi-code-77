from abc import ABC, abstractmethod

class Analyzer(ABC):

    def __init__(self, **kwargs):
        self.model = kwargs.pop('model')
        self.data = kwargs.pop('data')

    @abstractmethod
    def run(self, **kwargs):
        pass

    @abstractmethod
    def show(self, **kwargs):
        pass