from .transports import TCPAbridged, TCPIntermediate, TCPFull
from ..utils import DC, asyncrange


class Connection:
    MAX_RETRIES = 5

    transports = [TCPAbridged, TCPIntermediate, TCPFull]

    def __init__(self, dc_id: int, transport: int = 0, test_mode: bool = False):
        self.transport = self.transports[transport]()
        self.test_mode = test_mode
        self.connected = False
        self.dc_id = dc_id

    async def connect(self):
        assert not self.connected, "connection.py: Already connected."
        self.connected = True

        async for retry in asyncrange(self.MAX_RETRIES):
            try:
                await self.transport.connect(DC(self.dc_id, self.test_mode), 80)
            except OSError as e:
                if retry == self.MAX_RETRIES - 1:
                    raise e
            else:
                break

    async def close(self):
        assert self.connected, "connection.py: connection is already closed."
        self.connected = False
        await self.transport.close()

    async def send(self, data: bytes):
        await self.transport.send(data)

    async def recv(self) -> bytes:
        return await self.transport.recv()

    def __str__(self):
        return f"Connection(test_mode={self.test_mode}, dc_id={self.dc_id}, connected={self.connected})"
