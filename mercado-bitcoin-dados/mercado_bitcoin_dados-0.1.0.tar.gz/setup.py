# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mercado_bitcoin_dados']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'mercado-bitcoin-dados',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Nicolas Rodriguez Celys',
    'author_email': 'n.rodri.eng.soft@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
