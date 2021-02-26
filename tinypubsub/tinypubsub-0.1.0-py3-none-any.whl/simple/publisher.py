from typing import Callable, Dict, TypeVar

from .. import Publisher, Subscription

Message = TypeVar("Message")


class SimplePublisher(Publisher[Message]):
    def __init__(self) -> None:
        self._subscribers: Dict[Subscription, Callable[[Message], None]] = {}

    def publish(self, message: Message) -> None:
        for subscriber in self._subscribers.values():
            subscriber(message)

    def subscribe(self, subscriber: Callable[[Message], None]) -> Subscription:
        subscription = Subscription(self.unsubscribe)
        self._subscribers[subscription] = subscriber
        return subscription

    def unsubscribe(self, subscription: Subscription) -> None:
        self._subscribers.pop(subscription, None)

    def unsubscribe_all(self) -> None:
        # list() is required to prevent 'dictionary changed size during iteration' error
        for subscription in list(self._subscribers.keys()):
            self.unsubscribe(subscription)
