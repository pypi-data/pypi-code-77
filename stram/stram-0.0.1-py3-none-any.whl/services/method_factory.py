from stram.utils.exceptions import InvalidOrderException
from stram.domain.methods.gatys_method import GatysMethod
from stram.domain.methods.yijun_method import YijunMethod


def create_method(method_name):
    """
    Instantiate a method object

    Args:
        method_name (str): name of the method
    Return:
        method_object (BaseMethod): an object of the desired method class
    """
    methods_dict = dict(gatys=GatysMethod, yijun=YijunMethod)

    try:
        return methods_dict[method_name]()
    except KeyError:
        raise InvalidOrderException(f'Method {method_name} does not exist')
