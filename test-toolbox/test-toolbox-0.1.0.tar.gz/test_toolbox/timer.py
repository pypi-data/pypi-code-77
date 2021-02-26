import time

now = time.time


class Timer:
    """
    Tacks the time elapsed since instantiation.
    """

    def __init__(self):
        self._start = now()

    @property
    def elapsed(self) -> float:
        """
        Returns the time elapsed since instantiation in seconds.
        """
        return now() - self._start
