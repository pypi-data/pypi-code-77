# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parachute']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'json5>=0.9.5,<0.10.0',
 'pymavlink>=2.4.14,<3.0.0',
 'pyserial>=3.5,<4.0',
 'tqdm>=4.58.0,<5.0.0']

entry_points = \
{'console_scripts': ['parachute = parachute.cli:cli']}

setup_kwargs = {
    'name': 'parachute',
    'version': '0.1.1',
    'description': 'A lifeline for ArduPilot craft.',
    'long_description': 'Parachute\n=========\n\nParachute is a helper script for ArduPilot craft. It helps you quickly and\neasily back up all your parameters to a file, and lets you filter them, diff\nthem, restore them or convert them to parameter files compatible with\nMission Planner/QGroundControl.\n\n\nInstallation\n------------\n\nInstalling Parachute is simple. You can use `pipx` (recommended):\n\n```\n$ pipx install parachute\n```\n\nOr `pip` (less recommended):\n\n```\n$ pip install parachute\n```\n\n\nUsage\n-----\n\nParachute is called like so:\n\n```\n$ parachute backup <craft name>\n```\n\nFor example:\n\n```\n$ parachute backup Mini-Drak\n```\n\n\nYou can also convert a Parachute file to a file compatible with Mission Planner or QGroundControl:\n\n```\n$ parachute convert qgc Mini-Drak_2021-03-02_02-29.chute Mini-Drak.params\n```\n\nYou can filter parameters based on a regular expression:\n\n```\n$ parachute filter "serial[123]_" Mini-Drak_2021-03-02_02-29.chute filtered.chute\n```\n\nSince all parameter names are uppercase, the regex is case-insensitive, for convenience.\n\nYou can also filter when converting:\n\n```\n$ parachute convert --filter=yaw mp Mini-Drak_2021-03-02_02-29.chute -\n```\n',
    'author': 'Stavros Korokithakis',
    'author_email': 'hi@stavros.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/stavros/parachute',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
