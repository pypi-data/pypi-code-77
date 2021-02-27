from typing import Any, Iterator, Tuple

from generic_args.errors import TypeArgsError
from generic_args.get_args import get_args


def iterate_by_type_parameters(  # type: ignore
    instance: Any,
) -> Iterator[Tuple[type, ...]]:
    """Iterate over classes in MRO and yield type parameters for each."""
    try:
        yield get_args(instance.__orig_class__)   # noqa: WPS609
    except AttributeError:
        pass   # noqa: WPS420

    try:
        yield from map(
            get_args,
            instance.__orig_bases__,  # noqa: WPS609
        )
    except AttributeError:
        pass   # noqa: WPS420

    instance_args = get_args(instance)
    if instance_args:
        yield instance_args


def generic_type_args(instance: Any) -> Tuple[type, ...]:  # type: ignore
    """Get type parameters given a class instance."""
    try:
        type_parameters, *etc = iterate_by_type_parameters(instance)
    except ValueError:
        raise TypeArgsError(instance=instance)

    return type_parameters
