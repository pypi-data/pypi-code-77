from __future__ import annotations
from typing import Callable, Sequence, TYPE_CHECKING
import functools
if TYPE_CHECKING:
    from .build import BuildStepCallable

def split_step_name(name: str, new = ' ', old='_'):
    return name.replace(old, new).capitalize()

def print_step_name(formatter=split_step_name, args: Sequence=()):
    """Gets a decorator that formats the name of the build step and prints it"""
    fmt_args = args
    def format_step_name(func: Callable):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            print(formatter(func.__name__, *fmt_args))
            return func(*args, **kwargs)
        return decorated
    return format_step_name

def print_step_doc():
    def decorate_with(func: Callable):
        @functools.wraps(func)
        def output_func_doc(*args, **kwargs):
            print(func.__doc__)
            return func(*args, *kwargs)
        return output_func_doc
    return decorate_with

def composed(*decorators: BuildStepCallable) -> BuildStepCallable:
    """
    Used to compose a decorator. Useful for defining specific
    outputs and progress reports to a build step and resusing
    """
    def decorated(func: BuildStepCallable):
        for decorator in reversed(decorators):
            func = decorator(func)
        return func
    return decorated
