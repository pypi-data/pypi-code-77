# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fluxio_parser',
 'fluxio_parser.states',
 'fluxio_parser.states.tasks',
 'fluxio_parser.transformers',
 'fluxio_parser.visitors']

package_data = \
{'': ['*']}

install_requires = \
['astor>=0.8.1,<0.9.0',
 'black>=19.3b0,<20.0',
 'networkx>=2.5,<3.0',
 'pypants>=1,<2']

setup_kwargs = {
    'name': 'fluxio-parser',
    'version': '0.1.0',
    'description': 'Fluxio parser library',
    'long_description': '',
    'author': 'Jonathan Drake',
    'author_email': 'jdrake@narrativescience.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
