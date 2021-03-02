# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['j2tpl',
 'j2tpl.console',
 'j2tpl.console.commands',
 'j2tpl.loaders',
 'j2tpl.parsers']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0', 'cleo==1.0.0a2']

entry_points = \
{'console_scripts': ['j2tpl = j2tpl.console.application:main']}

setup_kwargs = {
    'name': 'j2tpl',
    'version': '2021.3.1',
    'description': '',
    'long_description': None,
    'author': 'Janne K',
    'author_email': '0x022b@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
