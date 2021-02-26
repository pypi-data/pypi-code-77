# encoding: utf-8

"""Helper functions for dealing with simulation timestamps."""

import asyncio


def duration_until(simtime: float) -> float:
    """Obtain the time to wait until the specified simulation time is reached.

    The return value has the same unit as the simulation time. An asyncio
    event loop has to be running when calling this function. This function
    may only be called from within asyncio callbacks, tasks, or coroutines.
    """
    return simtime - asyncio.get_running_loop().time()


async def sleep_until(simtime: float) -> None:
    """Sleep using asyncio.sleep until the specified time is reached.

    This function returns immediately if the specified timestamp is in the
    past. This function may only be called from within asyncio callbacks,
    tasks, or coroutines.
    """
    duration = duration_until(simtime)
    if duration > 0:
        await asyncio.sleep(duration)
