import functools

from .helpers import make_payload


class JSONRPC:
    def __init__(self, url):
        """Build

        Parameters
        ----------
        url : the URL of the JSON-RPC endpoint.
        """
        self.url = url
        self.session = None

    def dispatch(self, name=None):
        """Dispatch

        Parameters
        ----------
        name : (optional) the JSON-RPC method name, otherwise
            use the function name

        Examples
        --------

        >>> j = JSONRPC()
        >>> j.session = requests.Session()
        >>> @j.dispatch(name="methodName")
            def method(key: str, amount: int) -> None:
                ...
        >>> # call
        >>> result = method()
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                payload = make_payload(name or func.__name__, kwargs.copy())
                response = self.session.post(self.url, json=payload)
                response.raise_for_status()
                return response.json()["result"]

            return wrapper

        return decorator
