# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dash_data_table']

package_data = \
{'': ['*']}

install_requires = \
['dash>=1.19.0,<2.0.0']

setup_kwargs = {
    'name': 'dash-data-table',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'Jakob Jul Elben',
    'author_email': 'elbenjakobjul@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
