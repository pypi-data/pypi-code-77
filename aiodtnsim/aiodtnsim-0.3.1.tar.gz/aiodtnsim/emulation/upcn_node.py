# encoding: utf-8

"""A Node class allowing integration of the uPCN DTN software."""

import asyncio
import subprocess
import logging
import time
import os
import atexit

from typing import Any, Optional, Set, Dict

from pyupcn.agents import ConfigMessage, Contact as ContactDef
from pyupcn.helpers import UNIX_EPOCH, unix2dtn
from pyupcn import bundle7

from .. import BaseNode, Message, Contact
from ..timeutil import sleep_until, duration_until
from .aio_upcn_interface import AsyncTCPSPPConnection

KEEPALIVE_TIMEOUT = 300

logger = logging.getLogger(__name__)


class UPCNNode(BaseNode):
    """A Node implementation allowing to integrate the uPCN DTN software.

    Args:
        eid: The DTN Endpoint Identifier for the uPCN instance.
        event_dispatcher: An EventDispatcher for monitoring the simulation.
        upcn_path: The absolute path to the uPCN binary to be executed.
        spp_port: The port to be used for SPP.
        aap_port: The port to be used for AAP.
        reachable_nodes: A dict associating all neighbors of the Node to EIDs
            reachable via them. Will be provided to uPCN.
            The format is equal to that of the `vertices` dict contained in
            a TVG representation obtained from the `tvgutil` package.
        contact_setup_time: The time, in seconds, allowed before the contact
            start for uPCN to setup the connection.
            NOTE: When setting the setup time to zero we will
            run into synchronization issues (i.e. a race condition where the
            contact in uPCN starts earlier, leading to dropped bundles).
        contact_min_duration: The minimum duration, in seconds, for a contact
            to be used in uPCN. This prevents scheduling contacts that are
            too short in schedule_contact.
        max_tx_channels: The maximum amount of simultaneous transmission
            channels to be allocated by this node. If this amount of channels
            is reached, no new outgoing connections can be established.
            The default is None, meaning an unlimited amount.
        loop: The asyncio EventLoop to be used.

    """

    def __init__(self, eid: str, event_dispatcher: Any,
                 upcn_path: str, spp_port: int, aap_port: int,
                 reachable_nodes: Dict[str, Set[str]],
                 contact_setup_time: float = 1.,
                 contact_min_duration: int = 1,
                 max_tx_channels: Optional[int] = None,
                 max_rx_channels: Optional[int] = None,
                 aap_lifetime: int = 86400,
                 loop: asyncio.AbstractEventLoop = None) -> None:
        super().__init__(
            eid,
            event_dispatcher,
            tx_channels=max_tx_channels,
            rx_channels=max_rx_channels,
        )
        self.reachable_nodes = reachable_nodes
        self.contact_setup_time = contact_setup_time
        self.contact_min_duration = contact_min_duration
        self.receiving_from: Set[str] = set()
        self.current_contacts: Dict[str, Contact] = dict()
        self.tx_queue: asyncio.Queue = asyncio.Queue()
        upcn_process = subprocess.Popen([
            upcn_path,
            "-c",
            f"tcpspp:*,{spp_port}",
            "-a",
            str(aap_port),
            "-e",
            eid,
            "-l",
            str(aap_lifetime),
        ])
        atexit.register(upcn_process.terminate)
        logger.info(
            "Spawned uPCN (%d) for EID '%s': SPP @ %d/tcp, AAP @ %d/tcp",
            upcn_process.pid,
            eid,
            spp_port,
            aap_port,
        )
        loop = loop or asyncio.get_event_loop()
        self.time_offset_unix = int(time.time() - loop.time())
        # We need to keep track of which messages came from other nodes and
        # which came in via AAP.
        self.known_messages: Set[Message] = set()
        asyncio.ensure_future(
            self._upcn_handler("localhost", spp_port),
            loop=loop,
        )

    def add_known_message(self, message):
        """Add a message to the set of known messages.

        If a message is not contained in this set, an injection event is
        triggered upon reception. This could be the case, e.g., if the
        message was received via AAP.

        """
        original = message.original_message
        if original not in self.known_messages:
            self.known_messages.add(original)

    async def schedule_contact(self, contact: Contact) -> None:
        """Schedule the provided contact for execution."""
        # NOTE: This schedules uPCN == TX contacts.
        #       Contacts where uPCN == RX are opportunistic.
        assert self is contact.tx_node
        # Prevent scheduling contacts that are too short
        start_time = unix2dtn(self._sim2unix(contact.start_time))
        end_time = unix2dtn(self._sim2unix(contact.end_time))
        if (end_time <= start_time or
                end_time - start_time < self.contact_min_duration):
            logger.debug("Contact too short, dropping: %s", contact)
            return
        # Send the scheduling command to uPCN
        await self._schedule_contact_in_upcn(contact, start_time, end_time)
        # Wait until the contact starts
        await sleep_until(contact.start_time - self.contact_setup_time)
        # Add to local distribution list
        assert contact.rx_node.eid not in self.current_contacts
        self.current_contacts[contact.rx_node.eid] = contact
        self.event_dispatcher.contact_started(contact)
        # Wait until the contact has _really_ started.
        await sleep_until(contact.start_time)
        # Wait until the contact ends
        await sleep_until(contact.end_time)
        # Remove from local distribution list
        del self.current_contacts[contact.rx_node.eid]
        self.event_dispatcher.contact_ended(contact)

    async def _schedule_contact_in_upcn(self, contact: Contact,
                                        start_time: int,
                                        end_time: int) -> None:
        bit_rate = contact.bit_rate // 8  # uPCN bit rate is in bytes/sec
        config_bundle = bundle7.create_bundle7(
            "dtn:manager",
            self.eid + "/config",
            bytes(ConfigMessage(
                contact.rx_node.eid,
                "tcpspp:out",
                contacts=[
                    ContactDef(
                        start=int(start_time),
                        end=int(end_time),
                        bitrate=int(bit_rate),
                    )
                ],
                reachable_eids=list(
                    self.reachable_nodes.get(contact.rx_node.eid, [])
                ),
            )),
        )
        await self.tx_queue.put(bytes(config_bundle))

    async def schedule_injection(self, message: Message) -> None:
        """Schedule the provided message for injection into the network."""
        await sleep_until(message.start_time)
        self.add_known_message(message)
        self.event_dispatcher.message_injected(self, message)
        await self._message_to_upcn(message)

    async def schedule_reception(self, message: Message, tx_node: BaseNode,
                                 delay: float, metadata: Any) -> None:
        """Schedule the provided message for reception at the next hop."""
        await asyncio.sleep(delay)
        self.add_known_message(message)
        self.event_dispatcher.message_received(self, message, tx_node)
        await self._message_to_upcn(message)

    async def _message_to_upcn(self, message: Any):
        if self.eid == message.destination:
            self.event_dispatcher.message_delivered(self, message)
        try:
            binary_data = message.data
            if binary_data is None:
                raise TypeError
        except (AttributeError, TypeError):
            creation_timestamp = self._sim2unix(message.start_time)
            lifetime = self._sim2unix(message.deadline) - creation_timestamp
            size_bytes = message.size // 8
            assert size_bytes * 8 == int(message.size)
            bundle = bundle7.create_bundle7(
                message.source,
                message.destination,
                os.urandom(size_bytes),
                creation_timestamp=creation_timestamp,
                lifetime=lifetime,
            )
            binary_data = bytes(bundle)
            # reduce bundle size by header overhead to get approx. the
            # expected message size on wire - NOTE: only _approximately_!
            header_overhead = len(binary_data) - size_bytes
            new_pl_len = size_bytes - header_overhead
            assert new_pl_len > 0
            bundle.payload_block.data = bundle.payload_block.data[:new_pl_len]
            binary_data = bytes(bundle)
        logger.debug(
            "Sending bundle to '%s' (size = %d) to uPCN (EID '%s')",
            message.destination,
            len(binary_data),
            self.eid,
        )
        await self.tx_queue.put(binary_data)

    async def _upcn_handler(self, host: str, spp_port: int) -> None:
        spp_connection = AsyncTCPSPPConnection(host, spp_port)
        async with spp_connection:
            logger.info(
                "Connected via TCPSPP to %s:%d/tcp",
                host,
                spp_port,
            )
            await asyncio.wait({
                asyncio.create_task(self._handle_upcn_rx(spp_connection)),
                asyncio.create_task(self._handle_upcn_tx(spp_connection)),
            })

    async def _handle_upcn_rx(self, spp_connection: AsyncTCPSPPConnection):
        while True:
            spp_pl = await spp_connection.recv_spp()
            await self._message_from_upcn(spp_pl)

    async def _handle_upcn_tx(self, spp_connection: AsyncTCPSPPConnection):
        while True:
            try:
                outgoing = await asyncio.wait_for(
                    self.tx_queue.get(),
                    timeout=KEEPALIVE_TIMEOUT,
                )
                assert isinstance(outgoing, bytes)
                await spp_connection.send_spp(outgoing)
            except asyncio.TimeoutError:
                # Send a NULL-byte for TCP keepalive purposes
                await spp_connection.send_spp(b"\0")

    async def _message_from_upcn(self, spp_payload: bytes) -> None:
        bundle = bundle7.Bundle.parse(spp_payload)
        logger.debug(
            "Bundle received from uPCN @ '%s': '%s' -> '%s'",
            self.eid,
            bundle.primary_block.source,
            bundle.primary_block.destination,
        )
        # Bundle properties
        creation_timestamp_unix = (
            bundle.primary_block.creation_time.time - UNIX_EPOCH
        ).total_seconds()
        start_time = self._unix2sim(creation_timestamp_unix)
        deadline = self._unix2sim(
            creation_timestamp_unix +
            bundle.primary_block.lifetime
        )
        # NOTE: We create a new message all the time! (the Bundle changes)
        message = Message(
            start_time=start_time,
            source=_base_eid(bundle.primary_block.source),
            destination=_base_eid(bundle.primary_block.destination),
            # Message contains the size of the serialized bundle in bits
            size=(len(spp_payload) * 8),
            deadline=deadline,
            fragment_offset=(bundle.primary_block.fragment_offset
                             if bundle.is_fragmented else None),
            total_size=(bundle.primary_block.total_payload_length * 8
                        if bundle.is_fragmented else None),
            data=spp_payload,
        )
        # XXX Messages may be injected manually, e.g. via AAP. As these are
        # unknown to the simulator, an injection event has to be triggered
        # when they are first received from uPCN.
        if message.original_message not in self.known_messages:
            self.event_dispatcher.message_injected(self, message)
        # Simple broadcast transmission, waiting until messages arrive
        # This waits until the message has been transmitted via all contacts.
        await asyncio.gather(*[
            self._schedule_for_contact(message, contact)
            for _, contact in self.current_contacts.items()
        ])

    async def _schedule_for_contact(self, message: Message,
                                    contact: Contact) -> None:
        assert self is contact.tx_node
        try:
            await asyncio.wait_for(
                self._send_via_contact(message, contact),
                timeout=duration_until(contact.end_time),
            )
        except asyncio.TimeoutError:
            pass

    async def _send_via_contact(self, message: Message,
                                contact: Contact) -> None:
        async with self.channel(contact.rx_node):
            self.event_dispatcher.message_transmission_started(
                message,
                contact,
            )
            tx_duration = message.size / contact.bit_rate
            try:
                await asyncio.sleep(tx_duration)
            except asyncio.CancelledError:
                self.event_dispatcher.message_transmission_aborted(
                    message,
                    contact,
                )
                raise
            self.event_dispatcher.message_transmission_completed(
                message,
                contact,
            )
        # We schedule reception of the message after the specified link delay.
        asyncio.ensure_future(contact.rx_node.schedule_reception(
            message,
            self,
            contact.delay,
            None,  # NOTE: Should we fwd. metadata for e.g. SnW?
        ))

    def _sim2unix(self, sim_time: float):
        return int(sim_time + self.time_offset_unix)

    def _unix2sim(self, dtn_time: int):
        return int(dtn_time - self.time_offset_unix)


def _base_eid(eid: bundle7.EID):
    base_eid = "/".join(str(eid).split("/")[:-1])
    # The latter case indicates we have split a "dtn://"-EID without agent ID.
    if base_eid in ("", "dtn:/"):
        return str(eid)
    return base_eid
