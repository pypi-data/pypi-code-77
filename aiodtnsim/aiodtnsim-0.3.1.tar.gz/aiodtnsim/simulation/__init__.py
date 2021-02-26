# encoding: utf-8

"""A Node implementation for simulating routing algorithms."""

from typing import (
    Any,
    Optional,
    Callable,
    Set,
    List,
    AsyncGenerator,
    Tuple,
)

import asyncio
import collections.abc
import dataclasses
import heapq

from .. import BaseNode, Contact, Message
from ..timeutil import duration_until, sleep_until


# Helpers for typing
LinkFactory = Callable[[Contact], "Link"]
MessageGenerator = AsyncGenerator[Tuple[Message, Any], None]


class SimNode(BaseNode):
    """Base class representing a simulated node.

    For own routing algorithms, at least the ``get_messages`` asynchronous
    generator has to be implemented.

    Args:
        eid: A unique identifier for the node.
        buffer_size: The amount of data (in bits) the node's buffer can hold.
        event_dispatcher: An EventDispatcher for monitoring the simulation.
        link_factory: A callable returning a ``Link`` instance for the given
            parameters. If not provided, ``Link`` will be used.

    """

    def __init__(self, eid: str, buffer_size: float, event_dispatcher: Any,
                 link_factory: Optional[LinkFactory] = None, **kwargs) -> None:
        super().__init__(eid, event_dispatcher, **kwargs)
        self.eid = eid
        self.buf = Buffer(buffer_size)
        self.event_dispatcher = event_dispatcher
        self.link_factory: LinkFactory = link_factory or Link

    async def schedule_contact(self, contact: Contact) -> None:
        """Schedule the provided contact for execution.

        This coroutine terminates after the link has been deestablished.

        """
        assert self is contact.tx_node
        link = self.link_factory(contact)
        await sleep_until(contact.start_time)
        self.event_dispatcher.contact_started(contact)
        try:
            await asyncio.wait_for(
                self._message_transmission(link, contact),
                timeout=duration_until(contact.end_time),
            )
        except asyncio.TimeoutError:
            pass
        else:
            await sleep_until(contact.end_time)
        self.event_dispatcher.contact_ended(contact)

    async def _message_transmission(self, link: "Link",
                                    contact: Contact) -> None:
        await link.establish()
        try:
            await link.transmit_messages(self.get_messages(contact.rx_node))
        finally:
            await link.teardown()

    async def schedule_injection(self, message: Message) -> None:
        """Schedule the provided message for injection into the network.

        This coroutine terminates after the message has been routed.

        """
        await sleep_until(message.start_time)
        self.event_dispatcher.message_injected(self, message)
        self.route(message, None, None)

    async def schedule_reception(self, message: Message, tx_node: BaseNode,
                                 delay: float, metadata: Any) -> None:
        """Schedule the provided message for reception at the next hop.

        This coroutine terminates after the message has been routed.

        """
        await asyncio.sleep(delay)
        self.event_dispatcher.message_received(self, message, tx_node)
        self.route(message, tx_node, metadata)

    def route(self, message: Message, tx_node: Optional[BaseNode],
              metadata: Any) -> None:
        """Evaluate how a given message should be forwarded further.

        After obtaining a routing and/or dropping decision, the message should
        be stored in the local buffer, if possible and applicable.

        Args:
            message: The message to be routed.
            tx_node: The transmitting Node, or None if the message has been
                injected locally.
            metadata: A parameter forwarded from the result of get_messages().

        """
        # If we receive the message after the deadline, it became useless...
        if message.deadline < asyncio.get_running_loop().time():
            self.event_dispatcher.message_dropped(self, message)
            return
        # By default messages are only buffered if they will be sent further.
        if message.destination == self.eid:
            self.event_dispatcher.message_delivered(self, message)
            return
        # If the message is too big or we have it already, reject it.
        if message.size > self.buf.size or self.buf.contains(message):
            self.reject_message(message, tx_node, metadata)
            return
        # Check what we can drop, and drop it.
        self.drop_messages(message, tx_node)
        # If the message still cannot fit in the buffer, reject it.
        if message.size > self.buf.free:
            self.reject_message(message, tx_node, metadata)
            return
        # Else, store and schedule the message.
        self.store_and_schedule(message, tx_node)

    def drop_messages(self, incoming_message: Message,
                      tx_node: Optional[BaseNode]) -> None:
        """Drop messages from buffer to make space for a new message.

        This function checks the local buffer for messages which should be
        dropped after the reception or injection of another message.

        Args:
            incoming_message: The message leading to the invocation.
            tx_node: The transmitting Node, or None if the message has been
                injected locally.

        """
        time = asyncio.get_running_loop().time()
        # Drop expired messages (w.r.t. their deadline).
        while True:
            candidate = self.buf.peek_edf()
            if not candidate or candidate.deadline >= time:
                break
            self.buf.pop_edf()
            self.event_dispatcher.message_dropped(self, candidate)

    def reject_message(self, message: Message, tx_node: Optional[BaseNode],
                       metadata: Any) -> None:
        """Reject the specified message, e.g. because the buffer is exhausted.

        Args:
            message: The message to be rejected.
            tx_node: The transmitting Node, or None if the message has been
                injected locally.
            metadata: A parameter forwarded from the result of get_messages().

        """
        self.event_dispatcher.message_rejected(self, message)

    def store_and_schedule(self, message: Message,
                           tx_node: Optional[BaseNode]) -> None:
        """Add the provided message to the buffer and schedule it.

        After a positive routing decision has been obtained (in ``route``),
        this method stores the message in the local buffer and schedules it
        for further forwarding.

        Args:
            message: The message to be stored.
            tx_node: The transmitting Node, or None if the message has been
                injected locally.

        """
        self.buf.add(message)
        self.event_dispatcher.message_scheduled(self, message)

    async def get_messages(self, rx_node: BaseNode) -> MessageGenerator:
        """Asynchronously yield messages to be transmitted.

        The created generator object asynchronously yields all messages to be
        transmitted to the provided node. It should be noted that it is
        possible and expected for this function to wait until new messages
        have been received. Multiple contacts may occur concurrently and lead
        to situations where messages are received during the contact over which
        they should be sent further. This method may consider the current
        simulation time as provided by the running event loop.
        If the communication channel closes, a GeneratorExit exception is
        thrown into the async generator.

        Args:
            rx_node: The next hop for the messages yielded by the generator.

        """
        raise NotImplementedError()
        yield  # mark function as generator -> pylint: disable=unreachable

    def __repr__(self) -> str:
        """Get a string representation of the class instance."""
        return f"<Node eid='{self.eid}'>"


@dataclasses.dataclass(eq=False)
class Link:
    """Represents a unidirectional link between two nodes.

    By default, this class provides a simulated link which does not
    transmit any data. The transmission time is calculated using the specified
    bit rate and delay.

    Args:
        contact: The factual contact for which the link is established.

    """

    contact: Contact

    async def establish(self) -> None:
        """Establish the connection.

        This coroutine is called at the start of the underlying contact.
        By default, a virtual link is used which does not need to be
        established first.

        """

    async def transmit_messages(self, generator: MessageGenerator) -> None:
        """Transmit the messages yielded by the provided generator.

        All messages the asyncronous generator yields are transmitted in
        order. It is expected that this coroutine is cancelled when the link
        is torn down.

        Args:
            generator: An asynchronous generator object yielding messages to
                be transmitted over the link.

        """
        contact = self.contact
        event_dispatcher = contact.tx_node.event_dispatcher
        async for message, metadata in generator:
            async with contact.tx_node.channel(contact.rx_node):
                try:
                    event_dispatcher.message_transmission_started(
                        message,
                        contact,
                    )
                    await self.transmit(message, metadata)
                except asyncio.CancelledError:
                    event_dispatcher.message_transmission_aborted(
                        message,
                        contact,
                    )
                    await generator.aclose()
                    raise
                else:
                    event_dispatcher.message_transmission_completed(
                        message,
                        contact,
                    )

    async def transmit(self, message: Message, metadata: Any) -> None:
        """Transmit the provided message over the link.

        By default, a virtual link is used which schedules a reception event
        at the next hop with the configured transmission delay after sleeping
        for the calculated transmit duration.

        """
        # If the contact does not transmit anything, block indefinitely.
        if self.contact.bit_rate <= 0:
            while True:
                await asyncio.sleep(86400)  # duration should not exceed 1 day
        tx_duration = message.size / self.contact.bit_rate
        await asyncio.sleep(tx_duration)
        # We schedule reception of the message after the specified link delay.
        asyncio.ensure_future(self.contact.rx_node.schedule_reception(
            message,
            self.contact.tx_node,
            self.contact.delay,
            metadata,
        ))

    async def teardown(self) -> None:
        """Close the connection and clean up afterwards.

        This coroutine is called at the end of the underlying contact.
        By default, a virtual link is used which does not need to be torn down.

        """


class Buffer(collections.abc.Sequence):
    """Represents a node buffer, allowing to store a specific amount of data.

    Args:
        size: The size of the buffer in bits. Defaults to -1 (unlimited).

    """

    def __init__(self, size: float = -1) -> None:
        self.messages: Set[Message] = set()
        self.messages_heap: List[Tuple[float, Message]] = []
        if size < 0:
            size = float("inf")
        self.size = self.free = size

    def contains(self, message: Message) -> bool:
        """Find out whether a given message is contained in the buffer."""
        return message in self.messages

    def add(self, message: Message) -> None:
        """Add the provided message to the buffer."""
        assert not self.contains(message)
        self.messages.add(message)
        heapq.heappush(self.messages_heap, (message.deadline, message))
        self.free -= message.size
        assert self.free >= 0.0

    def remove(self, message: Message) -> None:
        """Remove a message from the buffer."""
        self.messages.remove(message)
        self.messages_heap.remove((message.deadline, message))
        # Restore heap structure after
        heapq.heapify(self.messages_heap)
        self.free += message.size

    def peek_edf(self) -> Optional[Message]:
        """Get the message with the smallest deadline."""
        if not self.messages_heap:
            return None
        _, message = self.messages_heap[0]
        return message

    def pop_edf(self) -> Optional[Message]:
        """Remove the message with the smallest deadline."""
        if not self.messages_heap:
            return None
        _, message = heapq.heappop(self.messages_heap)
        self.messages.remove(message)
        self.free += message.size
        return message

    def __len__(self) -> int:
        """Get the amount of messages in the buffer."""
        # NOTE: This also allows statements like `if buf` to check for items.
        return len(self.messages_heap)

    def __getitem__(self, key) -> Any:
        """Get an item by its index, ordered by deadline (earliest first)."""
        return self.messages_heap[key][1]

    def __contains__(self, item: object) -> bool:
        """Find out whether a given message is contained in the buffer."""
        return item in self.messages
