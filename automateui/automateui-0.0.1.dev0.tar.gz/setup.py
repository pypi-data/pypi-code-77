# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['automateui']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'automateui',
    'version': '0.0.1.dev0',
    'description': 'Automate web UI fast',
    'long_description': '# Automate UI\n\n> Automate web UI fast and easily\n\n**This project is a work in progress!**',
    'author': 'ninest',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
