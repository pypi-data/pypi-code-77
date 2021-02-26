"""Different implementations of Link representing impaired transmission."""

import asyncio
import random
import dataclasses

from . import get_fc_volume

from .. import Link
from ..util import StartTimeBasedDict


class MessageExpired(Exception):
    """An Exception to be raised when a message expires during transmission."""

    pass


@dataclasses.dataclass(eq=False)
class IdealRedundancyImpairedCLALink(Link):
    """A Link that supports an ideal redundancy scheme for error recovery.

    This link takes the residual BER and transmits (CLA) packets of the
    given size. If a packet is lost, it is re-transmitted immediately.
    This simulates an ideal link that accounts for exactly the necessary
    amount of redundancy without any delay. In practice such redundancy may
    be introduced using either ARQ or FEC schemes, each with the associated
    advantages and drawbacks.

    """

    def __init__(self, contact, block_size):
        super().__init__(contact)
        self.block_size = block_size

    async def _try_transmit_block(self, size, deadline):
        time = asyncio.get_running_loop().time()
        assert time <= self.contact.end_time
        cur_char = self.contact.param.get_characteristics_at(time)
        # If the contact does not transmit anything, block indefinitely.
        if cur_char.bit_rate <= 0:
            while True:
                await asyncio.sleep(86400)  # duration should not exceed 1 day
        p_block_successfully_transmitted = (
            (1 - cur_char.bit_error_rate) ** size
        )
        tx_duration = size / cur_char.bit_rate
        if time + tx_duration > deadline:
            raise MessageExpired()
        await asyncio.sleep(tx_duration)
        # NOTE: We assume that if the packet had an error, this is _always_
        # recognized. The receiver will _not_ receive garbage, but a
        # re-transmission is planned by the sender
        if random.random() < p_block_successfully_transmitted:
            return size
        return 0

    async def transmit(self, message, metadata):
        """Transmit a Message via the Link."""
        # We attempt block retransmission until it succeeds
        size_remaining = message.size
        while size_remaining:
            try:
                size_remaining -= await self._try_transmit_block(
                    min(size_remaining, self.block_size),
                    message.deadline,
                )
            except MessageExpired:
                return
        # We schedule reception of the message after the specified link delay.
        time = asyncio.get_running_loop().time()
        cur_char = self.contact.param.get_characteristics_at(time)
        if time + cur_char.delay * 2 > message.deadline:
            return
        asyncio.ensure_future(self.contact.rx_node.schedule_reception(
            message,
            self.contact.tx_node,
            cur_char.delay * 2,  # one full round-trip b/c ACKs needed
            metadata,
        ))


@dataclasses.dataclass(eq=False)
class SimulatedIdealRedundancyImpairedCLALink(Link):
    """An IdealRedundancyImpairedCLALink with deterministic transmission."""

    def __init__(self, contact, block_size):
        super().__init__(contact)
        self.effective_data_rate = (
            get_fc_volume(contact.param, block_size) /
            (contact.end_time - contact.start_time)
        )
        self.delays = StartTimeBasedDict({
            char.starting_at: char.delay
            for char in contact.param.characteristics
        })
        # NOTE: Assumes the bit rate of all characteristics is the same.
        br0 = contact.param.characteristics[0].bit_rate
        for char in contact.param.characteristics[1:]:
            assert br0 == char.bit_rate, "please use another Link class"
        # We do not need the parameter anymore, thus delete it to free memory.
        object.__delattr__(contact, "param")

    async def transmit(self, message, metadata) -> None:
        """Transmit the provided message over the link."""
        # If the contact does not transmit anything, block indefinitely.
        if self.effective_data_rate <= 0:
            while True:
                await asyncio.sleep(86400)  # duration should not exceed 1 day
        tx_duration = message.size / self.effective_data_rate
        await asyncio.sleep(tx_duration)
        # We schedule reception of the message after the specified link delay.
        time = asyncio.get_running_loop().time()
        # one full round-trip is needed b/c of ACKs
        rt_delay = self.delays.get_entry_for(time) * 2
        if time + rt_delay > message.deadline:
            return
        asyncio.ensure_future(self.contact.rx_node.schedule_reception(
            message,
            self.contact.tx_node,
            rt_delay,
            metadata,
        ))
