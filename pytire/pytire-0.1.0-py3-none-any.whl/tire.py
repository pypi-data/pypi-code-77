"""
:author: Alex Robinson <girotobial@gmail.com>
:copyright: Copyright (c) Alex Robinson, 2021-2021.
:license: MIT
"""

import re
from typing import Optional

from .constant import DIAMETER_RE, METRIC_RE, WHEEL_DIAMETER_RE, WIDTH_RE
from .enums import Unit
from .util import convert_length


class Tire:
    """A rubber pneumatic tire.

    Attributes
    ----------
    size : str
        Size code as would be displayed on the sidewall.
        E.g 'H45.5x16.5-21', '30x10.75-16', '615x225-10'
    diameter : float
        Outer diameter in metres
    width : float
        width in metres
    wheel_diameter : float
        inner diameter in metres
    """

    def __init__(self, size: str):
        """A rubber pneumatic tire.

        Parameters
        ----------
        size : str
            Size code as would be displayed on the sidewall.
            E.g 'H45.5x16.5-21', '30x10.75-16', '615x225-10'
        """
        self.size = size
        self.unit = Unit.MILLIMETRE if re.match(METRIC_RE, self.size) else Unit.INCH

    @property
    def diameter(self) -> Optional[float]:
        """Tire diameter in metres"""

        match = re.search(DIAMETER_RE, self.size)

        if match is None:
            return match

        diameter = float(match.group(0))
        return convert_length(diameter, self.unit, Unit.METRE)

    @property
    def width(self) -> Optional[float]:
        """Tire width in metres"""

        match = re.search(WIDTH_RE, self.size)
        if match is None:
            return match

        width = float(match.group(0))
        return convert_length(width, self.unit, Unit.METRE)

    @property
    def wheel_diameter(self) -> Optional[float]:
        """Wheel diameter in metres"""

        match = re.search(WHEEL_DIAMETER_RE, self.size)
        if match is None:
            return match

        wheel_diameter = float(match.group(0))
        return convert_length(wheel_diameter, Unit.INCH, Unit.METRE)
