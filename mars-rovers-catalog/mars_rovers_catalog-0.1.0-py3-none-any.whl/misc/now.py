"""Miscellaneous now module."""

from datetime import datetime as dt


def now():
    """Get time in ISO format."""
    return dt.now().isoformat()[:-7]
