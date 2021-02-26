# encoding: utf-8

"""Module providing a ONE-like implementation of Spray and Wait Routing."""

import asyncio
import math
import random

from .opportunistic_node import DropStrategy, OpportunisticNode


class ONESprayAndWaitNode(OpportunisticNode):
    """A node class using binary Spray and Wait Routing as implemented in ONE.

    Args:
        eid: A unique identifier for the node.
        buffer_size: The amount of data (in bits) the node's buffer can hold.
        event_dispatcher: An EventDispatcher for monitoring the simulation.
        link_factory: A callable returning a ``Link`` instance for the given
            parameters. If not provided, ``Link`` will be used.
        initial_copies (int): The initial number of copies for any message.

    """

    def __init__(self, eid, buffer_size, event_dispatcher,
                 initial_copies=6, **kwargs):
        super().__init__(
            eid,
            buffer_size,
            event_dispatcher,
            drop_strategy=DropStrategy.FIFO,  # first-received first
            **kwargs
        )
        self.initial_copies = initial_copies
        self._msg_metadata = {}
        self.delivered = set()

    async def get_messages(self, rx_node):
        """Asynchronously yield messages to be transmitted."""
        in_flight = None
        while True:
            deliverable = [
                msg for msg in self.buf
                if rx_node.eid == msg.destination
                # Optimization: Do not send messages the receiver has already.
                # NOTE: This is ONE-specific and not quite realistic.
                and msg not in rx_node.buf
                and msg not in rx_node.delivered
                and msg is not in_flight
            ]
            population = [
                msg for msg in self.buf
                if self._msg_metadata[msg] > 1
                and rx_node.eid != msg.destination
                # Optimization: Do not send messages the receiver has already.
                # NOTE: This is ONE-specific and not quite realistic.
                and msg not in rx_node.buf
                and msg not in rx_node.delivered
                and msg is not in_flight
            ]
            random.shuffle(population)
            random.shuffle(deliverable)
            event = self.get_event()
            while not event.is_set():
                # Unfortunately, we cannot yield > 1 message as the population
                # may change during transmission which occurs during `yield`.
                if deliverable:
                    # First, send messages for which neighbor == receiver.
                    # This behavior has been adopted from the ONE simulator.
                    used_list = deliverable
                elif population:
                    # Second, send other messages for which we have copies.
                    used_list = population
                else:
                    # Nothing to send, wait for a new message.
                    in_flight = None
                    await self.wait_until_new_message_scheduled()
                    break
                # Send ONE message.
                message = used_list.pop()
                # It might happen that a message is removed from the buffer
                # but nothing new gets scheduled, so we don't need a new
                # population but have to check whether we still have it.
                if not self.buf.contains(message):
                    continue
                if message.deadline < asyncio.get_running_loop().time():
                    self.event_dispatcher.message_dropped(self, message)
                    self.buf.remove(message)
                    continue
                copies = self._msg_metadata[message]
                if copies <= 1:
                    if rx_node.eid != message.destination:
                        continue
                    assert rx_node.eid == message.destination
                    out_copies = 1
                    keep_copies = 1  # NOTE: ONE-specific!
                else:
                    # See the Spray and Wait paper, definition 3.2.
                    out_copies = math.floor(copies / 2)
                    keep_copies = math.ceil(copies / 2)
                # We now have given copies away
                self._msg_metadata[message] = keep_copies
                # Yield the message and transmit the copy count as metadata.
                in_flight = message
                try:
                    yield message, out_copies
                except GeneratorExit:
                    # Transmission failed, add back the failed copies.
                    self._msg_metadata[message] += out_copies
                    raise
                # If the message was not sent out successfully, we will not
                # get here but yield will throw.
                if keep_copies == 0 and message in self.buf:
                    self.event_dispatcher.message_deleted(self, message)
                    self.buf.remove(message)

    def route(self, message, tx_node, metadata):
        """Schedule the provided message for reception at the next hop."""
        if tx_node:
            # NOTE: We cannot really ensure we do not get messages we already
            # have. If a node chooses to send something to us we have to
            # increase the number of copies we have by the forwarded number
            # of copies.
            if self.eid == message.destination:
                self.delivered.add(message)
            else:
                if message not in self._msg_metadata:
                    self._msg_metadata[message] = 0
                self._msg_metadata[message] += metadata
        else:
            self._msg_metadata[message] = self.initial_copies  # injected
        super().route(message, tx_node, metadata)
