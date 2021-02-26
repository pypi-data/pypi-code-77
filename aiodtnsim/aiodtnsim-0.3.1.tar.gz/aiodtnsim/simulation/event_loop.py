# encoding: utf-8

"""Helpers for realizing a discrete event simulator with asyncio."""

import heapq
import math
import asyncio
from concurrent.futures import CancelledError


# This is a modified version of:
# Source: https://gist.github.com/damonjw/35aac361ca5d313ee9bf79e00261f4ea
# Description: https://stackoverflow.com/a/45495507
# NOTE: This _has_ to access some protected variables, thus:
# pylint: disable=protected-access
class DESEventLoop(asyncio.AbstractEventLoop):
    """An AbstractEventLoop implementation for discrete event simulation."""

    def __init__(self, start_time=0):
        self._time = start_time
        self._running = False
        self._immediate = []
        self._scheduled = []
        self._exc = None
        self._debug = False

    def time(self):
        """Return the current time, as a float value."""
        return self._time

    # Methods for running the event loop.
    #
    # For a real asyncio system you need to worry a lot more about
    # running+closed. For a simple simulator, we completely control the
    # passage of time, so most of these functions are trivial.
    #
    # I've split the pending events into _immediate and _scheduled.
    # I could put them all in _scheduled; but if there are lots of
    # _immediate calls there's no need for them to clutter up the heap.

    def run_forever(self):
        """Run the event loop until stop() is called."""
        self._running = True
        asyncio.events._set_running_loop(self)
        while (self._immediate or self._scheduled) and self._running:
            if self._immediate:
                handle = self._immediate[0]
                self._immediate = self._immediate[1:]
            else:
                handle = heapq.heappop(self._scheduled)
                self._time = handle._when
                # XXX just for asyncio.TimerHandle debugging?
                handle._scheduled = False
            if not handle._cancelled:
                handle._run()
            if self._exc is not None:
                raise self._exc  # pylint: disable=raising-bad-type

    def run_until_complete(self, future):
        """Run until the future (an instance of Future) has completed."""
        raise NotImplementedError

    def _timer_handle_cancelled(self, handle):
        # NOTE: We could remove the handle from _scheduled, but instead we'll
        # just skip over it in the "run_forever" method.
        pass

    def is_running(self):
        """Return ``True`` if the event loop is currently running."""
        return self._running

    def is_closed(self):
        """Return ``True`` if the event loop was closed."""
        return not self._running

    def stop(self):
        """Stop the event loop."""
        self._running = False

    def close(self):
        """Close the event loop."""
        self._running = False

    async def shutdown_asyncgens(self):
        """Schedule all open asynchronous generator objects to close."""
        raise NotImplementedError

    def call_exception_handler(self, context):
        """Call the current event loop exception handler."""
        # If there is any exception in a callback, this method gets called.
        # I'll store the exception in self._exc, so that the main simulation
        # loop picks it up.
        self._exc = context.get("exception", None)

    # Methods scheduling callbacks.  All these return Handles.
    #
    # If the job is a coroutine, the end-user should call
    # asyncio.ensure_future(coro()).
    # The asyncio machinery will invoke loop.create_task(). Asyncio will then
    # run the coroutine in pieces, breaking it apart at async/await points,
    # and every time it will construct an appropriate callback and call
    # loop.call_soon(cb).
    #
    # If the job is a plain function, the end-user should call one of the
    # loop.call_*() methods directly.
    #

    # NOTE: For now, we do not support Python 3.7.'s `context` argument.
    # We disable the function argument check because this override fails in
    # pylint though using Python 3.7.
    # pylint: disable=arguments-differ

    def call_soon(self, callback, *args, context=None):
        """Schedule a callback to be called at the next iteration."""
        handle = asyncio.Handle(callback, args, self)
        self._immediate.append(handle)
        return handle

    def call_later(self, delay, callback, *args, context=None):
        """Schedule callback to be called after the given delay."""
        if delay < 0:
            raise RuntimeError("Can't schedule in the past")
        assert not math.isnan(delay)
        return self.call_at(self._time + delay, callback, *args)

    def call_at(self, when, callback, *args, context=None):
        """Schedule callback to be called at the given absolute timestamp."""
        if when < self._time:
            raise RuntimeError("Can't schedule in the past")
        assert not math.isnan(when)
        handle = asyncio.TimerHandle(when, callback, args, self)
        heapq.heappush(self._scheduled, handle)
        # XXX perhaps just for debugging in asyncio.TimerHandle?
        handle._scheduled = True
        return handle

    # pylint: enable=arguments-differ

    def create_task(self, coro):
        """Schedule the execution of a Coroutine. Return a Task object."""
        # Since this is a simulator, I'll run a plain simulated-time event
        # loop, and if there are any exceptions inside any coroutine I'll pass
        # them on to the event loop, so it can halt and print them out.
        # To achieve this, I need the exception to be caught in "async mode"
        # i.e. by a coroutine, and then use self._exc to pass it on to
        # "regular execution mode".
        async def wrapper():
            try:
                await coro
            except CancelledError:  # pylint: disable=try-except-raise
                # We do not want to intercept cancellation.
                raise
            except Exception as exc:  # pylint: disable=broad-except
                self._exc = exc
        return asyncio.Task(wrapper(), loop=self)

    def create_future(self):
        """Create an asyncio.Future object attached to the event loop."""
        # Not sure why this is here rather than in AbstractEventLoop.
        return asyncio.Future(loop=self)

    def get_debug(self):
        """Get the debug mode (bool) of the event loop."""
        return self._debug

    def set_debug(self, enabled):
        """Set the debug mode of the event loop."""
        self._debug = enabled
