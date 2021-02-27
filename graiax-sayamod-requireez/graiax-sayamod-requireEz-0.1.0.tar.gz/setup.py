# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graiax_sayamod_requireez']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'graiax-sayamod-requireez',
    'version': '0.1.0',
    'description': '[Sayamod] 轻松require——解决依赖问题',
    'long_description': None,
    'author': 'Eric',
    'author_email': 'erictianc@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
