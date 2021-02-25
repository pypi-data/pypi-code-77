# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twacapic']

package_data = \
{'': ['*']}

install_requires = \
['TwitterAPI>=2.6.9,<3.0.0']

setup_kwargs = {
    'name': 'twacapic',
    'version': '0.1.0',
    'description': 'A Twitter Academic API Client',
    'long_description': None,
    'author': 'FlxVctr',
    'author_email': 'flxvctr@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
