import operator
from itertools import groupby
from typing import List


def group_by_key(items: List[dict], key: 'the_dict_key') -> dict:
    """group a dict list by the given dict key

    :param items: List[ dict ]
    :param key: the_dict_key
    :return: dict{ key: List[ the_dict_value ] }
    """
    # return {i[key]: [j for j in items if j[key] == i[key]] for i in items}

    return {i[0]: i[1] for i in groupby(items, operator.attrgetter(key))}


def id_by_key(items: List[dict], key: 'the_dict_key') -> dict:
    """unique a dict list by the given dict key and reserved the last

    :param items: List[ dict ]
    :param key: the_dict_key
    :return: dict{ key: the_dict_value }
    """
    return {i[key]: i for i in items}


def list_get(items: list, index: int) -> object:
    """ 不在索引范围内的，返回None，不抛异常 """
    size = len(items)
    ret = items[index] if -size <= index < size else None
    return ret
