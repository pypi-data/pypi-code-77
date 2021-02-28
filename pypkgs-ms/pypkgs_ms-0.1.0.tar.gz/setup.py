# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_ms']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.5,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-ms',
    'version': '0.1.0',
    'description': 'Python package that eases the pain of concatenating Pandas categoricals!',
    'long_description': None,
    'author': 'Sicheng Marc SUN',
    'author_email': 'sun9703@student.ubc.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
