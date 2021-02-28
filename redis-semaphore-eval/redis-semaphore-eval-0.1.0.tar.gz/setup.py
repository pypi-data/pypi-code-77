# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['redis_semaphore_eval']

package_data = \
{'': ['*']}

install_requires = \
['redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'redis-semaphore-eval',
    'version': '0.1.0',
    'description': 'A redis semaphore implementation using eval scripts',
    'long_description': '# Redis Semaphore Eval\n\n[![codecov](https://codecov.io/gh/wakemaster39/fastbin/branch/master/graph/badge.svg?token=H9WAVWZ7YY)](undefined)\n[![Actions Status](https://github.com/wakemaster39/fastbin/workflows/Tests/badge.svg)](https://github.comwakemaster39/fastbin/actions)\n[![Version](https://img.shields.io/pypi/v/fastbin)](https://pypi.org/project/fastbin/)\n[![PyPI - Wheel](https://img.shields.io/pypi/wheel/fastbin.svg)](https://pypi.org/project/fastbin/)\n[![Pyversions](https://img.shields.io/pypi/pyversions/fastbin.svg)](https://pypi.org/project/fastbin/)\n\n_Fastbin_ is a drop in replacement of [pycasbin](https://github.com/casbin/pycasbin) the python implementation of the\n\n\n\n## Contributing\n\n```\npoetry run pre-commit install -t pre-commit -t commit-msg && poetry run pre-commit run --all\n```\n',
    'author': 'Cameron HUrst',
    'author_email': 'cameron.a.hurst@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wakemaster39/redis-semaphore-eval',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
