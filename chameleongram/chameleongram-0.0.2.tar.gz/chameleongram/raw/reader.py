from io import BytesIO

from ._all import _all
from .tl_base import TL


class Reader(BytesIO):
    def __init__(self, data: bytes = None):
        super().__init__(data)

    def getobj(self, *args, **kwargs) -> TL:
        return _all[int.from_bytes(super().read(4), "little", signed=False)].read(
            self, *args, **kwargs
        )

    def readtg(self, *args, **kwargs):
        return self.getobj(*args, **kwargs)
