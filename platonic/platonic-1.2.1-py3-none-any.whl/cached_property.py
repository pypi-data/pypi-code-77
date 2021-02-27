import typing

if typing.TYPE_CHECKING:  # pragma: no cover
    from backports.cached_property import cached_property

else:  # pragma: no cover
    try:
        from functools import cached_property
    except ImportError:
        from backports.cached_property import cached_property
