# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pystratosphere']

package_data = \
{'': ['*']}

install_requires = \
['blessed>=1.17.10,<2.0.0',
 'python-box>=5.1.1,<6.0.0',
 'ruamel.yaml>=0.16.12,<0.17.0']

entry_points = \
{'console_scripts': ['strat = pystratosphere.cli:main']}

setup_kwargs = {
    'name': 'pystratosphere',
    'version': '0.1.0',
    'description': 'Show your speedrunning notes in time with your splits',
    'long_description': None,
    'author': 'Mark Rawls',
    'author_email': 'markrawls96@gmail.com',
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
