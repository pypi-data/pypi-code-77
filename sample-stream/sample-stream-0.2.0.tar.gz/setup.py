# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sample_stream']

package_data = \
{'': ['*']}

install_requires = \
['rich>=9.8.2,<10.0.0', 'typer[all]>=0.3.2,<0.4.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['sample-stream = sample_stream.__main__:main']}

setup_kwargs = {
    'name': 'sample-stream',
    'version': '0.2.0',
    'description': 'Sample lines from a stream.',
    'long_description': '# sample-stream\n\n<div align="center">\n\n[![Build status](https://github.com/jeroenjanssens/sample-stream/workflows/build/badge.svg?branch=master&event=push)](https://github.com/jeroenjanssens/sample-stream/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/sample-stream.svg)](https://pypi.org/project/sample-stream/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/jeroenjanssens/sample-stream/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/jeroenjanssens/sample-stream/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/jeroenjanssens/sample-stream/releases)\n[![License](https://img.shields.io/github/license/jeroenjanssens/sample-stream)](https://github.com/jeroenjanssens/sample-stream/blob/master/LICENSE)\n\nSample lines from a stream.\n\n</div>\n\n## License\n\n[![License](https://img.shields.io/github/license/jeroenjanssens/sample-stream)](https://github.com/jeroenjanssens/sample-stream/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/jeroenjanssens/sample-stream/blob/master/LICENSE) for more details.\n\n## Citation\n\n```\n@software{sample-stream,\n  author = {Jeroen H.M. Janssens},\n  title = {{sample-stream} -- Sample lines from a stream},\n  year = {2021},\n  url = {https://github.com/jeroenjanssens/sample-stream},\n  version = {0.2.0}\n}\n```\n\n## Credits\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).\n',
    'author': 'Jeroen Janssens',
    'author_email': 'jeroen@jeroenjanssens.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jeroenjanssens/sample-stream',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
