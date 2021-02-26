# encoding: utf-8

"""Module providing a Node allowing to wait until a message was scheduled."""

import asyncio

from . import SimNode


class SchedulingEventNode(SimNode):
    """A node class allowing to wait until new messages have been scheduled."""

    def __init__(self, eid, buffer_size, event_dispatcher, **kwargs):
        super().__init__(
            eid,
            buffer_size,
            event_dispatcher,
            **kwargs
        )
        self._event = asyncio.Event()

    def set_message_scheduled(self):
        """Trigger the 'message scheduled' event to unblock waiting tasks."""
        self._event.set()
        # Construct a whole new event for the next successful scheduling, so
        # new calls to wait_until_new_message_scheduled wait again.
        # NOTE: By this, we cannot easily "query" the Event status.
        self._event = asyncio.Event()

    def get_event(self):
        """Obtain a reference to the internal asyncio.Event."""
        return self._event

    async def wait_until_new_message_scheduled(self):
        """Wait until a new message has been scheduled."""
        await self._event.wait()

    def store_and_schedule(self, message, tx_node):
        """Add the provided message to the buffer and schedule it."""
        super().store_and_schedule(message, tx_node)
        # if a get_messages generator is waiting for new messages, unblock it
        self.set_message_scheduled()

    async def get_messages(self, rx_node):
        """Asynchronously yield messages to be transmitted."""
        raise NotImplementedError()
        yield  # mark function as generator -> pylint: disable=unreachable
