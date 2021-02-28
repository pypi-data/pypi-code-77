# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flashgeotext']

package_data = \
{'': ['*'], 'flashgeotext': ['resources/*']}

install_requires = \
['flashtext>=2.7,<3.0', 'loguru>=0.5.3,<0.6.0', 'pydantic>=1.8,<2.0']

setup_kwargs = {
    'name': 'flashgeotext',
    'version': '0.3.0',
    'description': 'Extract and count countries and cities (+their synonyms) from text',
    'long_description': None,
    'author': 'Benjamin Ramser',
    'author_email': 'ahoi@iwpnd.pw',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
