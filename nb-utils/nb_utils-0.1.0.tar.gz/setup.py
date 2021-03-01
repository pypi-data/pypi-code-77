# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nb_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nb-utils',
    'version': '0.1.0',
    'description': 'Python utilities',
    'long_description': None,
    'author': 'Nivratti',
    'author_email': 'boyanenivratti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
