"""
Flask JSON-RPC extension.
"""

from typing import Any

import fastapi as fa

import pjrpc.server


class JsonRPC:
    """
    `FastAPI <https://fastapi.tiangolo.com/>`_ framework JSON-RPC extension class.

    :param path: JSON-RPC handler base path
    :param kwargs: arguments to be passed to the dispatcher :py:class:`pjrpc.server.Dispatcher`
    """

    def __init__(self, path: str, **kwargs: Any):
        self._path = path
        self._dispatcher = pjrpc.server.Dispatcher(**kwargs)

    @property
    def dispatcher(self) -> pjrpc.server.Dispatcher:
        """
        JSON-RPC method dispatcher.
        """

        return self._dispatcher

    def init_app(self, app: fa.FastAPI) -> None:
        """
        Initializes flask application with JSON-RPC extension.

        :param app: flask application instance
        """

        app.post(self._path)(self._rpc_handle)

    def _rpc_handle(self, body: fa.Body(None)) -> fa.Response:
        """
        Handles JSON-RPC request.

        :returns: flask response
        """

        response_text = self._dispatcher.dispatch(body)
        if response_text is None:
            return fa.Response(status_code=200)
        else:
            return fa.Response(status_code=200, content=response_text)
