# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multimv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'multimv',
    'version': '0.1.0',
    'description': 'Multi mv via fixed string / regex / bash pattern substitutions',
    'long_description': None,
    'author': 'Summer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
