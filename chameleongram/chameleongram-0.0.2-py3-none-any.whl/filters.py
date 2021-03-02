from typing import Callable


class Filter:
    func: Callable

    def __add__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)

    def __call__(self, update, client: "chameleongram.Client" = None):
        try:
            return self.func(update)
        except TypeError:
            return self.func(update, client)

    __radd__ = __and__ = __add__


class Not(Filter):
    def __init__(self, flt):
        self.flt = flt

    def __call__(self, update, client: "chameleongram.Client" = None):
        return not (self.flt(update, client) if client else self.flt(update))


class And(Filter):
    def __init__(self, flt, other):
        self.flt = flt
        self.other = other

    def __call__(self, update, client: "chameleongram.Client" = None):
        return (
            (self.flt(update, client) and self.other(update, client))
            if client
            else (self.flt(update) and self.other(update))
        )


class Or(Filter):
    def __init__(self, flt, other):
        self.flt = flt
        self.other = other

    def __call__(self, update, client: "chameleongram.Client" = None):
        return (
            (self.flt(update, client) or self.other(update, client))
            if client
            else (self.flt(update) or self.other(update))
        )


class Filters:
    def __and__(self): ...

    def __or__(self): ...

    def __invert__(self): ...

    @staticmethod
    def create(func, client: "chameleongram.Client" = None):
        return type(
            "filter",
            (Filter,),
            {
                "func": (lambda self, update, _client: func(_client, update))
                if client is not None
                else (lambda self, update: func(update)),
                "__add__": Filter.__add__,
            },
        )()

    # private = create(lambda msg: msg.chat.type == "private")
    # group = create(lambda msg: msg.chat.type in ["group", "supergroup"])
    # channel = create(lambda msg: msg.chat.type == "channel")
