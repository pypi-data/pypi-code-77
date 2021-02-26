# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_thrift']

package_data = \
{'': ['*']}

install_requires = \
['sphinx>=3.5.1,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'sphinx-thrift',
    'version': '0.1.1a1',
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
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
