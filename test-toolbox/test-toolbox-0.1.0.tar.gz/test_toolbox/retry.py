import time
from typing import Any, Callable, Union

from test_toolbox.timer import Timer

TimeoutSeconds = Union[float, int]
TestedReturnValue = Any
TestedCallable = Callable[[], TestedReturnValue]

_POLL_INTERVAL_SECONDS = 0.5


def retry_until_returns_value(callable_: TestedCallable,
                              return_value: TestedReturnValue,
                              timeout: TimeoutSeconds) -> None:
    """
    Repeatedly calls the given `callable_` until it returns the given
    `return_value`.

    Raises a TimeoutError if `callable_` does not return `return_value`
    within the given `timeout` number of seconds.
    """
    timer = Timer()
    while True:
        current_result = callable_()
        if current_result == return_value:
            return

        time.sleep(_POLL_INTERVAL_SECONDS)
        if timer.elapsed > timeout:
            raise TimeoutError()


def retry_until_pass_without_exception(callable_: TestedCallable,
                                       timeout: TimeoutSeconds) -> None:
    """
    Repeatedly calls the given `callable_` until it passes without
    raising an exception. Will re-raise the `callable_`'s exception
    if it hasn't run successfully after `timeout`.
    """
    timer = Timer()
    while True:
        try:
            callable_()
        except Exception:
            time.sleep(_POLL_INTERVAL_SECONDS)
            if timer.elapsed > timeout:
                raise
        else:
            break
