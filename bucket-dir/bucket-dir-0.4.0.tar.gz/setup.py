# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bucket_dir']

package_data = \
{'': ['*'], 'bucket_dir': ['templates/*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'boto3>=1.17.11,<2.0.0',
 'humanize>=3.2.0,<4.0.0',
 'rich>=9.11.0,<10.0.0']

entry_points = \
{'console_scripts': ['bucket-dir = bucket_dir:run_cli']}

setup_kwargs = {
    'name': 'bucket-dir',
    'version': '0.4.0',
    'description': 'Generate directory listings for S3 statically hosted content.',
    'long_description': None,
    'author': 'Dave Randall',
    'author_email': '19395688+daveygit2050@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
