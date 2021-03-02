import re

from ..raw.core.types import RpcError


class RpcException(Exception):
    """Exception base for any MTProto rpc error.

    :parameter:
        rpc_error: core.types.RpcError -- The serialized RpcError TL object.
    """

    def __init__(self, rpc_error: RpcError):
        rpc_re = re.compile("([A-Z]+((_[A-Z]+)+)?)|([0-9]+)")
        _ = [
            (int(x[0] or x[-1])
             if (x[0] or x[-1]).isdigit()
             else (x[0] or x[-1]))
            for x in rpc_re.findall(rpc_error.error_message)
            if any(x)
        ]

        self.rpc_error = rpc_error
        self.code = rpc_error.error_code
        self.description = _[0]
        self.x = _[1] if len(_) > 1 else None
        self.args = tuple(_[2:]) if len(_) > 2 else ()
        super().__init__(str(self))

    def __str__(self):
        return f"[{self.code} ~ {self.description}] An error occurred.{'' if self.x is None else f' Value: {self.x}'}"
