# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paaaaath']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-storage>=1.36.1,<2.0.0',
 'lambdas>=0.1.0,<0.2.0',
 'smart-open[gcs,http,s3]>=4.1.2,<5.0.0']

setup_kwargs = {
    'name': 'paaaaath',
    'version': '0.1.5',
    'description': 'a useful alternative Path object',
    'long_description': None,
    'author': 'Masahiro Wada',
    'author_email': 'argon.argon.argon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
