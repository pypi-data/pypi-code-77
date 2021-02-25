# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastabf',
 'fastabf.DAL',
 'fastabf.HACpackage',
 'fastabf.Helpers',
 'fastabf.csvstores',
 'fastabf.pipelines']

package_data = \
{'': ['*'], 'fastabf': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'fastabf',
    'version': '0.8.9',
    'description': 'A robust computation package for activity based funding calculations',
    'long_description': None,
    'author': 'Sri Sridharan',
    'author_email': 'sri@greenlakemedical.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
