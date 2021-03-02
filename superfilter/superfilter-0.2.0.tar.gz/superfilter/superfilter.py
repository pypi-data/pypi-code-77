from argskwargs import argskwargs as awk
import inspect

# Method decorator
class filtermethod:
    def __init__(self, function):
        self.function = function
    
    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

# Class decorator
def filterclass(cls):
    def create_replacement_method(superclass_filtermethod, subclass_method):
        def call(self, *args, **kwargs):
            params = superclass_filtermethod(self, *args, **kwargs)

            if isinstance(params, awk):
                args = params.args
                kwargs = params.kwargs
            elif isinstance(params, dict):
                args = list()
                kwargs = params
            else:
                try:
                    args = list(params)
                except TypeError:
                    args = [params]
                finally:
                    kwargs = dict()

            return subclass_method(self, *args, **kwargs)
        
        return call

    superclass = cls

    class FC(cls):
        def __init_subclass__(cls, **kwargs):
            subclass = cls

            superclass_filtermethods:dict = dict(inspect.getmembers(superclass, predicate=lambda x: type(x) == filtermethod))
            subclass_methods:dict = dict(inspect.getmembers(subclass, predicate=inspect.isfunction))

            for name, superclass_filtermethod in superclass_filtermethods.items():
                if (name in subclass_methods):
                    subclass_method = subclass_methods[name]

                    replacement_subclass_method = create_replacement_method(superclass_filtermethod, subclass_method)

                    setattr(subclass, name, replacement_subclass_method)
    
    return FC