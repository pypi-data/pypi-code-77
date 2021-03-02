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
            params:awk = superclass_filtermethod(self, *args, **kwargs)
            return subclass_method(self, *params.args, **params.kwargs)
        
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