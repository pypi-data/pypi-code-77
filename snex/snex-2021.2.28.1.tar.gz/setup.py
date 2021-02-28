# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['snex', 'snex.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pyhocon>=0.3.57,<0.4.0', 'pystache>=0.5.4,<0.6.0']

entry_points = \
{'console_scripts': ['snex = snex.cli:main']}

setup_kwargs = {
    'name': 'snex',
    'version': '2021.2.28.1',
    'description': 'snex - snippet extractor',
    'long_description': None,
    'author': 'Joachim Bargsten',
    'author_email': 'jw@bargsten.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jwbargsten/snex/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
