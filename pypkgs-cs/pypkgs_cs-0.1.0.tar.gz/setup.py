# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_cs']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-cs',
    'version': '0.1.0',
    'description': 'Python package to ease the pain of concatenating Pandas categoricals',
    'long_description': None,
    'author': 'Cal Schafer',
    'author_email': 'schafer1@student.ubc.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
