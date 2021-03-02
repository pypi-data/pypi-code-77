from functools import wraps

from .basic_handler import Handler
from .update_handler import UpdateHandler
from ..filters import Filters


class Handlers:
    handlers = []

    @classmethod
    def on_update(cls, filters: Filters = None):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                await func(*args, **kwargs)

            cls.handlers.append(UpdateHandler(wrapper, filters))
            return wrapper

        return decorator
