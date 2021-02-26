# encoding: utf-8

"""Helper classes for connecting to a uPCN instance."""

import asyncio

from typing import Optional

from pyupcn.aap import AAPMessage, AAPMessageType, InsufficientAAPDataError
from pyupcn.spp import SPPPacket, SPPPacketHeader, SPPTimecode


class AsyncTCPConnection:
    """An async context manager class for establishing TCP connections.

    Args:
        host: The host (hostname or IP) to connect to.
        port: The port number to connect to.
        loop: The EventLoop to be used. If None, asyncio.get_event_loop() is
            called to obtain it.

    """

    def __init__(self, host: str, port: int,
                 loop: asyncio.AbstractEventLoop = None) -> None:
        self.host = host
        self.port = port
        self.loop = loop or asyncio.get_event_loop()
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None

    async def __aenter__(self) -> "AsyncTCPConnection":
        """Connect to the endpoint specified during initialization."""
        await self.connect()
        return self

    async def connect(self) -> None:
        """Connect to the endpoint specified during initialization."""
        self.reader, self.writer = await asyncio.open_connection(
            self.host, self.port, loop=self.loop
        )

    async def disconnect(self) -> None:
        """Disconnect and close the socket."""
        if self.writer is not None:
            await self.writer.drain()
            self.writer.close()
            self.writer = None
        self.reader = None

    async def send(self, data: bytes) -> None:
        """Send the provided binary data over the socket connection."""
        if self.writer is None:
            raise RuntimeError("Not connected to endpoint")
        self.writer.write(data)
        await self.writer.drain()

    async def recv(self, count: int) -> bytes:
        """Attempt to receive the exact amount of bytes provided."""
        if self.reader is None:
            raise RuntimeError("Not connected to endpoint")
        return await self.reader.readexactly(count)

    async def __aexit__(self, *args) -> None:
        """Disconnect and close the socket."""
        await self.disconnect()


class AsyncAAPConnection(AsyncTCPConnection):
    """An async context manager class for establishing uPCN-AAP connections.

    Args:
        host: The host (hostname or IP) to connect to.
        port: The port number to connect to.
        loop: The EventLoop to be used. If None, asyncio.get_event_loop() is
            called to obtain it.

    """

    def __init__(self, host: str, port: int,
                 loop: asyncio.AbstractEventLoop = None) -> None:
        super().__init__(host, port, loop)
        self.eid: Optional[str] = None
        self.agent_id: Optional[str] = None
        self.full_eid: Optional[str] = None

    async def connect(self) -> None:
        """Connect to the AAP endpoint specified during initialization."""
        await super().connect()
        msg_welcome = await self.recv_aap()
        assert msg_welcome.msg_type == AAPMessageType.WELCOME
        self.eid = msg_welcome.eid

    async def register(self, agent_id: str) -> None:
        """Attempt to register the specified agent identifier.

        Args:
            agent_id: THe agent identifier to be registered.

        """
        await self.send(
            AAPMessage(AAPMessageType.REGISTER, agent_id).serialize()
        )
        msg_register = await self.recv_aap()
        assert msg_register.msg_type == AAPMessageType.ACK
        if self.eid is not None:
            self.agent_id = agent_id
            self.full_eid = self.eid + "/" + agent_id

    async def send_ping(self) -> None:
        """Send a PING message via AAP (e.g. for keepalive purposes)."""
        await self.send(AAPMessage(AAPMessageType.PING).serialize())

    async def send_bundle(self, destination: str, bundle_data: bytes) -> None:
        """Send the provided bundle to the AAP endpoint.

        Args:
            destination: The destination EID.
            bundle_data: The binary payload data to be encapsulated in a
                bundle.

        """
        await self.send(
            AAPMessage(
                AAPMessageType.SENDBUNDLE,
                destination,
                bundle_data,
            ).serialize()
        )

    async def recv_aap(self) -> AAPMessage:
        """Receive and return the next AAP message."""
        data = bytearray()
        next_len = 1
        while True:
            data += await self.recv(next_len)
            try:
                return AAPMessage.parse(data)
            except InsufficientAAPDataError as err:
                next_len = len(data) - err.bytes_needed


class AsyncTCPSPPConnection(AsyncTCPConnection):
    """An async context manager class for establishing TCPSPP connections.

    Args:
        host: The host (hostname or IP) to connect to.
        port: The port number to connect to.
        use_crc: Specifies whether or not to use a CRC in SPP packets.
        loop: The EventLoop to be used. If None, asyncio.get_event_loop() is
            called to obtain it.

    """

    def __init__(self, host: str, port: int, use_crc: bool = True,
                 loop: asyncio.AbstractEventLoop = None) -> None:
        super().__init__(host, port, loop)
        self.use_crc = use_crc

    async def send_spp(self, bundle: bytes) -> None:
        """Send the provided (serialized) bundle to the SSP endpoint.

        Args:
            bundle: The binary serialized bundle data.

        """
        await self.send(bytes(SPPPacket(
            SPPPacketHeader(
                timecode=SPPTimecode(),
            ),
            bundle,
            has_crc=self.use_crc,
        )))

    async def recv_spp(self) -> bytes:
        """Receives the next bundle from the SPP endpoint."""
        hdr_raw = await self.recv(6)
        data_length, has_secondary = SPPPacketHeader.preparse_data_length(
            hdr_raw
        )
        data_plus_secondary = await self.recv(data_length)
        packet, _ = SPPPacket.parse(
            hdr_raw + data_plus_secondary,
            timecode_used=has_secondary,
            has_crc=self.use_crc,
        )
        if self.use_crc:
            assert packet.crc_provided == packet.crc()
        return packet.payload
