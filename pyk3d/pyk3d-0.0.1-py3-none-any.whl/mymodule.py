"""Stub module"""

from typing import Any


def get_class_name(obj: Any) -> str:
    """Get the class name of object

    Running tests after adding breakpoints should allow the user
    to step through the various statements.
    """
    obj_type = type(obj)
    name = obj_type.__name__
    return name
