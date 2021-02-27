from dataclasses import dataclass

from jeeves.commands.find_packages import FindPackages
from jeeves.commands.subprocess import Subprocess


@dataclass
class Mypy(Subprocess):
    """Check types in code with mypy."""

    __name__ = 'mypy'

    # FIXME remove this dependency
    directories: FindPackages

    def __call__(self):
        """Run flahekell."""
        self.run('mypy', *self.directories())
