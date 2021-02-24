import random
from .random_helpers import set_seed


def mutate_param_state(param, gaconf):
    param_copy = {**param}
    for k, var in gaconf.items():
        if var['type'] == 'number':
            r = random.randrange(-var['step'], var['step'])
        elif var['type'] == 'float':
            r = 2 * (random.random()-0.5) * var['step']
        else:
            raise ValueError('Invalid var type')
        if r == 0:
            continue
        print(r)
        new_val = param[k] + r
        new_val = min(new_val, var['max']) if var['max'] is not None else new_val
        new_val = max(new_val, var['min']) if var['min'] is not None else new_val
        param_copy[k] = new_val
    return param_copy
