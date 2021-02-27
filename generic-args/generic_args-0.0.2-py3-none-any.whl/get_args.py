from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    # This one is always available.
    from typing_inspect import get_args

else:  # pragma: no cover
    try:
        # For Python >= 3.8: use the method from standard library.
        # https://docs.python.org/3/library/typing.html#typing.get_args
        from typing import get_args
    except ImportError:
        # For older versions, rely upon typing_inspect.
        # https://github.com/ilevkivskyi/typing_inspect
        from typing_inspect import get_args
