# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toypackage']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'toypackage',
    'version': '0.1.0',
    'description': 'A toy package so we would learn how to create a python package',
    'long_description': None,
    'author': 'kshahnazari1998',
    'author_email': 'kshahnazari@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
