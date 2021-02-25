"""Prod-ready HTTP client with timeout and retries by default."""
# pylint: disable=too-few-public-methods
import email.parser
import importlib.metadata
import re
import typing as t
import warnings

import orjson
import requests
from memoization import cached
from pydantic import AnyHttpUrl, BaseSettings
from requests import exceptions as errors
from requests.adapters import HTTPAdapter
from requests.cookies import cookiejar_from_dict
from requests.sessions import Session
from requests.structures import CaseInsensitiveDict
from urllib3.util.retry import Retry

__version__ = importlib.metadata.version("fw-http-client")
__all__ = [
    "get_client",
    "HttpConfig",
    "HttpClient",
    "load_useragent",
]


RETRY_METHODS = ["DELETE", "GET", "HEAD", "POST", "PUT", "OPTIONS"]
RETRY_STATUSES = [429, 500, 502, 503, 504]

# necessary evil for performance - use orjson for loading and dumping
requests.models.complexjson = orjson  # type: ignore


class HttpConfig(BaseSettings):
    """HTTP client configuration."""

    class Config:
        """Enable envvar config using prefix 'FW_HTTP_'."""

        env_prefix = "fw_http_"

    client_name: str
    client_version: str
    client_info: t.Dict[str, str] = {}

    baseurl: t.Optional[AnyHttpUrl]
    cookies: t.Dict[str, str] = {}
    headers: t.Dict[str, str] = {}
    params: t.Dict[str, str] = {}
    cert: t.Optional[t.Union[str, t.Tuple[str, str]]]
    auth: t.Optional[t.Tuple[str, str]]
    proxies: t.Dict[str, str] = {}
    verify: bool = True
    trust_env: bool = True
    connect_timeout: float = 5
    read_timeout: float = 15
    max_redirects: int = 30
    stream: bool = False
    response_hooks: t.List[t.Callable] = []
    retry_backoff_factor: float = 0.5
    retry_allowed_methods: t.List[str] = RETRY_METHODS
    retry_status_forcelist: t.List[int] = RETRY_STATUSES
    retry_total: int = 5


class HttpClient(Session):  # pylint: disable=too-many-instance-attributes
    """Prod-ready HTTP client with timeout and retries by default."""

    def __init__(self, config: t.Optional[HttpConfig] = None) -> None:
        """Init client instance using attrs from HttpConfig."""
        super().__init__()
        config = config or HttpConfig()
        self.baseurl = config.baseurl or ""
        self.cookies = cookiejar_from_dict(config.cookies)
        self.headers.update(config.headers)
        self.headers["User-Agent"] = dump_useragent(
            config.client_name,
            config.client_version,
            **config.client_info,
        )
        self.params.update(config.params)  # type: ignore
        self.cert = config.cert
        self.auth = config.auth
        self.proxies = config.proxies
        self.verify = config.verify
        self.trust_env = config.trust_env
        self.timeout = (config.connect_timeout, config.read_timeout)
        self.max_redirects = config.max_redirects
        self.stream = config.stream
        self.hooks = {"response": config.response_hooks}
        retry = Retry(
            backoff_factor=config.retry_backoff_factor,
            allowed_methods=config.retry_allowed_methods,
            status_forcelist=config.retry_status_forcelist,
            total=config.retry_total,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.mount("http://", adapter)
        self.mount("https://", adapter)

    # pylint: disable=arguments-differ
    def request(  # type: ignore
        self, method: str, url: str, raw: bool = False, **kwargs: t.Any
    ) -> t.Any:
        """Send request and return loaded JSON response (AttrDict)."""
        kwargs.setdefault("timeout", self.timeout)
        # prefix relative paths with baseurl
        if not url.startswith("http"):
            url = f"{self.baseurl}{url}"
        if not url.startswith(self.baseurl):
            # TODO consider only allowing external requests via opt-in (raw?)
            # TODO consider stripping (auth) headers (allow, maybe simplify)
            pass
        context = f"{method} {url}"
        try:
            response = super().request(method, url, **kwargs)
        except (errors.ConnectionError, errors.RetryError) as exc:
            msg = get_connect_error_msg(exc)
            raise ConnectError(f"{context} - {msg}", exc) from exc
        if not raw:
            # raise if there was an http error (eg. 404)
            try:
                response.raise_for_status()
            except errors.HTTPError as exc:
                err = ClientError if response.status_code < 500 else ServerError
                msg = f"{context} - {response.status_code} {response.reason}"
                raise err(msg, exc) from exc
        # return response when streaming or raw=True
        if raw or self.stream or kwargs.get("stream"):
            # add multipart support (cast as subclass)
            response.__class__ = Response
            return response
        # never try to decode empty response
        if not response.content:
            return None
        try:
            return attrify(response.json())
        except orjson.JSONDecodeError as exc:
            cont = response.content[:20]
            if len(response.content) > 20:
                cont = cont[:-3] + b"..."
            raise DecodeError(f"{context} - invalid JSON {cont!r}", exc) from None


class RequestError(Exception):
    """Request error base class to wrap original exceptions with.

    Wrapping enables
      * providing simpler error messages that always include context
      * consolidating exception types for easier general adoption
      * making raising contract more explicit w/o requests knowledge
    """

    def __init__(self, message: str, error: Exception) -> None:
        """Initialize exception and store original error on self."""
        super().__init__(message)
        self.error = error


class ConnectError(RequestError):
    """Could not retrieve a response from the server."""


class ClientError(RequestError):
    """The server returned a response with 4xx status."""


class ServerError(RequestError):
    """The server returned a response with 5xx status."""


class DecodeError(RequestError):
    """The content could not be decoded as JSON."""


def get_connect_error_msg(error: Exception) -> str:
    """Extract the meaningful parts of the cryptic connection exceptions."""
    pattern = r".*?\((.*)\)"
    if isinstance(error, errors.RetryError):
        pattern = r".*\('(.*)'\).*"
    elif isinstance(error, errors.ConnectionError):
        pattern = r".*(\[.*)'\).*"
    err_cls = type(error)
    err_msg = re.sub(pattern, r"\1", str(error))
    return f"{err_cls.__name__}: {err_msg}"


class Response(requests.Response):
    """Response class with multipart message splitting/iter support.

    References:
      https://www.w3.org/Protocols/rfc1341/7_2_Multipart.html
      https://github.com/requests/toolbelt/blob/0.9.1/requests_toolbelt/multipart/decoder.py#L74
      https://github.com/MGHComputationalPathology/dicomweb-client/blob/v0.51.0/src/dicomweb_client/api.py#L697
    """

    def iter_parts(self, **kwargs: t.Any) -> t.Iterator["Part"]:
        """Yield individual message parts from a multipart response."""
        content_type = self.headers["content-type"]
        media_type, *ct_info = [ct.strip() for ct in content_type.split(";")]
        if not media_type.lower().startswith("multipart"):
            raise ValueError(f"Media type is not multipart: {media_type}")
        for item in ct_info:
            attr, _, value = item.partition("=")
            if attr.lower() == "boundary":
                boundary = value.strip('"')
                break
        else:
            # Some servers set the media type to multipart but don't provide a
            # boundary and just send a single frame in the body - yield as is.
            yield Part(self.content, split_header=False)
            return
        message = b""
        delimiter = f"\r\n--{boundary}".encode()
        preamble = True
        with self:
            for chunk in self.iter_content(**kwargs):
                message += chunk
                if preamble and delimiter[2:] in message:
                    preamble = False
                    message = message[len(delimiter) :]
                    continue
                while delimiter in message:
                    content, message = message.split(delimiter, maxsplit=1)
                    yield Part(content)
        if not message.startswith(b"--"):
            warnings.warn("Last boundary is not a closing delimiter")


class Part:
    """Single part of a multipart message with it's own headers and content."""

    def __init__(self, content: bytes, split_header: bool = True) -> None:
        """Initialize message part instance with headers and content."""
        if not split_header:
            headers = None
        elif b"\r\n\r\n" not in content:
            raise ValueError("Message part does not contain CRLF CRLF")
        else:
            header, content = content.split(b"\r\n\r\n", maxsplit=1)
            headers = email.parser.HeaderParser().parsestr(header.decode()).items()
        self.headers = CaseInsensitiveDict(headers or {})
        self.content = content


@cached
def get_client(**kwargs: t.Any) -> HttpClient:
    """Return (cached) HttpClient configured via kwargs."""
    return HttpClient(HttpConfig(**kwargs))


def dump_useragent(name: str, version: str, **kwargs: str) -> str:
    """Return parsable UA string for given name, version and extra keywords."""
    info = "; ".join(f"{k}:{v}" for k, v in sorted(kwargs.items()))
    info_str = f" ({info})" if kwargs else ""
    return f"{name}/{version}{info_str}"


def load_useragent(useragent: str) -> t.Dict[str, str]:
    """Return name, version and extra keywords parsed from UA string."""
    name, _, useragent = useragent.partition("/")
    version, _, useragent = useragent.partition(" ")
    info = {}
    info_str = useragent.strip("()")
    if info_str:
        for item in info_str.split("; "):
            key, value = item.split(":", maxsplit=1)
            info[key] = value
    return AttrDict(name=name, version=version, **info)


def attrify(data: t.Any) -> t.Any:
    """Return data with dicts cast to AttrDict for dot notation access."""
    if isinstance(data, dict):
        return AttrDict((key, attrify(value)) for key, value in data.items())
    if isinstance(data, list):
        return [attrify(elem) for elem in data]
    return data


class AttrDict(dict):
    """Dictionary allowing attribute access to valid-python-id keys."""

    def __getattr__(self, name: str) -> t.Any:
        try:
            return self[name]
        except KeyError as exc:  # pragma: no cover
            raise AttributeError(name) from exc
