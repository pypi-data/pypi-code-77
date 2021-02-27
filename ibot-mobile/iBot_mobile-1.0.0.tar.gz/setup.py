# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ibot_mobile']
setup_kwargs = {
    'name': 'ibot-mobile',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': '0X00077',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
