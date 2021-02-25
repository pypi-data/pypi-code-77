"""A fixture for the config object."""

import pytest
from outcome.devkit_api.fixtures.keys import *  # type: ignore  # noqa: F403,WPS347,F401
from outcome.utils.config import Config


@pytest.fixture(scope='session')
def config(idp_public_key: str, private_key: str, public_key: str) -> Config:
    return Config(
        defaults={
            'DB_DATABASE': 'postgres',
            'DB_USERNAME': 'postgres',
            'DB_PASSWORD': 'postgres',
            'DB_SERVER': '127.0.0.1',
            'DB_PORT': '5432',
            'APP_NAME': 'apikit',
            'APP_VERSION': '0.1.0',
            'APP_PUBLIC_KEY': public_key,
            'APP_PRIVATE_KEY': private_key,
            'IDP_PUBLIC_KEY': idp_public_key,
        },
    )


__all__ = ['config']
