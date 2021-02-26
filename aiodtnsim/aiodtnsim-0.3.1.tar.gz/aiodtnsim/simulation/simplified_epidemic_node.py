# encoding: utf-8

"""Module providing a Node that uses a minimal variant of Epidemic Routing."""

import random
import asyncio

from .opportunistic_node import OpportunisticNode


class SimplifiedEpidemicNode(OpportunisticNode):
    """A Node using a simplified variant of Epidemic Routing.

    Compared to Epidemic Routing, this approach does NOT exchange message
    vectors. It just sends random messages from the buffer, regardless of any
    other parameters.

    Args:
        eid: A unique identifier for the node.
        buffer_size: The amount of data (in bits) the node's buffer can hold.
        event_dispatcher: An EventDispatcher for monitoring the simulation.
        link_factory: A callable returning a ``Link`` instance for the given
            parameters. If not provided, ``Link`` will be used.
        drop_strategy: The dropping behavior if a new message is received.

    """

    async def get_messages(self, rx_node):
        """Asynchronously yield messages to be transmitted."""
        while True:
            while self.buf:
                message = random.choice(self.buf)
                if message.deadline < asyncio.get_running_loop().time():
                    self.buf.remove(message)
                    continue
                yield message, None
            await self.wait_until_new_message_scheduled()
