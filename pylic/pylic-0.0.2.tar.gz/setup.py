# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylic']

package_data = \
{'': ['*']}

install_requires = \
['taskipy>=1.6.0,<2.0.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'pylic',
    'version': '0.0.2',
    'description': 'Python license checker',
    'long_description': None,
    'author': 'Sandro Huber',
    'author_email': 'sandrochuber@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
