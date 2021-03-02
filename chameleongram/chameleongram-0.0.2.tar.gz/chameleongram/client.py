import hashlib
import logging
import os
from typing import Final, Union, List

from chameleongram.connection import Connection
from chameleongram.crypto import AES
from chameleongram.exceptions import RpcException, Propagate, NowStop
from chameleongram.filters import Filters
from chameleongram.handlers import Handlers
from chameleongram.methods import Methods
from chameleongram.raw import core
from chameleongram.raw.primitives import (
    TL,
    Long,
    MessageID,
    SeqNo,
    MsgContainer,
    CoreMessage,
    Int,
)
from chameleongram.raw.reader import Reader


class Client(Methods, Handlers):
    """MTProto Client itself"""

    MAX_RETRIES: int = 5
    __version__: Final[str] = "0.0.1"
    __start__ = f"ChameleonGram started. Version: {__version__} | @ChameleonGram"
    _started: bool = False

    @staticmethod
    def dont_stop():
        """
        By default, after an handler is executed, client will stop propagating the update to
        other handlers.
        By calling this function in an handler, it will propagate the update to *all* handlers.
        """

        raise Propagate()

    @staticmethod
    def now_stop():
        """
        The opposite of `Client,dont_stop`, this will stop propagation of the update among handlers.
        """

        raise NowStop()

    @classmethod
    def create_filter(cls, func: callable) -> Filters:
        return Filters.create(func, cls)

    @classmethod
    def show_message(cls):
        """
        Show the startup message (`Client.__start__`)
        """

        if not cls._started:
            print(cls.__start__)
        cls._started = True

    @staticmethod
    def rnd(as_int: bool = False) -> Union[bytes, int]:
        """Generates a random id (8 bytes)"""

        return (
            int.from_bytes(os.urandom(8), "little", signed=True)
            if as_int
            else os.urandom(8)
        )

    async def import_auth_key(self, auth_key: Union[bytes, List[int]]):
        raise NotImplementedError()
        await self.stop()
        self.auth_key = auth_key if isinstance(auth_key, bytes) else bytes(auth_key)
        self.auth_key_id = hashlib.sha1(self.auth_key).digest()[-8:]
        # TODO: import auth key here, and connect (connect(auth_key=...))

    def encrypt(self, payload: bytes, tl_object) -> bytes:
        if not self.auth_key_id:
            self.auth_key_id = hashlib.sha1(self.auth_key).digest()[-8:]
        msg_id = MessageID.getvalue().to_bytes(8, "little")
        auth_key = self.auth_key
        seq_no = SeqNo.getvalue(
            is_content_related=isinstance(
                tl_object,
                (
                    core.functions.Ping,
                    core.types.HttpWait,
                    core.types.MsgsAck,
                    MsgContainer,
                ),
            )
        )
        payload: bytes = (
                self.server_salt
                + self.session_id
                + msg_id
                + seq_no.to_bytes(4, "little", signed=True)
                + len(payload).to_bytes(4, "little", signed=True)
                + payload
        )
        payload += os.urandom(-(len(payload) + 12) % 16 + 12)
        msg_key_large = hashlib.sha256(auth_key[88:120] + payload).digest()
        msg_key = msg_key_large[8:24]
        a = hashlib.sha256(msg_key + auth_key[:36]).digest()
        b = hashlib.sha256(auth_key[40:76] + msg_key).digest()
        aes_key = a[:8] + b[8:24] + a[24:32]
        aes_iv = b[:8] + a[8:24] + b[24:32]
        return self.auth_key_id + msg_key + AES.encrypt_ige(payload, aes_key, aes_iv)

    def decrypt(self, data: bytes) -> TL:
        if not self.auth_key_id:
            self.auth_key_id = hashlib.sha1(self.auth_key).digest()[-8:]
        auth_key = self.auth_key
        data = Reader(data)
        auth_key_id = data.read(8)
        assert auth_key_id == self.auth_key_id, "Response Auth Key ID is not valid."
        response_msg_key = data.read(16)
        a = hashlib.sha256(response_msg_key + auth_key[8:44]).digest()
        b = hashlib.sha256(auth_key[48:84] + response_msg_key).digest()
        aes_key = a[:8] + b[8:24] + a[24:32]
        aes_iv = b[:8] + a[8:24] + b[24:32]
        plaintext = AES.decrypt_ige(data.read(), aes_key, aes_iv)
        msg_key = hashlib.sha256(self.auth_key[96: 96 + 32] + plaintext).digest()[8:24]
        assert msg_key == response_msg_key, "Response Msg Key is not valid."
        plaintext = Reader(plaintext)
        plaintext.read(8)
        response_session_id = plaintext.read(8)
        assert response_session_id == self.session_id, (
            "Response client session id is different, exiting...",
            self.connection.close(),
        )[0]
        return CoreMessage.read(plaintext)

    async def send(self, tl_object: TL) -> TL:
        assert self.connection, "Client is not initialized."
        data: bytes = tl_object.getvalue()
        if self.auth_key:
            await self.connection.send(
                self.encrypt(
                    data,
                    tl_object,
                )
            )
        else:
            await self.connection.send(
                bytes(8)
                + Long.getvalue(MessageID.getvalue())
                + Int.getvalue(len(data))
                + data
            )
        return await self.recv()

    async def recv(self) -> TL:
        data = await self.connection.recv()
        if len(data) == 4:
            assert (
                    len(data) != 4
            ), f"[Client][Transport] len(recv()) is 4 (_all[{int.from_bytes(data, 'little', signed=True)}])"
        if self.auth_key:
            tl_object = self.decrypt(data)
        else:
            tl_object = Reader(data[20:]).getobj()
        if isinstance(tl_object, CoreMessage) and isinstance(
                tl_object.body, core.types.RpcResult
        ):
            if isinstance(tl_object.body.result, core.types.RpcError):
                raise RpcException(rpc_error=tl_object.body.result)
        return tl_object

    def __init__(
            self,
            api_id: int,
            api_hash: str,
            token: str = None,
            dc_id: int = 2,
            test_mode: bool = False,
            transport: int = 0,
            blueprint: tuple = (),
            phone_number: str = None,
            custom_traceback: bool = True,
    ):
        self.connection = None
        self.auth_key = None
        self.auth_key_id = None
        self.server_salt = None
        self.session_id: bytes = self.rnd()
        self.dc_id = dc_id
        self.api_id = api_id
        self.api_hash = api_hash
        self.token = token
        self.test_mode = test_mode
        self.transport = transport
        self.blueprint = blueprint
        self.phone_number = phone_number
        if custom_traceback:
            try:
                import pretty_errors

                pretty_errors.configure(
                    separator_character="🭸",
                    line_number_first=True,
                    display_link=True,
                    lines_before=3,
                    lines_after=0,
                    truncate_code=True,
                    header_color=pretty_errors.RED,
                    link_color="╭─"
                               + pretty_errors.BRIGHT_BLACK
                               + pretty_errors.RED_BACKGROUND,
                    code_color="╽ "
                               + pretty_errors.GREEN
                               + pretty_errors.BLACK_BACKGROUND,
                    line_color="╰─"
                               + pretty_errors.BLACK_BACKGROUND
                               + pretty_errors.BRIGHT_YELLOW,
                    exception_arg_color="╰─> " + pretty_errors.BRIGHT_YELLOW,
                )
            except ImportError:
                logging.warning(
                    "pretty_errors not installed."
                    + " Consider installing it or passing 'custom_traceback=False' to Client(...)"
                )

    async def __aenter__(self):
        self.connection = Connection(
            dc_id=self.dc_id, test_mode=self.test_mode, transport=self.transport
        )
        await self.connection.connect()
        return await self.start()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

    def __repr__(self):
        return f"Client(dc_id={self.dc_id})"

    def __str__(self):
        return (
            f"<{type(self).__name__}(dc_id={self.dc_id}, test_mode={self.test_mode})>"
        )

    __call__ = send
