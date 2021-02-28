import typing as t
from unittest import TestCase

from ingots.tests.units.scripts.test_base import BaseDispatcherTestsMixin

from ingot_rabbitmq.scripts.ingot_rabbitmq import IngotRabbitmqDispatcher

__all__ = ("IngotRabbitmqDispatcherTestsMixin",)


class IngotRabbitmqDispatcherTestsMixin(BaseDispatcherTestsMixin):
    """Contains tests for the IngotRabbitmqDispatcher class and checks it."""

    tst_cls: t.Type = IngotRabbitmqDispatcher
    tst_builder_name = "test"


class IngotRabbitmqDispatcherTestCase(IngotRabbitmqDispatcherTestsMixin, TestCase):
    """Checks the IngotRabbitmq class."""
