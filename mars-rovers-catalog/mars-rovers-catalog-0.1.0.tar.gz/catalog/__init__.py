"""Mars Rovers Catalog module."""

from .database import Mars2020
from .version import __version__


__all__ = [
    'Mars2020',
    '__version__',
]
