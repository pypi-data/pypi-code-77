"""
chatrelater.serialization
~~~~~~~~~~~~~~~~~~~~~~~~~

Serialization of chat log analysis results as JSON.

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Tuple


def serialize_data_to_file(data: Dict[str, Any], filename: Path) -> None:
    """Serialize data to file."""
    with filename.open('w') as f:
        json.dump(data, f)


def serialize_data_to_stdout(data: Dict[str, Any]) -> None:
    """Serialize data to STDOUT."""
    json.dump(data, sys.stdout)


def load_data(
    filename: Path,
) -> Tuple[List[str], List[Tuple[str, str, int]], bool]:
    """Import data from file."""
    with filename.open() as f:
        d = json.load(f)

    return d['nicknames'], d['relations'], d['directed']
