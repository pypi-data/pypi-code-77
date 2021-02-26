# encoding: utf-8

"""Module providing a Node that allows configurable message dropping."""

import asyncio
import enum
import random

from .scheduling_event_node import SchedulingEventNode


class DropStrategy(enum.Enum):
    """Definitions for strategies concerning message dropping."""

    EXPIRED = "drop only expired messages"
    EDF = "drop messages with earliest deadline first"
    LDF = "drop messages with latest deadline first"
    FIFO = "track and drop first-received messages first"
    RANDOM = "drop random messages"


class OpportunisticNode(SchedulingEventNode):
    """A Node behaving like ActiveRouter in ONE.

    This node drops messages by first reception time as done in the ONE.

    Args:
        eid: A unique identifier for the node.
        buffer_size: The amount of data (in bits) the node's buffer can hold.
        event_dispatcher: An EventDispatcher for monitoring the simulation.
        link_factory: A callable returning a ``Link`` instance for the given
            parameters. If not provided, ``Link`` will be used.
        drop_strategy: The dropping behavior if a new message is received.

    """

    def __init__(self, eid, buffer_size, event_dispatcher,
                 drop_strategy=DropStrategy.FIFO, **kwargs):
        super().__init__(
            eid,
            buffer_size,
            event_dispatcher,
            **kwargs
        )
        self.drop_strategy = drop_strategy
        self._reception_times = {}

    def drop_messages(self, incoming_message, tx_node):
        """Drop messages from buffer to make space for a new message."""
        # Perform configured default dropping by expiration time.
        super().drop_messages(incoming_message, tx_node)
        if self.drop_strategy is DropStrategy.EXPIRED:
            return
        # Drop further messages by reception time.
        while self.buf.free < incoming_message.size and self.buf:
            if self.drop_strategy is DropStrategy.FIFO:
                # Get the message with smallest (oldest) reception time.
                msg = min(self.buf, key=lambda m: self._reception_times[m])
            if self.drop_strategy is DropStrategy.RANDOM:
                msg = random.choice(self.buf)
            elif self.drop_strategy is DropStrategy.EDF:
                msg = self.buf[0]
            elif self.drop_strategy is DropStrategy.LDF:
                msg = self.buf[-1]
            # Drop it.
            self.buf.remove(msg)
            self.event_dispatcher.message_dropped(self, msg)

    def store_and_schedule(self, message, tx_node):
        """Add the provided message to the buffer and schedule it."""
        super().store_and_schedule(message, tx_node)
        # Update stored timestamp to latest reception time.
        if self.drop_strategy is DropStrategy.FIFO and message in self.buf:
            self._reception_times[message] = asyncio.get_running_loop().time()
