import yaml

from pathlib import Path
from typing import Any
from typing import Dict


class YamlParser:
    def __init__(self) -> None:
        pass

    def parse_file(self, path: Path) -> Dict[str, Any]:
        d = {}
        with open(path, "r") as f:
            d = yaml.safe_load(f.read())
        return d
