''' Package for soil.task '''
from typing import Callable, Any, List
from soil.data_structure import DataStructure


def task(modulified_module: Callable) -> Callable:
    '''
    Decorates a modulified module in soil. This function is to call
    soil modules from other soil modules.
    Example:
        task(my_module)(data, arg1='val1')
    '''
    def decorator(*args: DataStructure, **kwargs: Any) -> List[DataStructure]:
        return modulified_module(*args, **kwargs)
    return decorator
