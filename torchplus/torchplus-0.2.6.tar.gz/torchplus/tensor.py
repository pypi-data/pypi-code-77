#! python3.8 -u
#  -*- coding: utf-8 -*-

##############################
## Project PyCTLib
## Package torchplus
##############################

__all__ = """
    set_autodevice
    unset_autodevice
    to_device
    Tensor
""".split()

try:
    import torch
    import numpy as np
except ImportError:
    raise ImportError("'pyctlib.torchplus' cannot be used without dependency 'torch' and 'numpy'.")
# import torch.nn as nn
import typing
import inspect
import builtins
from pyoverload import *
from pyctlib import raw_function, return_type_wrapper, touch, recursive_apply, vector
from functools import wraps
from typing import Union
# from types import GeneratorType
from .device import AutoDevice as Device

import sys
from pyctlib.visual.debugger import profile
"""
from torchplus import Tensor
import torchplus as tp
"""

_auto_device = True

def set_autodevice(flag=True):
    global _auto_device
    _auto_device = flag

def unset_autodevice():
    global _auto_device
    _auto_device = False

def to_device(obj, device=Device):
    return recursive_apply(obj, lambda x: x.to(device))

def return_tensor_wrapper(*args_out):
    def output_wrapper(func, auto_device=_auto_device):
        func = raw_function(func)
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not auto_device:
                return result
            else:
                return to_device(result)
        return wrapper

    if len(args_out) == 1 and (args_out[0] == True or args_out[0] == False):
        return lambda func: output_wrapper(func, args_out[0])
    else:
        return output_wrapper(args_out[0])

def _replace_key_with_sequence(original, sequence, key=-1):
    sequence = list(sequence)
    assert original.count(key) == len(sequence)
    result = list()
    index = 0
    for t in original:
        if t == key:
            result.append(sequence[index])
            index += 1
        else:
            result.append(t)
    return original.__class__(result)

def _replace_sequence_with_key(original, sequence, key=-1):
    sequence = list(sequence)
    result = list()
    index = 0
    for t in original:
        if index < len(sequence) and t == sequence[index]:
            result.append(key)
            index += 1
        else:
            result.append(t)
    assert index == len(sequence)
    return original.__class__(result)

_create_tensor_function = vector(['arange', 'tensor', 'as_tensor', 'bartlett_window', 'blackman_window', 'empty', 'empty_meta', 'eye', 'hamming_window', 'hann_window', 'kaiser_window', 'ones', 'rand', 'randn', 'randperm', 'scalar_tensor', 'sparse_coo_tensor', 'zeros'])

template = "@return_tensor_wrapper\ndef {key}(*args, **kwargs): return torch.{key}(*args, **kwargs)"

for func in _create_tensor_function:
    exec(template.format(key=func))
    __all__.append(func)

Tensor = torch.Tensor
