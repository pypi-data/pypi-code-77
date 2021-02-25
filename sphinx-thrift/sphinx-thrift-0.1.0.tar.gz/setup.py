# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_thrift']

package_data = \
{'': ['*']}

install_requires = \
['sphinx>=3.5.1,<4.0.0']

setup_kwargs = {
    'name': 'sphinx-thrift',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Csonkás Kristóf Gyula',
    'author_email': 'csonkas.kristof@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
