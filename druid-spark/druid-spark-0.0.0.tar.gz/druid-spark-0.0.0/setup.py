# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['druid_spark']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'druid-spark',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Vivek Balakrishnan',
    'author_email': 'vivek.balakrishnan@rovio.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
