import typing as t
from unittest import TestCase

from ingots.tests.units.bootstrap.test_base import BaseBuilderTestsMixin

from ingot_rabbitmq.bootstrap import IngotRabbitmqBaseBuilder

__all__ = ("IngotRabbitmqBaseBuilderTestsMixin",)


class IngotRabbitmqBaseBuilderTestsMixin(BaseBuilderTestsMixin):
    """Contains tests for the IngotRabbitmqBuilder class."""

    tst_cls: t.Type = IngotRabbitmqBaseBuilder


class IngotRabbitmqBaseBuilderTestCase(IngotRabbitmqBaseBuilderTestsMixin, TestCase):
    """Checks the IngotRabbitmqBuilder class."""
