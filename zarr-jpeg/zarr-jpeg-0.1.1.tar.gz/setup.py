# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zarr_jpeg']

package_data = \
{'': ['*']}

install_requires = \
['imagecodecs>=2020.1.31,<2021.0.0', 'numcodecs>=0.6.4,<0.7.0']

setup_kwargs = {
    'name': 'zarr-jpeg',
    'version': '0.1.1',
    'description': 'JPEG Compression for uint8 zarr arrays',
    'long_description': None,
    'author': 'Davis Vann Bennett',
    'author_email': 'davis.v.bennett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
