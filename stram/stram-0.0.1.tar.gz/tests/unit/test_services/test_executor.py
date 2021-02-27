import pytest
import logging
import numpy as np
from unittest.mock import patch

from stram.utils.json_processing import Config
from stram.utils.exceptions import InvalidOrderException
from stram.services.executor import execute_orders
from stram.domain.methods.base_method import BaseMethod


@pytest.fixture(scope='function')
def concrete_method():
    class ConcreteMethodMock(BaseMethod):
        def set_up(self, content_image, style_image, config):
            self.image_shape = content_image.shape
            self.image_dtype = style_image.dtype

        def process(self, config):
            self.synthesized_image = np.zeros(self.image_shape, dtype=self.image_dtype)

        def get_synthesized_image(self):
            return self.synthesized_image

    yield ConcreteMethodMock


@pytest.fixture(scope='function')
def create_method_mock(concrete_method):
    def create_method_mock_function(method_name):
        methods_dict = dict(method_A=concrete_method)
        try:
            return methods_dict[method_name]()
        except KeyError:
            raise InvalidOrderException(f'Method {method_name} does not exist')

    yield create_method_mock_function


@pytest.fixture(scope='function')
def orders():
    yield dict(
        styling_hash_1=Config(method='method_A', strength=0.5),
        styling_hash_2=Config(method='method_B', precision=0.225),
    )


def test_execute_orders(caplog, content_image, style_image, orders, create_method_mock):
    with patch('stram.services.executor.create_method', side_effect=create_method_mock):
        with caplog.at_level(logging.ERROR):
            product_was_received = False
            products = execute_orders(content_image, style_image, orders)

            for product in products:
                product_was_received = True
                assert isinstance(product.styling_hash, str)
                assert isinstance(product.synthesized_image, np.ndarray)
                assert product.styling_config.method == 'method_A'
                assert product.styling_config.strength == 0.5

        assert product_was_received
        assert 'Method method_B does not exist. Order is skipped' in caplog.text
