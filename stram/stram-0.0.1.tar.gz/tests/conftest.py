import pytest
from os.path import join

from stram.utils.image_processing import load_image


def pytest_collection_modifyitems(items):
    e2e_identifier = join('tests', 'e2e')
    unit_identifier = join('tests', 'unit')
    integration_identifier = join('tests', 'integration')

    for item in items:
        item_path = str(item.fspath)

        if unit_identifier in item_path:
            item.add_marker(pytest.mark.run(order=0))
        elif integration_identifier in item_path:
            item.add_marker(pytest.mark.run(order=1))
        elif e2e_identifier in item_path:
            item.add_marker(pytest.mark.run(order=2))


@pytest.fixture(scope='function')
def mock_debug_env(monkeypatch, tmpdir):
    monkeypatch.setenv('DEBUG', 'True')
    monkeypatch.setenv('SUMMARY_PATH', str(tmpdir.mkdir('summaries')))
    monkeypatch.setenv('SUMMARY_FREQUENCY_IMAGES', '5')


@pytest.fixture(scope='function')
def mock_release_env(monkeypatch):
    monkeypatch.setenv('DEBUG', 'False')


@pytest.fixture(scope='package')
def content_image():
    content_image_path = join('tests', 'data', 'content_image.jpg')
    yield load_image(content_image_path)


@pytest.fixture(scope='package')
def style_image():
    style_image_path = join('tests', 'data', 'style_image.jpg')
    yield load_image(style_image_path)


@pytest.fixture(scope='package')
def content_image_hash():
    yield 'dd24aa9483cc39fea4ba326b1377709789e82a23927749509036f1bd04f64323'


@pytest.fixture(scope='package')
def style_image_hash():
    yield 'ed1d677c42733ea402c3fedda329cd29025b552873169e2fe4572c516f84c36f'
