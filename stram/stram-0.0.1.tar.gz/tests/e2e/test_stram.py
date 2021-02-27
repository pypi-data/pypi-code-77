import pytest
import numpy as np
from bunch import Bunch

from stram.utils.worklog import Worklog
from stram.utils.json_processing import Config
from stram.services.commander import get_orders
from stram.services.executor import execute_orders


@pytest.fixture(scope='function')
def worklog_in_progress(content_image, style_image):
    worklog = Worklog.new(content_image, style_image)
    worklog.add_work_unit(
        '231020b292c6225139a99c14a1d78f87830facd02ba5c37c07151bc6367dc6f2', {}
    )
    worklog.add_work_unit(
        'ea735cc99e9a82552881be8cdfae636c65b4abfb297153491495299a7f1b6ed8', {}
    )
    worklog.add_work_unit(
        'ea6c938370793f75cc45b310287bb3cdc5704d2a50cd47cbd997ed53bb2a7d68', {}
    )
    worklog.add_work_unit(
        '2c29eb63670a7b70df098605048bba210d91d48a0c82a9e5acee00e18f2f1abb', {}
    )
    yield worklog


@pytest.fixture(scope='module')
def full_config():
    config_1 = dict(
        method='gatys',
        max_iterations=10,
        early_stopping=dict(enabled=False),
        optimizer='Adam',
        optimizer_params=dict(beta_1=0.99, epsilon=1e-1),
        learning_rate_params=dict(
            decay_steps=5, initial_learning_rate=1.0, end_learning_rate=0.1, power=2.0
        ),
        content_layers=[dict(block2_conv1=1.0), dict(block2_conv2=1.0)],
        style_layers=dict(block1_conv1=0.5, block2_conv1=0.5),
        content_loss_weight=[1e4, 1e-5],
        style_loss_weight=1e-2,
        variation_loss_weight=30,
    )
    config_2 = dict(
        method='gatys',
        max_iterations=20,
        early_stopping=dict(enabled=True, delta=0.2, patience=5),
        optimizer='RMSprop',
        optimizer_params=dict(),
        learning_rate_params=dict(
            decay_steps=10, initial_learning_rate=1.0, end_learning_rate=0.01, power=1.0
        ),
        content_layers=dict(block2_conv1=1.0),
        style_layers=dict(block1_conv1=0.5, block2_conv1=0.5),
        content_loss_weight=[1e4, 1e-5],
        style_loss_weight=1e-2,
        variation_loss_weight=30,
    )
    config_3 = dict(
        method='yijun',
        style_bottom_layer=['block1_conv2', 'block2_conv2'],
        style_strength=0.5,
        smoothing_tool=['off', 'matting_affinity'],
        smoothing=dict(lambda_=1e-4, epsilon=1e-6, window_radius=1),
    )
    yield Config(configs=[config_1, config_2, config_3])


def test_orders_system_new_release(
    mock_release_env, content_image, style_image, full_config
):
    worklog = Worklog.new(content_image, style_image)
    orders = get_orders(content_image, style_image, full_config, worklog)
    style_products = execute_orders(content_image, style_image, orders)

    num_products = 0
    for product in style_products:
        assert isinstance(product.styling_hash, str)
        assert isinstance(product.styling_config, Bunch)
        assert product.synthesized_image.dtype == np.uint8
        assert product.synthesized_image.shape == content_image.shape
        num_products += 1

    assert num_products == 10


def test_orders_system_resume_debug(
    mock_debug_env, content_image, style_image, full_config, worklog_in_progress
):
    orders = get_orders(content_image, style_image, full_config, worklog_in_progress)
    style_products = execute_orders(content_image, style_image, orders)

    num_products = 0
    for product in style_products:
        assert isinstance(product.styling_hash, str)
        assert isinstance(product.styling_config, Bunch)
        assert product.synthesized_image.dtype == np.uint8
        assert product.synthesized_image.shape == content_image.shape
        num_products += 1

    assert num_products == 6
