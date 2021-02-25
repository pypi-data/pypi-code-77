"""Mars 2020 - Perseverance database module"""

from pathlib import Path

from .db import RoverDatabase

HERE = Path(__file__).parent

Mars2020 = RoverDatabase(HERE / 'mars2020.db', 'mars2020')
