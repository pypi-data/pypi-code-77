# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pfin']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pfin',
    'version': '0.0.1',
    'description': 'Personal Finance simplified. A minimal toolkit to manage your finances from the command-line. Easy to learn and extendible.',
    'long_description': None,
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
