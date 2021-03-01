from .app import App


class ODMApp(App):
    def __init__(self, **kwargs):
        self._storage = kwargs.get('storage', None)
