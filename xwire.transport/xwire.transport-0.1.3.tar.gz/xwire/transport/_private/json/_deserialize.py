from dataclasses import fields
from typing import TypeVar, Type, Dict, Any, get_origin, get_args

from xwire.common import decorator_utils

from xwire.transport._private.decorators import serializable
from xwire.transport._private.exceptions import DeserializationError


T = TypeVar('T')


def deserialize(json: Dict[str, Any], target: Type[T]) -> T:
    if not decorator_utils.has_decorator(target, serializable):
        raise DeserializationError('Target must be decorated with @xwire.serializable in order to be deserialized to')
    else:
        deserialized = {}
        for field in fields(target):
            if get_origin(field.type) is list and decorator_utils.has_decorator(get_args(field.type)[0], serializable):
                deserialized[field.name] = [deserialize(item, get_args(field.type)[0]) for item in json[field.name]]
            elif decorator_utils.has_decorator(field.type, serializable):
                deserialized[field.name] = deserialize(json[field.name], field.type)
            else:
                deserialized[field.name] = json[field.name]

        return target(**deserialized)
