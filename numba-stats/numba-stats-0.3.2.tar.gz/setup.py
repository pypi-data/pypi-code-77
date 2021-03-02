# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numba_stats']

package_data = \
{'': ['*']}

install_requires = \
['importlib_metadata>=3.4', 'numba>=0.49', 'numpy>=1.18', 'scipy>=1.5']

setup_kwargs = {
    'name': 'numba-stats',
    'version': '0.3.2',
    'description': 'Numba-accelerated implementations of common probability distributions',
    'long_description': "# numba-stats\n\n![](https://img.shields.io/pypi/v/numba-stats.svg)\n\nWe provide numba-accelerated implementations of statistical functions for common probability distributions\n\n* normal\n* poisson\n* exponential\n* student's t\n* voigt\n\nwith more to come. The speed gains are huge, up to a factor of 100 compared to `scipy`. Benchmarks are included in the repository and are run by pytest.\n\n**You can help with adding more distributions, patches are very welcome.** Implementing a probability distribution is easy. You need to write it in simple Python that numba can understand. Special functions from `scipy.special` can be used after some wrapping, see submodule `numba_stats._special.py` how it is done.\n\nBecause of limited manpower, this project is barely documented. The documentation is basically `pydoc numba_stats`. The calling conventions are the same as for the corresponding functions in scipy.stats. These are sometimes a bit unusual, for example, for the exponential distribution, see the `scipy` docs for details.\n\n## numba-stats and numba-scipy\n\n[numba-scipy](https://github.com/numba/numba-scipy) is the official package and repository for fast numba-accelerated scipy functions, are we reinventing the wheel?\n\nIdeally, the functionality in this package should be in `numba-scipy` and we hope that eventually this will be case. In this package, we don't offer overloads for scipy functions and classes like `numba-scipy` does. This simplifies the implementation dramatically. `numba-stats` is intended as a temporary solution until fast statistical functions are included in `numba-scipy`. `numba-stats` currently does not depend on `numba-scipy`, only on `numba` and `scipy`.\n",
    'author': 'Hans Dembinski',
    'author_email': 'hans.dembinski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hdembinski/numba-stats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
