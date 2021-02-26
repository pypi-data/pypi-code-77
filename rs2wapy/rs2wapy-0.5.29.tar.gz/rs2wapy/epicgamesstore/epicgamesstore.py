class EGSID:

    def __init__(self, ident: int):
        self._ident = ident

    @property
    def ident(self) -> int:
        return self._ident

    @ident.setter
    def ident(self, ident: int):
        self._ident = ident
