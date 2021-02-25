import inspect
from typing import TypeVar, Dict, Callable
from xwire.common import decorator_utils
from xwire.rest._private.proxy.decorators import cookies, resource

T = TypeVar('T')


def get_cookies(resource_obj: T) -> Dict[str, str]:
    resource_metadata = decorator_utils.get_decorator_metadata(resource_obj, resource)
    cookies_method: Callable[..., Dict[str, str]] = resource_metadata['cookies']
    if cookies_method is None:
        methods = inspect.getmembers(resource_obj, inspect.ismethod)
        for _, method in methods:
            if decorator_utils.has_decorator(method, cookies):
                cookies_method = method
                resource_metadata['cookies'] = cookies_method
                decorator_utils.set_decorator_metadata(resource_obj, resource, resource_metadata)
                return cookies_method()
        return {}
    else:
        return cookies_method()
