import asyncio
import os
from typing import Optional

import attr
from aiohttp import ClientSession

from isilon.api import Accounts, Containers, Discoverability, Endpoints, Objects
from isilon.creds import Credentials


@attr.s
class IsilonClient:
    address = attr.ib(
        type=str,
        default=os.getenv("ISILON_ADDRESS", "http://localhost:8080"),
        validator=attr.validators.instance_of(str),
    )
    account = attr.ib(
        type=str,
        default=os.getenv("ISILON_ACCOUNT", "test"),
        validator=attr.validators.instance_of(str),
    )
    user = attr.ib(
        type=str,
        default=os.getenv("ISILON_USER", "tester"),
        validator=attr.validators.instance_of(str),
    )
    password = attr.ib(
        type=str,
        default=os.getenv("ISILON_PASSWORD", "testing"),
        validator=attr.validators.instance_of(str),
    )
    http = attr.ib(
        type=Optional[ClientSession],
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(ClientSession)),
        repr=False,
    )

    def __attrs_post_init__(self) -> None:
        if self.http is None:
            loop = asyncio.get_event_loop()
            loop.create_task(self._create_client_session())
        self.credentials = Credentials(self)
        self.discoverability = Discoverability(self)
        self.objects = Objects(self)
        self.containers = Containers(self)
        self.endpoints = Endpoints(self)
        self.accounts = Accounts(self)

    async def _create_client_session(self):
        self.http = ClientSession()

    def __del__(self) -> None:
        if not self.http.closed:  # type: ignore
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.shield(self.http.close()))  # type: ignore


async def init_isilon_client(*args, **kwargs) -> IsilonClient:
    return IsilonClient(*args, **kwargs)
