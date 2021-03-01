from .pipe import Pipe


class NATSPipe(Pipe):
    def __init__(self, name, **kwargs):
        self._http_handler = kwargs.get('handler', None)

        Pipe.__init__(self, name, **kwargs)

    def __str__(self):
        return f'[NATSPipe name={self.name}]'