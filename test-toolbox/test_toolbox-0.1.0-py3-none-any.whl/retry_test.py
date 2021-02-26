import unittest

from test_toolbox.retry import TimeoutSeconds, retry_until_pass_without_exception, \
    retry_until_returns_value
from test_toolbox.timer import Timer


class Test_retry_until_returns_value(unittest.TestCase):

    def test___function_returning_True_wait_for_True_very_short_timeout___expect_pass(self):
        def return_True() -> bool:
            return True

        callable_ = return_True
        return_value = True
        timeout: TimeoutSeconds = 0.0000000001
        retry_until_returns_value(callable_, return_value, timeout)

    def test___function_returning_False_wait_for_True_short_timeout___expect_TimeoutError_and_timeout_seconds_elapsed(
            self):
        def return_False() -> bool:
            return False

        callable_ = return_False
        return_value = True
        timeout: TimeoutSeconds = 0.1

        timer = Timer()
        with self.assertRaises(TimeoutError):
            retry_until_returns_value(callable_, return_value, timeout)

        actual_elapsed_seconds = timer.elapsed
        self.assertGreaterEqual(actual_elapsed_seconds, timeout)

    def test___function_returning_first_x_then_y_waiting_for_y__expect_two_calls_and_pass(self):
        actual_number_of_calls = 0

        incorrect_return_value = 'totally_wait_for_this_NOT'
        correct_return_value = 'totally_wait_for_this'

        def return_incorrect_then_correct() -> str:
            nonlocal actual_number_of_calls
            actual_number_of_calls += 1
            if actual_number_of_calls == 1:
                return incorrect_return_value
            elif actual_number_of_calls == 2:
                return correct_return_value
            else:
                raise AssertionError("Should never end up here")

        callable_ = return_incorrect_then_correct
        timeout: TimeoutSeconds = 1
        retry_until_returns_value(callable_, correct_return_value, timeout)

        expected_number_of_calls = 2
        self.assertEqual(expected_number_of_calls, actual_number_of_calls)


class CustomTestException(Exception):
    """
    Used in the tests for `retry_until_pass_without_exception`.
    """
    pass


class Test_retry_until_pass_without_exception(unittest.TestCase):

    def test___no_exception_raised_short_timeout___expect_one_function_call(self):
        actual_number_of_calls = 0

        def do_not_raise_an_exception() -> None:
            nonlocal actual_number_of_calls
            actual_number_of_calls += 1

        retry_until_pass_without_exception(do_not_raise_an_exception,
                                           timeout=0.0001)

        expected_number_of_calls = 1
        self.assertEqual(expected_number_of_calls, actual_number_of_calls)

    def test___exception_raised_medium_timeout___expect_exception_reraised_and_timeout_seconds_elapsed(
            self):
        def raise_an_exception() -> None:
            raise CustomTestException()

        timeout_seconds: TimeoutSeconds = 1.3

        timer = Timer()
        with self.assertRaises(CustomTestException):
            retry_until_pass_without_exception(
                raise_an_exception,
                timeout_seconds
            )

        actual_elapsed_seconds = timer.elapsed
        self.assertGreaterEqual(actual_elapsed_seconds, timeout_seconds)

    def test___two_times_exception_raised_then_pass_with_medium_timeout___expect_pass_and_three_function_calls(
            self):
        actual_number_of_calls = 0

        def pass_on_third_call() -> None:
            nonlocal actual_number_of_calls
            actual_number_of_calls += 1
            if actual_number_of_calls in (1, 2):
                raise CustomTestException()
            elif actual_number_of_calls == 3:
                pass
            else:
                raise AssertionError("Should never end up here")

        retry_until_pass_without_exception(pass_on_third_call, timeout=2.1)

        expected_number_of_calls = 3
        self.assertGreaterEqual(expected_number_of_calls,
                                actual_number_of_calls)
