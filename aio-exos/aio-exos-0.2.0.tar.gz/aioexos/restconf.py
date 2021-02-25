"""
This file contains the Extreme EXOS RESTCONF device asyncio Client.
"""

# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from typing import Optional

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

import httpx

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["Device"]


class Device(httpx.AsyncClient):
    """
    This Device class provides the asyncio RESTCONF client for Extreme EXOS.
    The device must be configured with web http or https service.

    References
    ----------
    https://api.extremenetworks.com/EXOS/ProgramInterfaces/RESTCONF/RESTCONF.html
    """

    BODY_XML = "application/yang-data+xml"
    BODY_JSON = "application/yang-data+xml"

    DEFAULT_PROTO = "https"
    URL_RESTCONF = "/rest/restconf/data/"

    def __init__(self, host, username, password, proto=None, **kwargs):
        base_url = f"{proto or self.DEFAULT_PROTO}://{host}"
        kwargs.setdefault("verify", False)

        super().__init__(base_url=base_url, **kwargs)

        self.headers["Content-Type"] = "application/json"
        self.body_format = self.BODY_JSON
        self.token: Optional[str] = None
        self.__auth = dict(username=username, password=password)

    @property
    def body_format(self):
        return self.headers["Accept"]

    @body_format.setter
    def body_format(self, content_type: str):
        allowed = [self.BODY_JSON, self.BODY_XML]
        if content_type not in allowed:
            raise ValueError(f"{content_type} not one of [{allowed}]")
        self.headers["Accept"] = content_type

    async def login(self):
        """
        This coroutine is used to authenticate with the device to obtain a
        session token used for further command access.  Upon completiton the
        base URL will be shifted to use the URL_RESTCONF value.

        Raises
        ------
        httpx.HTTPError if request status is not OK.
        """
        res = await self.post("/auth/token/", json=self.__auth)
        res.raise_for_status()

        self.token = res.json()["token"]
        self.headers["cookie"] = f"x-auth-token={self.token}"
        self.base_url = self.base_url.join(self.URL_RESTCONF)
