# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daylio_parser']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.1,<2.0.0']

setup_kwargs = {
    'name': 'daylio-parser',
    'version': '0.1.0',
    'description': 'A Python module to parse Daylio exports',
    'long_description': None,
    'author': 'Meesha',
    'author_email': '44530786+meesha7@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
