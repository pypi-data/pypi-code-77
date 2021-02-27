import pytest

from stram.services.method_factory import create_method
from stram.utils.exceptions import InvalidOrderException
from stram.domain.methods.gatys_method import GatysMethod


def test_create_method_success():
    method = create_method('gatys')
    assert isinstance(method, GatysMethod)


def test_create_method_failure():
    with pytest.raises(InvalidOrderException):
        create_method('unknown_method')
