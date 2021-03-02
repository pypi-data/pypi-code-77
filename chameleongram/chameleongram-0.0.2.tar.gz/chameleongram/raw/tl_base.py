from abc import abstractmethod

from chameleongram.utils import get_json


class TL:
    def __init__(self, *args, **kwargs):
        ...

    @staticmethod
    @abstractmethod
    def read(data) -> "TL":
        ...

    @abstractmethod
    def getvalue(self) -> bytes:
        ...

    __str__ = __repr__ = lambda self: get_json(self, as_string=True)
