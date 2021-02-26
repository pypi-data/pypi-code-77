import functools
import logging
import time

import arrow
from google.cloud.exceptions import Conflict, ServiceUnavailable

from ..exceptions import RetryError, TransientException

logger = logging.getLogger(__name__)


def retry_target(target, deadline=None, on_error=None, sleep=None):
    """Call a function and retry if it fails.

    Paremeters:
        target(Callable):
            The function to call and retry.
        deadline (float):
            How long to keep retrying the target. The last sleep period is shortened as necessary,
            so that the last retry runs at ``deadline`` (and not considerably beyond it).
        on_error (Callable[Exception]):
            A function to call while processing a retryable exception. Any error raised by this
            function will *not* be caught.
        sleep (int):
            An integer that defines how long to speel for between retries.
    Returns:
        Any: the return value of the target function.
    Raises:
        rbx.exceptions.RetryError: If the deadline is exceeded while retrying.
        Exception: If the target raises a method that isn't retryable.
    """
    deadline = deadline or 30
    deadline_datetime = arrow.utcnow().shift(seconds=deadline).datetime
    sleep = sleep or 1
    last_exc = None

    while True:
        try:
            return target()

        # pylint: disable=broad-except
        # This function explicitly must deal with broad exceptions.
        except Exception as exc:
            if not isinstance(exc, (Conflict, ServiceUnavailable, TransientException)):
                raise
            last_exc = exc
            if on_error is not None:
                on_error(exc)

        now = arrow.utcnow().datetime

        if deadline_datetime <= now:
            raise RetryError(
                f'Deadline of {deadline:.1f}s exceeded while calling {target}',
                last_exc
            ) from last_exc

        logger.debug(f'Retrying due to {last_exc}, sleeping {sleep:.1f}s ...')
        time.sleep(sleep)


def retry(func, *args, **kwargs):
    deadline = kwargs.pop('deadline', None)
    on_error = kwargs.pop('on_error', None)
    sleep = kwargs.pop('sleep', None)
    target = functools.partial(func, *args, **kwargs)
    return retry_target(target, deadline=deadline, on_error=on_error, sleep=sleep)
