from abc import ABC, abstractmethod

class Model(ABC):

    def __init__(self, model, **kwargs):
        self.model = model

    @abstractmethod
    def fit(self, **kwargs):
        pass

    @abstractmethod
    def predict(self, X):
        pass

    @abstractmethod
    def save(self, path):
        pass