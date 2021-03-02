# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybookmd', 'pybookmd.generators']

package_data = \
{'': ['*']}

install_requires = \
['fastcore==1.3.19', 'packaging==20.9', 'pypandoc==1.5', 'pyparsing==2.4.7']

setup_kwargs = {
    'name': 'pybookmd',
    'version': '1.0.1',
    'description': '"Simple book building CLI for markdown based books"',
    'long_description': None,
    'author': 'Dylan Kirby',
    'author_email': 'dylankirbydev@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
