import json

from pathlib import Path
from typing import Any
from typing import Dict


class JsonParser:
    def __init__(self) -> None:
        pass

    def parse_file(self, path: Path) -> Dict[str, Any]:
        d = {}
        with open(path, "r") as f:
            d = json.loads(f.read())
        return d
