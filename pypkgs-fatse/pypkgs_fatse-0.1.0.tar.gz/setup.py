# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_fatse']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-fatse',
    'version': '0.1.0',
    'description': 'Experiment on creating python packages',
    'long_description': None,
    'author': 'fatse',
    'author_email': 'fatimeseelimi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
