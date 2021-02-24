# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests']

package_data = \
{'': ['*']}

modules = \
['redismap']
install_requires = \
['redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'redismap',
    'version': '0.1.0',
    'description': 'A Redis wrapper that lets Redis be used as a python mapping',
    'long_description': '# redismap\n\nWrapper for Redis that allows a connection to a Redis server to be used as a Python mapping\n',
    'author': 'Ethan Paul',
    'author_email': '24588726+enpaul@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/enpaul/redismap/',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
