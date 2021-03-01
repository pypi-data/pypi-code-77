# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['date_formatter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'date-formatter',
    'version': '0.1.0',
    'description': 'A Python package for formatting strings into readable date strings',
    'long_description': None,
    'author': 'pauladjata',
    'author_email': 'info@adjata.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
