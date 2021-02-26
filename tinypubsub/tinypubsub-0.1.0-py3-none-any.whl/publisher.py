from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar

from .subscription import Subscription

Message = TypeVar("Message")


class Publisher(ABC, Generic[Message]):
    @abstractmethod
    def publish(self, message: Message) -> None:
        ...

    @abstractmethod
    def subscribe(self, subscriber: Callable[[Message], None]) -> Subscription:
        ...

    @abstractmethod
    def unsubscribe(self, subscription: Subscription) -> None:
        ...

    @abstractmethod
    def unsubscribe_all(self) -> None:
        ...
