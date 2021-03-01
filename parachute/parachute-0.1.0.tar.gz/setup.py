# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parachute']

package_data = \
{'': ['*']}

install_requires = \
['pymavlink>=2.4.14,<3.0.0', 'pyserial>=3.5,<4.0', 'tqdm>=4.58.0,<5.0.0']

entry_points = \
{'console_scripts': ['parachute = parachute.cli:cli']}

setup_kwargs = {
    'name': 'parachute',
    'version': '0.1.0',
    'description': 'A lifeline for ArduPilot craft.',
    'long_description': None,
    'author': 'Stavros Korokithakis',
    'author_email': 'hi@stavros.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
