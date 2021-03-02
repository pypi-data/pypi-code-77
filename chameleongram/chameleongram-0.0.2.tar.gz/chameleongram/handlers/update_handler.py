from typing import Callable

from .basic_handler import Handler


class UpdateHandler(Handler):
    def __init__(self, callback: Callable, filters=None):
        super().__init__(callback, filters)
