# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wusa']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'docker>=4.4.0,<5.0.0',
 'gidgethub>=5.0.0,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.11.1,<10.0.0',
 'shortuuid>=1.0.1,<2.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['wusa = wusa.main:app']}

setup_kwargs = {
    'name': 'wusa',
    'version': '0.0.1',
    'description': 'CLI for managing self-hosted GitHub actions runner',
    'long_description': None,
    'author': 'Anton Helm',
    'author_email': 'anton.helm@tecnico.ulisboa.pt',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
