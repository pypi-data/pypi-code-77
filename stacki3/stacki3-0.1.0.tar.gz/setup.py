# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stacki3']

package_data = \
{'': ['*']}

install_requires = \
['i3ipc>=2.2.1,<3.0.0']

setup_kwargs = {
    'name': 'stacki3',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Viliam Valent',
    'author_email': 'vilo.valent@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
