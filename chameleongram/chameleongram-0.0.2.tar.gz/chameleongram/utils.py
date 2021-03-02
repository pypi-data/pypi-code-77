import json
from typing import Union


def get_json(value: "chameleongram.raw.TL", as_string: bool = True) -> Union[dict, str]:
    values = {"_": value.__class__.__qualname__}

    for k, v in value.__dict__.items():
        if isinstance(v, bytes):
            values[k] = str(v)
        elif issubclass(type(v), value.__class__.__bases__[0]):
            values[k] = get_json(v, False)
        elif isinstance(v, list) and len(v) > 0:
            if isinstance(v[0], bytes):
                values[k] = [str(list_v) for list_v in v]
            elif issubclass(type(v[0]), value.__class__.__bases__[0]):
                values[k] = [get_json(list_v, False) for list_v in v]
            else:
                values[k] = v
        else:
            values[k] = v
    return json.dumps(values, indent=4) if as_string else values


class DC:
    production = {
        1: "149.154.175.50",
        2: "149.154.167.51",
        3: "149.154.175.100",
        4: "149.154.167.91",
        5: "91.108.56.149",
    }

    testmode = {1: "149.154.175.10", 2: "149.154.167.40", 3: "149.154.175.117"}

    def __new__(cls, dc_id: int, test: bool):
        return cls.testmode[dc_id] if test else cls.production[dc_id]


class asyncrange:
    class __asyncrange:
        def __init__(self, *args):
            self.__iter_range = iter(range(*args))

        async def __anext__(self):
            try:
                return next(self.__iter_range)
            except StopIteration as e:
                raise StopAsyncIteration(str(e))

    def __init__(self, *args):
        self.__args = args

    def __aiter__(self):
        return self.__asyncrange(*self.__args)
