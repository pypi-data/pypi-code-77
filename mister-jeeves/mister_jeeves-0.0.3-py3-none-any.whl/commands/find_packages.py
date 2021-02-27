from dataclasses import dataclass
from typing import List

import setuptools


@dataclass
class FindPackages:
    """Find Python packages in current directory."""

    def __call__(self) -> List[str]:
        """Use Setuptools."""
        return list(filter(
            lambda package_name: '.' not in package_name,
            setuptools.find_packages(),
        ))
