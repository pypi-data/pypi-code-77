# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unscrapulous']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0',
 'argparse>=1.4.0,<2.0.0',
 'bs4>=0.0.1,<0.0.2',
 'lxml>=4.6.2,<5.0.0',
 'openpyxl>=3.0.6,<4.0.0',
 'pandas>=1.2.2,<2.0.0',
 'pytest>=6.2.2,<7.0.0',
 'requests>=2.25.1,<3.0.0',
 'tabula-py>=2.2.0,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'xlrd>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['unscrapulous = unscrapulous.unscrapulous:main']}

setup_kwargs = {
    'name': 'unscrapulous',
    'version': '0.1.1',
    'description': 'A utility that scrapes lists of unscrupulous entities (barred from doing financial business) published by various legal institutions',
    'long_description': None,
    'author': 'Navaneeth Suresh',
    'author_email': 'navaneeths1998@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1',
}


setup(**setup_kwargs)
