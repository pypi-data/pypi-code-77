# encoding: utf-8

"""A discrete-event simulator for delay-tolerant networks, based on asyncio."""

from typing import (
    Any,
    AsyncGenerator,
    Optional,
)

import asyncio
import contextlib
import functools
import dataclasses


@dataclasses.dataclass(frozen=True, order=True)
class Contact:
    """Represents a unidirectional factual contact.

    This directly corresponds to a time frame during which a link between
    two nodes is up, plus the associated properties.

    Args:
        tx_node: A Node instance representing the sending side of the link.
        rx_node: A Node instance representing the receiving side of the link.
        start_time: The time at which the link becomes available.
        end_time: The time at which the link will become unavailable.
        bit_rate: The transmission rate of the link, in bit/s.
        delay: The time it takes for a signal to reach the receiving node,
            in seconds.
        param: Arbitrary parameters for use by custom implementations.

    """

    tx_node: "BaseNode"
    rx_node: "BaseNode"
    start_time: float
    end_time: float
    bit_rate: float
    delay: float = 0.0
    param: Any = dataclasses.field(default=None, compare=False)


@dataclasses.dataclass(frozen=True, order=True)
class Message:
    """Represents a message, i.e. a DTN bundle.

    Args:
        start_time: The time at which the message is injected/created.
        source: The unique identifier of the source node.
        destination: The unique identifier of the destination node.
        size: The message size in bits.
        deadline: The time at which the message expires, i.e. a time after
            which forwarding of the message is not sensible anymore.
        fragment_offset: For fragmented messages, this contains the fragment
            offset in bits from the start of the original message.
        total_size: For fragmented messages, this contains the total
            length of the payload of the original message.
        data: An optional payload data field to hand over bundle contents.

    """

    start_time: float
    source: str
    destination: str = dataclasses.field(compare=False)
    size: int = dataclasses.field(compare=False)
    deadline: float = dataclasses.field(compare=False)
    fragment_offset: Optional[int] = None
    total_size: Optional[int] = None
    data: Any = dataclasses.field(default=None, compare=False, repr=False)

    @property
    def is_fragmented(self):
        """Get whether the Message is a fragment of another Message."""
        return self.fragment_offset is not None

    @property
    def original_message(self):
        """Get a Message equal to the original Message of this fragment."""
        if self.is_fragmented:
            return Message(
                start_time=self.start_time,
                source=self.source,
                destination=self.destination,
                size=self.total_size,
                deadline=self.deadline,
            )
        return self


class BaseNode:
    """Base class representing a DTN node.

    Args:
        eid: A unique identifier for the node.
        event_dispatcher: An EventDispatcher for monitoring the simulation.

    """

    def __init__(self, eid: str, event_dispatcher: Any,
                 tx_channels: Optional[int] = None,
                 rx_channels: Optional[int] = None) -> None:
        self.eid = eid
        self.event_dispatcher = event_dispatcher
        self.tx_channel_sem: Optional[asyncio.BoundedSemaphore] = (
            asyncio.BoundedSemaphore(tx_channels)
            if tx_channels else None
        )
        self.rx_channel_sem: Optional[asyncio.BoundedSemaphore] = (
            asyncio.BoundedSemaphore(rx_channels)
            if rx_channels else None
        )

    @contextlib.asynccontextmanager
    async def channel(self, rx_node: "BaseNode") -> AsyncGenerator:
        """Reserve a tx_channel at this node and an rx_channel at rx_node."""
        # This logic allows to prevent unnecessary blocking of TX/RX channels.
        # If one of them is not available, the other will not be blocked,
        # until both are available at the same time.
        while True:
            # First, wait for a TX channel, then, an RX channel.
            async with self.tx_channel(rx_node):
                # If we cannot obtain an RX channel _right now_, try it the
                # other way around (see below).
                if (rx_node.rx_channel_sem is None or
                        not rx_node.rx_channel_sem.locked()):
                    async with rx_node.rx_channel(self):
                        # Got both, allow transmissions!
                        yield
                        break
            # Try it the other way around...
            async with rx_node.rx_channel(self):
                if (self.tx_channel_sem is None or
                        not self.tx_channel_sem.locked()):
                    async with self.tx_channel(rx_node):
                        # Got both, allow transmissions!
                        yield
                        break

    @contextlib.asynccontextmanager
    async def rx_channel(self, tx_node: "BaseNode") -> AsyncGenerator:
        """Reserve a free channel to receive data."""
        if not self.rx_channel_sem:
            yield
            return
        await self.rx_channel_sem.acquire()
        try:
            yield
        finally:
            self.rx_channel_sem.release()

    @contextlib.asynccontextmanager
    async def tx_channel(self, rx_node: "BaseNode") -> AsyncGenerator:
        """Reserve a free channel to transmit data."""
        if not self.tx_channel_sem:
            yield
            return
        await self.tx_channel_sem.acquire()
        try:
            yield
        finally:
            self.tx_channel_sem.release()

    async def schedule_contact(self, contact: Contact) -> None:
        """Schedule the provided contact for execution.

        This coroutine has to terminate after the link has been deestablished.

        """
        raise NotImplementedError()

    async def schedule_injection(self, message: Message) -> None:
        """Schedule the provided message for injection into the network.

        This coroutine has to terminate after the message has been routed.

        """
        raise NotImplementedError()

    async def schedule_reception(self, message: Message, tx_node: "BaseNode",
                                 delay: float, metadata: Any) -> None:
        """Schedule the provided message for reception at the next hop.

        This coroutine has to terminate after the message has been routed.

        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        """Get a string representation of the class instance."""
        return f"<BaseNode eid='{self.eid}'>"


class EventHandler:
    """Defines the interface for classes handling simulator events."""

    def contact_started(self, time: float, contact: Contact) -> None:
        """Event triggered when a contact has started."""

    def contact_ended(self, time: float, contact: Contact) -> None:
        """Event triggered when a contact has ended."""

    def message_received(self, time: float, rx_node: BaseNode,
                         message: Message, tx_node: BaseNode) -> None:
        """Event triggered when a message has been received."""

    def message_dropped(self, time: float, node: BaseNode,
                        message: Message) -> None:
        """Event triggered when a message has been dropped from the buffer."""

    def message_rejected(self, time: float, node: BaseNode,
                         message: Message) -> None:
        """Event triggered when a message has been dropped on reception."""

    def message_delivered(self, time: float, node: BaseNode,
                          message: Message) -> None:
        """Event triggered when a message has been delivered successfully."""

    def message_deleted(self, time: float, node: BaseNode,
                        message: Message) -> None:
        """Event triggered when a message has been dropped after TX."""

    def message_injected(self, time: float, node: BaseNode,
                         message: Message) -> None:
        """Event triggered when a message has been injected/created."""

    def message_scheduled(self, time: float, node: BaseNode,
                          message: Message) -> None:
        """Event triggered when a message has been stored and scheduled."""

    def message_transmission_started(self, time: float, message: Message,
                                     contact: Contact) -> None:
        """Event triggered when a message transmission is initiated."""

    def message_transmission_completed(self, time: float, message: Message,
                                       contact: Contact) -> None:
        """Event triggered when a message transmission succeeded."""

    def message_transmission_aborted(self, time: float, message: Message,
                                     contact: Contact) -> None:
        """Event triggered when a message transfer has been aborted."""


class EventDispatcher:
    """Provides an extensible monitoring interface for the simulator."""

    def __init__(self):
        self._handlers = {
            event: []
            for event in EventHandler.__dict__ if not event.startswith("__")
        }

        def _dispatch_event(callbacks, *args, **kwargs):
            if not callbacks:
                return
            loop = asyncio.get_running_loop()
            for func in callbacks:
                func(loop.time(), *args, **kwargs)

        # This adds a method for each event to the current instance.
        for event_name, callbacks in self._handlers.items():
            setattr(self, event_name, functools.partial(
                _dispatch_event,
                callbacks,  # NOTE that callbacks is a [] reference
            ))

    def add_subscriber(self, subscriber: EventHandler, no_parent: bool = True):
        """Add an event subscriber to be notified.

        Args:
            subscriber: An EventHandler instance to be notified.
            no_parent: Do not add non-overridden methods of parent
                classes for efficiency. Defaults to True.

        """
        for event, handler_list in self._handlers.items():
            register_method = (
                (event in subscriber.__class__.__dict__) if no_parent
                else hasattr(subscriber, event)
            )
            if register_method:
                handler_list.append(getattr(subscriber, event))
