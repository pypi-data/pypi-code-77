import platform

def _nullfunction(name: str):
    def nullfunction(*args, **kwargs):
        raise RuntimeError(f"Sorry, function `{name}` was not implemented for your platform.")
    return nullfunction

def _nullmethod(name: str):
    def nullmethod(*args, **kwargs):
        raise RuntimeError(f"Sorry, method `{name}` was not implemented for your platform.")
    return nullmethod

def _nullproperty(name: str):
    def nullproperty(*args, **kwargs):
        raise RuntimeError(f"Sorry, property `{name}` was not implemented for your platform.")
    return nullproperty

def _nullclass(name: str):
    class NullClass:
        
        NAME = name

        def __new__(cls, *args, **kwargs):
            raise RuntimeError(f"Sorry, class `{cls.NAME}` was not implemented for your platform.")

        def __init__(self, *args, **kwargs):
            raise RuntimeError(f"Sorry, class `{self.NAME}` was not implemented for your platform.")

        def __getattribute__(self, *args, **kwargs):
            raise RuntimeError(f"Sorry, class `{self.NAME}` was not implemented for your platform.")

        def __setattr__(self, *args, **kwargs):
            raise RuntimeError(f"Sorry, class `{self.NAME}` was not implemented for your platform.")

        def __getattr__(self, *args, **kwargs):
            raise RuntimeError(f"Sorry, class `{self.NAME}` was not implemented for your platform.")
    
    return NullClass

class OsWhich:

    LINUX = 'Linux'
    MACOSX = 'Darwin'
    WINDOWS = 'Windows'
    SOLARIS = 'Solaris'

    __table__ = {}

    def __init__(self, system: {str, callable}):
        """
        """
        if type(system) is str:
            self.__active = bool(system == platform.system())
        else:
            self.__active = bool(system(platform.system()))

    @property
    def cls(self):
        return self.__class__

    @property
    def active(self) -> bool:
        return self.__active

    @classmethod
    def _get_func_type_name(cls, callback: callable):
        if isinstance(callback, cls.t_method):
            return cls.t_method, callback.__qualname__
        elif isinstance(callback, cls.t_function):
            return cls.t_function, callback.__qualname__
        elif isinstance(callback, cls.t_property):
            return cls.t_property, callback.fget.__qualname__
        elif isinstance(callback, type):
            return type, callback.__qualname__
        else:
            raise TypeError(f"Invalid type {type(callback)}.")

    t_class = type
    t_method = type(_get_func_type_name)
    t_function = type(lambda : None)
    t_property = property

    def __bool__(self):
        return self.__active

    def __call__(self, callback: callable):
        type_, name_ = self._get_func_type_name(callback)
        if self.active:
            self.cls.__table__[name_] = callback
            return callback
        elif name_ in self.cls.__table__:
            return self.cls.__table__[name_]
        elif type_ is self.t_method:
            return _nullmethod(name_)
        elif type_ is self.t_function:
            return _nullfunction(name_)
        elif type_ is self.t_property:
            return _nullproperty(name_)
        elif type_ is self.t_class:
            return _nullclass(name_)
            
linux = OsWhich(OsWhich.LINUX)
macosx = OsWhich(OsWhich.MACOSX)
windows = OsWhich(OsWhich.WINDOWS)
solaris = OsWhich(OsWhich.SOLARIS)