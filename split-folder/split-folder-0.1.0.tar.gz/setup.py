# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['split_folder']

package_data = \
{'': ['*']}

install_requires = \
['nb-utils>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'split-folder',
    'version': '0.1.0',
    'description': 'Spilt folder into train/val/test subset',
    'long_description': None,
    'author': 'Nivratti',
    'author_email': 'boyanenivratti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
