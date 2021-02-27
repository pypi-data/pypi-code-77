import pytest
import numpy as np
from stram.utils.json_processing import Config
from stram.domain.methods.yijun_method import YijunMethod


@pytest.fixture(scope='module')
def config_1():
    yield Config(
        method='yijun',
        style_bottom_layer='block3_conv2',
        style_strength=0.8,
        smoothing_tool='matting_affinity',
        smoothing=dict(lambda_=1e-4, epsilon=1e-6, window_radius=1),
    )


@pytest.fixture(scope='module')
def config_2():
    yield Config(
        method='yijun',
        style_bottom_layer='block2_conv2',
        style_strength=0.5,
        smoothing_tool='guided_filter',
        smoothing=dict(epsilon=3, window_radius=5),
    )


def test_method_str():
    method = YijunMethod()
    assert str(method) == 'yijun'


def test_method_in_debug_mode(mock_debug_env, content_image, style_image, config_1):
    method = YijunMethod()
    method.set_up(content_image, style_image, config_1)
    method.process(config_1)

    synthesized_image = method.get_synthesized_image()
    assert synthesized_image.shape == content_image.shape
    assert synthesized_image.dtype == np.uint8


def test_method_in_release_mode(mock_release_env, content_image, style_image, config_2):
    method = YijunMethod()
    method.set_up(content_image, style_image, config_2)
    method.process(config_2)

    synthesized_image = method.get_synthesized_image()
    assert synthesized_image.shape == content_image.shape
    assert synthesized_image.dtype == np.uint8
