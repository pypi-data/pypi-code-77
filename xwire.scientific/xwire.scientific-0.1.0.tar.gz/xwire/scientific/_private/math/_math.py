import math


def log_return(initial: float, final: float, period: float, decimals=None) -> float:
    return_value = math.log(final/initial) / period
    if decimals is not None:
        return round(return_value, decimals)
    else:
        return return_value
