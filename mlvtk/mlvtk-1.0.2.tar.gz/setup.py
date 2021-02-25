# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlvtk',
 'mlvtk.base',
 'mlvtk.base.callbacks',
 'mlvtk.base.normalize',
 'mlvtk.base.plot']

package_data = \
{'': ['*']}

install_requires = \
['h5py>=2.10.0,<2.11.0',
 'pandas>=1.1.3,<1.2.0',
 'plotly>=4.9.0,<4.10.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'tensorflow>=2.3.1,<2.4.0',
 'tqdm>=4.50.2,<4.51.0']

setup_kwargs = {
    'name': 'mlvtk',
    'version': '1.0.2',
    'description': 'loss surface visualization tool',
    'long_description': None,
    'author': 'tm-schwartz',
    'author_email': 'tschwartz@csumb.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
