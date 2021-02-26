# encoding: utf-8

"""Module providing a Node that simulates ONE Epidemic Routing."""

import random

from .opportunistic_node import DropStrategy, OpportunisticNode


class ONEEpidemicNode(OpportunisticNode):
    """A Node using a variant of Epidemic Routing as implemented in ONE.

    Compared to Epidemic Routing, this approach does NOT exchange message
    vectors. It first delivers messages for which the next node is the
    destination. Secondly, random messages are sent, but only if the
    destination does not have them which is checked without delay.

    Args:
        eid: A unique identifier for the node.
        buffer_size: The amount of data (in bits) the node's buffer can hold.
        event_dispatcher: An EventDispatcher for monitoring the simulation.
        link_factory: A callable returning a ``Link`` instance for the given
            parameters. If not provided, ``Link`` will be used.

    """

    def __init__(self, eid, buffer_size, event_dispatcher, **kwargs):
        super().__init__(
            eid,
            buffer_size,
            event_dispatcher,
            drop_strategy=DropStrategy.FIFO,  # first-received first
            **kwargs
        )
        self.delivered = set()

    async def get_messages(self, rx_node):
        """Asynchronously yield messages to be transmitted."""
        in_flight = None
        while True:
            population = (
                self.buf.messages -
                rx_node.buf.messages -
                rx_node.delivered
            )
            message = None
            for candidate in random.sample(population, len(population)):
                if candidate is in_flight:
                    continue
                if message is None:
                    # assume first msg neigh does not have if no candidate
                    # continue to search for "deliverable"
                    message = candidate
                if rx_node.eid == candidate.destination:
                    # if there is a "deliverable" msg, use it directly
                    message = candidate
                    break
            # if nothing found, wait until a new msg arrives
            if message is None:
                in_flight = None
                await self.wait_until_new_message_scheduled()
                continue
            in_flight = message
            yield message, None

    def route(self, message, tx_node, metadata):
        """Schedule the provided message for reception at the next hop."""
        if self.eid == message.destination:
            self.delivered.add(message)
        super().route(message, tx_node, metadata)
