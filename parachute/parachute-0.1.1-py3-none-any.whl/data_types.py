import re
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List


@dataclass(order=True)
class Parameter:
    """Represent a MAVLink parameter."""

    value: Any
    index: int
    type: int

    def __post_init__(self):
        # Convert the value according to the type:
        # https://mavlink.io/en/messages/common.html#MAV_PARAM_TYPE
        if 1 <= self.type <= 8:
            self.value = int(self.value)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "index": self.index,
            "type": self.type,
        }


@dataclass()
class Backup:
    """Represent an entire backup file."""

    status: List[str] = field(default_factory=list)
    schema: int = 1
    timestamp: datetime = field(default_factory=datetime.now)
    parameters: Dict[str, Parameter] = field(default_factory=dict)

    @property
    def status_str(self) -> str:
        """Construct a status comment string from a list of status messages."""
        if not self.status:
            return ""
        return "// " + "\n// ".join(self.status) + "\n\n"

    @classmethod
    def from_dict(cls, d) -> "Backup":
        d["timestamp"] = datetime.fromisoformat(d["timestamp"])
        d["parameters"] = {
            name: Parameter(**data) for name, data in d["parameters"].items()
        }
        backup = cls(**d)
        return backup

    def as_dict(self) -> Dict[str, Any]:
        return {
            "schema": self.schema,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
            "parameters": {
                name: param.as_dict() for name, param in sorted(self.parameters.items())
            },
        }

    def filter(self, regex) -> None:
        """
        Filter parameters based on a regex.

        Modifies the backup in-place.
        """
        r = re.compile(regex, re.IGNORECASE)
        self.parameters = {
            name: param for name, param in self.parameters.items() if r.search(name)
        }
