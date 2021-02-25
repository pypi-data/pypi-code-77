# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dji3d']

package_data = \
{'': ['*']}

install_requires = \
['ffmpeg-python>=0.2.0,<0.3.0',
 'matplotlib>=3.3.4,<4.0.0',
 'pysrt>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'dji3d',
    'version': '0.1.0',
    'description': 'DJI3D is a tool for graphing 3d positional data extracted from DJI drone telemetry',
    'long_description': None,
    'author': 'Evan Pratten',
    'author_email': 'ewpratten@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
