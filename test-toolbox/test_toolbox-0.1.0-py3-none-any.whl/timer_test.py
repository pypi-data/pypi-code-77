import time
import unittest

from test_toolbox.timer import Timer


class TestTimer(unittest.TestCase):

    def test___access_elapsed_time___expect_is_greater_equal_zero(self):
        timer = Timer()
        actual_elapsed = timer.elapsed
        self.assertGreaterEqual(actual_elapsed, 0.0)

    def test___sleep_between_accessing_elapsed___expect_second_elapsed_is_at_least_sleep_time_greater(
            self):
        timer = Timer()

        sleep_time_sec = 0.1

        elapsed_before_sleep = timer.elapsed
        time.sleep(sleep_time_sec)
        elapsed_after_sleep = timer.elapsed

        self.assertGreaterEqual(elapsed_after_sleep, elapsed_before_sleep + sleep_time_sec)
