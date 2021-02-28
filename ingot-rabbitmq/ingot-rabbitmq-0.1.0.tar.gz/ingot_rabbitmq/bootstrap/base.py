from logging import getLogger

from ingots.bootstrap.base import BaseBuilder

import ingot_rabbitmq as package

__all__ = ("IngotRabbitmqBaseBuilder",)


logger = getLogger(__name__)


class IngotRabbitmqBaseBuilder(BaseBuilder):

    package = package
