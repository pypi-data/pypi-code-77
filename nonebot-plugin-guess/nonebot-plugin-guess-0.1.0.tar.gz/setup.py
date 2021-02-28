# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_guess']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.6.3,<2.0.0', 'nonebot2>=2.0.0-alpha.10,<3.0.0', 'pydantic==1.7.3']

setup_kwargs = {
    'name': 'nonebot-plugin-guess',
    'version': '0.1.0',
    'description': 'nobebot2插件《猜猜看》',
    'long_description': None,
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/nonebot-plugin-guess-game',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
