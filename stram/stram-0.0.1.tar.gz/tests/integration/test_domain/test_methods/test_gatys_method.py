import pytest
import numpy as np
from stram.utils.json_processing import Config
from stram.domain.methods.gatys_method import GatysMethod


@pytest.fixture(scope='module')
def config():
    yield Config(
        method='gatys',
        max_iterations=10,
        early_stopping=dict(enabled=True, delta=0.1, patience=5),
        optimizer='Adam',
        optimizer_params=dict(beta_1=0.99, epsilon=1e-1),
        learning_rate_params=dict(
            decay_steps=8, initial_learning_rate=1.0, end_learning_rate=0.1, power=2.0
        ),
        content_layers=dict(block2_conv2=1.0),
        style_layers=dict(block1_conv2=0.5, block2_conv2=0.5),
        content_loss_weight=1.0,
        style_loss_weight=0.01,
        variation_loss_weight=0.1,
    )


def test_method_str():
    method = GatysMethod()
    assert str(method) == 'gatys'


def test_method_in_debug_mode(mock_debug_env, content_image, style_image, config):
    method = GatysMethod()
    method.set_up(content_image, style_image, config)
    method.process(config)

    synthesized_image = method.get_synthesized_image()
    assert synthesized_image.shape == content_image.shape
    assert synthesized_image.dtype == np.uint8


def test_method_in_release_mode(mock_release_env, content_image, style_image, config):
    method = GatysMethod()
    method.set_up(content_image, style_image, config)
    method.process(config)

    synthesized_image = method.get_synthesized_image()
    assert synthesized_image.shape == content_image.shape
    assert synthesized_image.dtype == np.uint8
