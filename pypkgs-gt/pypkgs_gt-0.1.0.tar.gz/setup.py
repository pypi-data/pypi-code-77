# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_gt']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-gt',
    'version': '0.1.0',
    'description': 'Python package for 524 assignment#1',
    'long_description': None,
    'author': 'Guanshu Tao',
    'author_email': 'guanshu@ualberta.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
