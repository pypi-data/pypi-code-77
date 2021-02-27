import pytest
import numpy as np

from stram.utils.worklog import Worklog
from stram.utils.json_processing import Config
from stram.utils.exceptions import InvalidOrderException
from stram.services.commander import (
    get_orders,
    variation_dict_to_styling_configs,
    get_styling_configs_with_no_duplicates,
)


@pytest.fixture(scope='function')
def styling_configs_list():
    yield [
        [Config(b1='B1', b2=2.0, b3=False), Config(b1='Z3', b2=2.5, b3=False)],
        [Config(b1='B1', b2=2.0, b3=False), Config(b1='Z4', b2=15.0, b3=True)],
        [Config(b1='D1', b2=0, b3=False), Config(b1='D1', b2=0, b3=False)],
    ]


@pytest.fixture(scope='module')
def full_config():
    var_dict_1 = dict(a1='a1', a2=10, a3=0.5, a4=[0, 1, 2], a5=['way_1', 'way_2'])
    var_dict_2 = dict(a1='a1', a2=[10, 20], a3=0.5, a4=[0, 1], a5='way_1')
    var_dict_3 = dict(a6='something_new', a7=1.0)
    yield Config(configs=[var_dict_1, var_dict_2, var_dict_3])


@pytest.fixture(scope='module')
def worklog(content_image_hash, style_image_hash):
    worklog = Worklog()
    worklog.content_hash = content_image_hash
    worklog.style_hash = style_image_hash
    worklog.table = {
        '02398101405c2b765c9fc87423c1423629990bdfe0415c5e40c67380d239df85': dict(
            image_name='0000.png', other_attribute=10
        ),
        '25104f6cdb887041b0858deb2dc54ab0f06035758c57b6ab7c394a028c5c45ee': dict(
            image_name='0001.png', other_attribute=14.5
        ),
        '59fabfdcf222823c48ceb0025689d48c6bb9aa0bac359b71b4369b1d9a0241e0': dict(
            image_name='0004.png', other_attribute=True
        ),
        '7181bba92070d3410fb1ed62296cc7cab327666bf56aa6490cf9b4a6c76e96a4': dict(
            image_name='0005.png', other_attribute=None
        ),
    }
    yield worklog


def test_variation_dict_to_styling_configs(full_config):
    # test sample 1
    expected_styling_configs_1 = [
        Config(a1='a1', a2=10, a3=0.5, a4=0, a5='way_1'),
        Config(a1='a1', a2=10, a3=0.5, a4=0, a5='way_2'),
        Config(a1='a1', a2=10, a3=0.5, a4=1, a5='way_1'),
        Config(a1='a1', a2=10, a3=0.5, a4=1, a5='way_2'),
        Config(a1='a1', a2=10, a3=0.5, a4=2, a5='way_1'),
        Config(a1='a1', a2=10, a3=0.5, a4=2, a5='way_2'),
    ]
    resulted_styling_configs_1 = variation_dict_to_styling_configs(full_config.configs[0])

    assert len(resulted_styling_configs_1) == len(expected_styling_configs_1)
    for styling_config in resulted_styling_configs_1:
        assert styling_config in expected_styling_configs_1

    # test sample 2
    expected_styling_configs_2 = [
        Config(a1='a1', a2=10, a3=0.5, a4=0, a5='way_1'),
        Config(a1='a1', a2=10, a3=0.5, a4=1, a5='way_1'),
        Config(a1='a1', a2=20, a3=0.5, a4=0, a5='way_1'),
        Config(a1='a1', a2=20, a3=0.5, a4=1, a5='way_1'),
    ]
    resulted_styling_configs_2 = variation_dict_to_styling_configs(full_config.configs[1])

    assert len(resulted_styling_configs_2) == len(expected_styling_configs_2)
    for styling_config in resulted_styling_configs_2:
        assert styling_config in expected_styling_configs_2

    # test sample 3
    expected_styling_configs_3 = [Config(a6='something_new', a7=1.0)]
    resulted_styling_configs_3 = variation_dict_to_styling_configs(full_config.configs[2])

    assert len(resulted_styling_configs_3) == len(expected_styling_configs_3)
    for styling_config in resulted_styling_configs_3:
        assert styling_config in expected_styling_configs_3


def test_get_styling_configs_with_no_duplicates(styling_configs_list):
    expected_unique_styling_configs = [
        Config(b1='B1', b2=2.0, b3=False),
        Config(b1='Z3', b2=2.5, b3=False),
        Config(b1='Z4', b2=15.0, b3=True),
        Config(b1='D1', b2=0, b3=False),
    ]
    styling_configs_dict = get_styling_configs_with_no_duplicates(styling_configs_list)
    resulted_unique_styling_configs = list(styling_configs_dict.values())

    assert len(resulted_unique_styling_configs) == len(expected_unique_styling_configs)
    for styling_config in resulted_unique_styling_configs:
        assert styling_config in expected_unique_styling_configs


def test_get_orders_no_worklog(content_image, style_image, full_config):
    expected_styling_configs = [
        Config(a1='a1', a2=10, a3=0.5, a4=0, a5='way_1'),
        Config(a1='a1', a2=10, a3=0.5, a4=0, a5='way_2'),
        Config(a1='a1', a2=10, a3=0.5, a4=1, a5='way_1'),
        Config(a1='a1', a2=10, a3=0.5, a4=1, a5='way_2'),
        Config(a1='a1', a2=10, a3=0.5, a4=2, a5='way_1'),
        Config(a1='a1', a2=10, a3=0.5, a4=2, a5='way_2'),
        Config(a1='a1', a2=20, a3=0.5, a4=0, a5='way_1'),
        Config(a1='a1', a2=20, a3=0.5, a4=1, a5='way_1'),
        Config(a6='something_new', a7=1.0),
    ]
    orders = get_orders(content_image, style_image, full_config)
    resulted_styling_configs = list(orders.values())

    assert len(resulted_styling_configs) == len(expected_styling_configs)
    for order in resulted_styling_configs:
        assert order in expected_styling_configs


def test_get_orders_with_worklog(content_image, style_image, full_config, worklog):
    expected_styling_configs = [
        Config(a1='a1', a2=10, a3=0.5, a4=0, a5='way_1'),
        Config(a1='a1', a2=10, a3=0.5, a4=1, a5='way_2'),
        Config(a1='a1', a2=10, a3=0.5, a4=2, a5='way_2'),
        Config(a1='a1', a2=20, a3=0.5, a4=0, a5='way_1'),
        Config(a6='something_new', a7=1.0),
    ]
    orders = get_orders(content_image, style_image, full_config, worklog)
    resulted_styling_configs = list(orders.values())

    assert len(resulted_styling_configs) == len(expected_styling_configs)
    for order in resulted_styling_configs:
        assert order in expected_styling_configs


def test_get_orders_with_new_image_pair(content_image, style_image, full_config, worklog):
    new_content_image = np.copy(content_image)
    new_content_image[50, 50, 0] = 255

    with pytest.raises(InvalidOrderException):
        get_orders(new_content_image, style_image, full_config, worklog)
