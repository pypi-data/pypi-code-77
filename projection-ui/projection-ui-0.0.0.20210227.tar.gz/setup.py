# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['projection', 'projection.elements', 'projection.externals']

package_data = \
{'': ['*'], 'projection': ['static/*', 'static/css/*', 'static/js/*']}

install_requires = \
['tornado>=6.1,<7.0']

setup_kwargs = {
    'name': 'projection-ui',
    'version': '0.0.0.20210227',
    'description': 'A library for projecting a UI onto a browser',
    'long_description': None,
    'author': 'Kaithar',
    'author_email': 'noreply.committer@the-cell.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kaithar/projection-ui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
