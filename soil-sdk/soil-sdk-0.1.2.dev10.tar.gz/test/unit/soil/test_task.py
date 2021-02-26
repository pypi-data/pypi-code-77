# pylint: disable=missing-docstring,no-self-use,line-too-long, unused-argument
# type: ignore

import unittest
from unittest.mock import MagicMock
from soil import task


class TestTask(unittest.TestCase):
    def test_task(self):
        mock_module = MagicMock()
        mock_module.return_value = 'ok'
        tasked = task(mock_module)
        assert tasked(1, 2, 3, a=2, b=3) == 'ok'
        mock_module.assert_called_once_with(1, 2, 3, a=2, b=3)
