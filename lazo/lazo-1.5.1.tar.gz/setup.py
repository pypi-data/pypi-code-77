# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lazo', 'lazo.commands']

package_data = \
{'': ['*'], 'lazo': ['templates/*']}

install_requires = \
['click',
 'colorama',
 'pygments',
 'requests>=2.21.0',
 'websocket-client>=0.55.0']

setup_kwargs = {
    'name': 'lazo',
    'version': '1.5.1',
    'description': 'lazo',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
