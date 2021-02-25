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
    'version': '1.0.0',
    'description': 'DJI3D is a tool for graphing 3d positional data extracted from DJI drone telemetry',
    'long_description': '# DJI3D\n\n![Poetry Build Suite](https://github.com/Ewpratten/dji3d/workflows/Poetry%20Build%20Suite/badge.svg)\n\nDJI3D is a tool for graphing 3d positional data extracted from DJI drone telemetry. Many DJI drones have the option to save basic flight telemetry data inside subtitle tracks on recorded videos. This script will extract this data and export it in one of three formats:\n\n - 3D graph\n   - Takes GPS data, and plots it with matplotlib\n - JSON\n   - A raw, timestamped JSON dump\n - CSV\n   - A timestamped CSV log\n\n## Usage\n\n```\nusage: dji3d [-h] [-i] [-f {graph,csv,json}] [-o OUTPUT] input\n\nDJI3D is a tool for graphing 3d positional data extracted from DJI drone telemetry\n\npositional arguments:\n  input                 Raw drone video file with telemetry data\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -i, --interactive     Run interactively\n  -f {graph,csv,json}, --format {graph,csv,json}\n                        Output format\n  -o OUTPUT, --output OUTPUT\n                        Output location\n```\n\n## Installing\n\n```sh\npython3 -m pip install dji3d\n```\n\n## Example\n\n![](./test.png)',
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
