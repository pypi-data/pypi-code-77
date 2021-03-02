"""Utilities."""
from typing import Dict, Any


def get_interval_unit(interval: int) -> str:
    """Get interval unit.

    :param interval:
    :return:
    """
    return "seconds" if interval > 1 else "seconds"


def clean_args(arguments) -> Dict[str, Any]:
    """Clean argumetns. Remove None values.

    :param arguments:
    :return:
    """
    return {key: val for key, val in arguments.items() if val is not None}
