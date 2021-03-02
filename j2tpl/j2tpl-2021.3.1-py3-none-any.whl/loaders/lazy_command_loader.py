from importlib import import_module
from pkgutil import iter_modules
from typing import Callable
from typing import List
from typing import Type

from cleo.commands.command import Command
from cleo.loaders.factory_command_loader import FactoryCommandLoader


class LazyCommandLoader(FactoryCommandLoader):
    def __init__(self, package: str) -> None:
        module = import_module(".console.commands", package)

        super(LazyCommandLoader, self).__init__(
            {
                name: self._load_command("{}.{}".format(module.__name__, name))
                for finder, name, ispkg in iter_modules(module.__path__)
            }
        )

    def _load_command(self, name: str) -> Callable:
        def _load() -> Type[Command]:
            command_class = getattr(import_module(name), "Command")
            return command_class()

        return _load
