class traxexException(Exception):
    """ Base exception class for scathach.py """

    pass


class NothingFound(traxexException):
    """ The API didn't return anything """

    pass


class EmptyArgument(traxexException):
    """ When no target is defined """

    pass


class InvalidArgument(traxexException):
    """ Invalid argument within the category """

    pass
