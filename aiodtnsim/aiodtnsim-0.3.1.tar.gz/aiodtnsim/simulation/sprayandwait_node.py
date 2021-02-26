# encoding: utf-8

"""Module providing an implementation of Spray and Wait Routing."""

import asyncio
import math
import random

from .opportunistic_node import OpportunisticNode


class SprayAndWaitNode(OpportunisticNode):
    """A node class using binary Spray and Wait Routing.

    Args:
        eid: A unique identifier for the node.
        buffer_size: The amount of data (in bits) the node's buffer can hold.
        event_dispatcher: An EventDispatcher for monitoring the simulation.
        link_factory: A callable returning a ``Link`` instance for the given
            parameters. If not provided, ``Link`` will be used.
        drop_strategy: The dropping behavior if a new message is received.
        initial_copies (int): The initial number of copies for any message.
        deliverable_first (bool): Whether to send messages addressed to the
            encountered neighbor first (may improve delays, used in ONE).
        send_once (bool): Send messages only once during a contact.

    """

    def __init__(self, eid, buffer_size, event_dispatcher, initial_copies=6,
                 deliverable_first=True, send_once=True, **kwargs):
        super().__init__(
            eid,
            buffer_size,
            event_dispatcher,
            **kwargs
        )
        self.initial_copies = initial_copies
        self.deliverable_first = deliverable_first
        self.send_once = send_once
        self._snw_copies = {}

    async def get_messages(self, rx_node):
        """Asynchronously yield messages to be transmitted."""
        # Keep track of what we already sent during the contact (see below!)
        sent = set()
        while True:
            if self.deliverable_first:
                population = [
                    msg for msg in self.buf.messages
                    if self._snw_copies[msg] > 1
                    and rx_node.eid != msg.destination
                    and msg not in sent
                ]
                deliverable = [
                    msg for msg in self.buf.messages
                    if rx_node.eid == msg.destination
                    and msg not in sent
                ]
            else:
                population = [
                    msg for msg in self.buf.messages
                    if (
                        self._snw_copies[msg] > 1
                        or rx_node.eid == msg.destination
                    )
                    and msg not in sent
                ]
                deliverable = []
            random.shuffle(population)
            random.shuffle(deliverable)
            # If something is received we have to determine the population
            # again, because it could have changed...
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
                copies = self._snw_copies[message]
                if copies <= 1 and rx_node.eid != message.destination:
                    continue
                if copies == 1:
                    assert rx_node.eid == message.destination
                    out_copies = 1
                    keep_copies = 0
                else:
                    # See the Spray and Wait paper, definition 3.2.
                    out_copies = math.floor(copies / 2)
                    keep_copies = math.ceil(copies / 2)
                # We now have given copies away...
                self._snw_copies[message] = keep_copies
                # Yield the message and transmit the copy count as metadata.
                try:
                    yield message, out_copies
                except GeneratorExit:
                    # Transmission failed, add back the failed copies.
                    self._snw_copies[message] += out_copies
                    raise
                if self.send_once:
                    sent.add(message)
                # If the message was not sent out successfully, we will not
                # get here but yield will throw.
                if keep_copies == 0 and message in self.buf:
                    self.event_dispatcher.message_deleted(self, message)
                    self.buf.remove(message)

    def route(self, message, tx_node, metadata):
        """Schedule the provided message for reception at the next hop."""
        # Add the incoming message to the list of outgoing ACKs
        if tx_node:
            # NOTE: We cannot really ensure we do not get messages we already
            # have. If a node chooses to send something to us we have to
            # increase the number of copies we have by the forwarded number
            # of copies.
            if message not in self._snw_copies:
                self._snw_copies[message] = 0
            self._snw_copies[message] += metadata
        else:
            self._snw_copies[message] = self.initial_copies  # injected
        super().route(message, tx_node, metadata)
