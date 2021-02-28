# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['xh1scr']
setup_kwargs = {
    'name': 'xh1scr',
    'version': '1.0.0',
    'description': 'Asynchronous TikTok API Wrapper',
    'long_description': None,
    'author': 'perfecto',
    'author_email': 'rektnpc@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
