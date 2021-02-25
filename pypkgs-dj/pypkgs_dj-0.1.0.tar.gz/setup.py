# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_dj']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-dj',
    'version': '0.1.0',
    'description': 'This is the initial step of creating a toy Python package.',
    'long_description': None,
    'author': 'Jianru D',
    'author_email': 'dengjr1509@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
