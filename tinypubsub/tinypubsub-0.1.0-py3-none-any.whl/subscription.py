from __future__ import annotations

from types import TracebackType
from typing import Callable, ContextManager, Optional, Type


class Subscription(ContextManager["Subscription"]):
    def __init__(self, unsubscribe: Callable[[Subscription], None]) -> None:
        self._unsubscribe: Callable[[Subscription], None] = unsubscribe

    def __enter__(self) -> Subscription:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.unsubscribe()

    def unsubscribe(self) -> None:
        self._unsubscribe(self)
