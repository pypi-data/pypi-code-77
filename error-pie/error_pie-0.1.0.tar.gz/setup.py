# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['error_pie']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'error-pie',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'CharlesAverill',
    'author_email': 'charlesaverill20@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
