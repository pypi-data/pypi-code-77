# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_iz']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-iz',
    'version': '0.1.0',
    'description': 'Python package that eases the pain of concatenating Pandas categoricals!',
    'long_description': None,
    'author': 'Ivy Zhang',
    'author_email': 'ivyzhang1017@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
