from .structure import Structure, Box, Sphere, Cylinder, PolySlab, GdsSlab
from .source import (Source, VolumeSource, PointDipole, PlaneSource,
                        PlaneWave, ModeSource, SourceTime, GaussianPulse)
from .monitor import Monitor, TimeMonitor, FreqMonitor, ModeMonitor
from .grid import Grid
from .material import Medium
from .dispersion import DispersionModel, Sellmeier
from .utils.em import dft_spectrum, poynting_flux
from .utils.log import logging_default, logging_level, logging_file

from . import material
PEC = material.PEC()
PMC = material.PMC()

from .simulation import Simulation
from .constants import C_0, ETA_0, EPSILON_0, MU_0, inf

import logging
logging_default()

logging.warning("!! The tidy3dclient package is deprecated and has been renamed to tidy3d. "
                "To stay up to date, please 'pip uninstall tidy3dclient' and 'pip install tidy3d'. !!")