from .app import App


class ODMApp(App):
    def __init__(self, pipepool, **kwargs):
        self._storage = kwargs.get('storage', None)

        App.__init__(self, pipepool)
