# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tikotapi']
setup_kwargs = {
    'name': 'tikotapi',
    'version': '1.0.4',
    'description': 'Documentation: tikotapi.tk or tikotapi.tutorial(). Easy API!',
    'long_description': None,
    'author': 'tikotstudio',
    'author_email': 'tikotstudio@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
