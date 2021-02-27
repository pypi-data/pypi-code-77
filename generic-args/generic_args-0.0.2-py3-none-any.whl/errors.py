from dataclasses import dataclass
from typing import Any

from documented import DocumentedError


@dataclass
class TypeArgsError(DocumentedError):   # type: ignore
    """
    Cannot ascertain type arguments from instance or class.

    Object: {self.instance}
    """

    instance: Any   # type: ignore
