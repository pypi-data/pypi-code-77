import typing as t
from logging import getLogger
from logging import INFO

from ingots.scripts.base import BaseDispatcher
from ingots.utils.logging import configure_startup_logging

if t.TYPE_CHECKING:
    from ingots.scripts.base import BaseEntryPoint  # noqa


__all__ = (
    "IngotRabbitmqDispatcher",
    "main",
)


configure_startup_logging(
    default_level=INFO,
    format="%(levelname)s: %(message)s",
)
logger = getLogger(__name__)


class IngotRabbitmqDispatcher(BaseDispatcher):

    prog = "ingot_rabbitmq"
    description = "The Ingot Rabbitmq management CLI."
    entry_points_classes: t.List[t.Type["BaseEntryPoint"]] = []


def main():
    dispatcher = IngotRabbitmqDispatcher.build()
    dispatcher.run()


if __name__ == "__main__":
    main()
