from typing import Callable

from ..filters import Filters


class Handler:
    def __init__(self, callback: Callable, filters: Filters = None):
        self.callback = callback
        self.filters = filters

    def __call__(self, update, client: "chameleongram.Client" = None):
        return (
            self.filters(update, client)
            if client
            else self.filters(update)
            if callable(self.filters)
            else True
        )
