from __future__ import annotations

import socket
from binascii import crc32
from typing import Union

import trio


class TCP:
    """TCP base class"""

    def __init__(self):
        self.sock = socket.socket()
        self.asock = None

    async def connect(self, *address) -> TCP:
        self.sock.connect(address)
        self.asock = trio.SocketStream(trio.socket.from_stdlib_socket(self.sock))
        return self

    async def send(self, data: bytes):
        await self.asock.send_all(data)

    async def recv(self, length: int = 0) -> bytes:
        return await self.asock.receive_some(length)

    async def close(self):
        await self.asock.aclose()
        self.asock = None
        self.sock = None


class TCPAbridged(TCP):
    """TCP Abridged - https://core.telegram.org/mtproto/mtproto-transports#abridged"""

    async def connect(self, *address):
        await super().connect(*address)
        await super().send(b"\xef")

    async def send(self, data: bytes):
        length = len(data) // 4

        await super().send(
            (
                length.to_bytes(1, "little")
                if length <= 126
                else b"\x7f" + length.to_bytes(3, "little")
            )
            + data
        )

    async def recv(self) -> bytes:
        length = await super().recv(1)

        if length == b"\x7f":
            length = await super().recv(3)
        return await super().recv(int.from_bytes(length, "little") * 4)


class TCPIntermediate(TCP):
    """TCP Intermediate - https://core.telegram.org/mtproto/mtproto-transports#intermediate"""

    async def connect(self, *address):
        await super().connect(*address)
        await super().send(b"\xee" * 4)

    async def send(self, data: bytes):
        await super().send(len(data).to_bytes(4, "little") + data)

    async def recv(self) -> bytes:
        return await super().recv(int.from_bytes(await super().recv(4), "little"))


class TCPFull(TCP):
    """TCP Full - https://core.telegram.org/mtproto/mtproto-transports#full"""

    def __init__(self):
        super().__init__()
        self.seq_no = None

    async def connect(self, *address):
        await super().connect(*address)
        self.seq_no = 0

    async def send(self, data: bytes, *args):
        data = (
                (len(data) + 12).to_bytes(4, "little")
                + self.seq_no.to_bytes(4, "little")
                + data
        )
        data += crc32(data).to_bytes(4, "little")
        self.seq_no += 1
        await super().send(data)

    async def recv(self, length: int = 0) -> Union[bytes, None]:
        length = await super().recv(4)
        if length is None:
            return None
        packet = await super().recv(int.from_bytes(length, "little") - 4)
        if packet is None:
            return None
        packet = length + packet
        checksum = packet[-4:]
        packet = packet[:-4]
        if crc32(packet) != int.from_bytes(checksum, "little"):
            return None
        return packet[8:]
