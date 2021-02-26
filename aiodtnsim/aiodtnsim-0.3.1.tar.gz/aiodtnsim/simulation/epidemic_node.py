# encoding: utf-8

"""Module providing a Node that uses Epidemic Routing."""

import asyncio
import random

from aiodtnsim import Message

from .opportunistic_node import OpportunisticNode

# Amount of seconds assumed for the TTL of the summary vector message.
VECTOR_MESSAGE_LIFETIME = 300


class SummaryVectorMessage(Message):
    """A message encapsulating Epidemic Routing summary vectors."""

    pass


class EpidemicNode(OpportunisticNode):
    """A node using Epidemic Routing.

    A gratuitous (proactive) acknowledgment mechanism is leveraged by this
    implementation to exchange the "summary vectors" at the beginning of a
    contact, i.e. inform the other node(s) which message(s) we have and only
    transmit those that the other node(s) don't have.

    Args:
        eid: A unique identifier for the node.
        buffer_size: The amount of data (in bits) the node's buffer can hold.
        event_dispatcher: An EventDispatcher for monitoring the simulation.
        link_factory: A callable returning a ``Link`` instance for the given
            parameters. If not provided, ``Link`` will be used.
        drop_strategy: The dropping behavior if a new message is received.
        vector_entry_size (int): The size of a msg. vector entry (bits).
        vector_header_size (int): The amount of bits assumed as header overhead
            included in the "summary vector" message.
        max_hops (int): The maximum number of hops (transmissions since
            creation, excluding replicas) allowed for a message.
        deliverable_first (bool): Whether to send messages addressed to the
            encountered neighbor first (may improve delays, used in ONE).
        send_once (bool): Send messages only once during a contact.

    """

    def __init__(self, eid, buffer_size, event_dispatcher,
                 vector_entry_size=32, vector_header_size=800, max_hops=6,
                 deliverable_first=True, send_once=True, **kwargs):
        super().__init__(
            eid,
            buffer_size,
            event_dispatcher,
            **kwargs
        )
        self.vector_entry_size = vector_entry_size
        self.vector_header_size = vector_header_size
        self.max_hops = max_hops
        self.deliverable_first = deliverable_first
        self.send_once = send_once
        self.last_vector = {}
        self.delivered = set()
        self._msg_remaining_hops = {}

    async def get_messages(self, rx_node):
        """Asynchronously yield messages to be transmitted."""
        if rx_node not in self.last_vector:
            self.last_vector[rx_node] = set()
        # First, send the "summary vector".
        time = asyncio.get_running_loop().time()
        vector_contents = self.buf.messages | self.delivered
        yield SummaryVectorMessage(
            start_time=time,
            source=self.eid,
            destination=rx_node.eid,
            size=(
                self.vector_entry_size * len(vector_contents) +
                self.vector_header_size
            ),
            deadline=(
                time + VECTOR_MESSAGE_LIFETIME
            ),
            data=vector_contents,
        ), None
        # Now, send the mesages not known to be available at the neighbor.
        # we run in an endless loop - even if no messages can be sent
        # anymore, we await the next reception event via the lock
        sent = set()
        while True:
            last_vector = self.last_vector[rx_node]
            if self.deliverable_first:
                population = [
                    msg for msg in self.buf.messages
                    if msg not in last_vector
                    and self._msg_remaining_hops[msg] > 1
                    and rx_node.eid != msg.destination
                    and msg not in sent
                ]
                deliverable = [
                    msg for msg in self.buf.messages
                    if msg not in last_vector
                    and rx_node.eid == msg.destination
                    and msg not in sent
                ]
            else:
                population = [
                    msg for msg in self.buf.messages
                    if msg not in last_vector
                    and (
                        self._msg_remaining_hops[msg] > 1
                        or rx_node.eid == msg.destination
                    )
                    and msg not in sent
                ]
                deliverable = []
            random.shuffle(population)
            random.shuffle(deliverable)
            # We check for the _current_ Event being set and keep a reference
            # because ScheulingEventNode replaces it upon message scheduling.
            # By that, the loop would effectively be endless if using
            # self.get_event().is_set().
            # NOTE that this allows sending messages just received from the
            # neighbor which is, however, prevented by sending only once
            # during a contact and exchanging new summary vectors at the
            # start of the next contact.
            event = self.get_event()
            while not event.is_set():
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
                # Yield the message.
                yield message, self._msg_remaining_hops[message] - 1
                # If the message was not sent out successfully, we will not
                # get here but yield will throw.
                if self.send_once:
                    sent.add(message)

    async def schedule_reception(self, message, tx_node, delay, metadata):
        """Schedule the provided message for reception at the local node."""
        if isinstance(message, SummaryVectorMessage):
            await asyncio.sleep(delay)
            self.last_vector[tx_node] = message.data
            # Trigger an update of the list of mesages to be sent or unblock
            # get_messages as the summary vector has been updated.
            self.set_message_scheduled()
        else:
            await super().schedule_reception(message, tx_node, delay, metadata)

    def route(self, message, tx_node, metadata):
        """Schedule the provided message for reception at the next hop."""
        if self.eid == message.destination:
            self.delivered.add(message)
        if tx_node:
            if (message not in self._msg_remaining_hops or
                    metadata > self._msg_remaining_hops.get(message, 1)):
                self._msg_remaining_hops[message] = metadata  # received
        else:
            self._msg_remaining_hops[message] = self.max_hops  # injected
        super().route(message, tx_node, metadata)
