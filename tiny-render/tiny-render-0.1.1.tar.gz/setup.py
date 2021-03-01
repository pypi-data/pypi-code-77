# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiny_render']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0']

setup_kwargs = {
    'name': 'tiny-render',
    'version': '0.1.1',
    'description': 'A simple wrapper of Jinja2 to render text based file, eg. SQL code and YAML files',
    'long_description': None,
    'author': 'Zhong Dai',
    'author_email': 'zhongdai@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
