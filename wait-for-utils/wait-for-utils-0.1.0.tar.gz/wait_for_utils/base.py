"""base."""
import abc
import time

from wait_for_utils.config import _BaseConfig


class BaseReady(abc.ABC):
    """Base abstract class."""

    start_time = time.time()

    @abc.abstractmethod
    def is_ready(self, config: _BaseConfig) -> bool:
        ...
