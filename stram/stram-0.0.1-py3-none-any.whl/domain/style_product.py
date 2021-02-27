import numpy as np
from bunch import Bunch
from dataclasses import dataclass


@dataclass
class StyleProduct:
    styling_hash: str
    styling_config: Bunch
    synthesized_image: np.ndarray
