# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['api_2b2t']
setup_kwargs = {
    'name': 'api-2b2t',
    'version': '1.0.4',
    'description': 'This is api for minecraft server 2b2t. Documentation: https://github.com/YegorKryukov404/api2b2t/wiki/DOCS',
    'long_description': None,
    'author': 'yer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
