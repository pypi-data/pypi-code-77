import platform

from chameleongram.auth_key import AuthKey
from chameleongram.connection import Connection
from chameleongram.exceptions import RpcException
from chameleongram.raw import core, functions, layer
from chameleongram.utils import asyncrange
from ..base import Base


class Connect(Base):
    async def connect(
            self,
            dc_id: int = None,
            test_mode: bool = None,
            transport: int = None,
    ):
        """Establish a connection with Telegram servers."""

        self.auth_key = None
        self.auth_key_id = None
        self.server_salt = None
        self.session_id = self.rnd()
        self.dc_id = dc_id or self.dc_id

        async for _ in asyncrange(self.MAX_RETRIES):
            await self.stop()
            self.auth_key, self.server_salt = await AuthKey(
                dc_id or self.dc_id, test_mode or self.test_mode
            ).generate()
            self.connection = Connection(
                dc_id or self.dc_id,
                test_mode=test_mode or self.test_mode,
                transport=transport or self.transport,
            )
            await self.connection.connect()
            try:
                await self(core.functions.Ping(ping_id=0))

                await self(
                    functions.InvokeWithLayer(
                        layer=layer,
                        query=functions.InitConnection(
                            api_id=self.api_id,
                            app_version=self.__version__,
                            device_model=f"{platform.python_implementation()} {platform.python_version()}",
                            lang_code="en",
                            lang_pack="",
                            query=functions.help.GetConfig(),
                            system_lang_code="en",
                            system_version=f"{platform.system()} {platform.release()}",
                        ),
                    )
                )
                return self
            except (RpcException, AssertionError) as error:
                if type(error) is AssertionError:
                    ...
                elif error.description == "USER_MIGRATE":
                    self.auth_key = None
                    self.auth_key_id = None
                    self.server_salt = None
                    self.session_id = self.rnd()
                    self.dc_id = error.x
                    continue
                else:
                    raise error
