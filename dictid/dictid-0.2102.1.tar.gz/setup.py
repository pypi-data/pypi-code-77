# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dictid']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3.5.0,<4.0.0']

setup_kwargs = {
    'name': 'dictid',
    'version': '0.2102.1',
    'description': '',
    'long_description': None,
    'author': 'davips',
    'author_email': 'dpsabc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
