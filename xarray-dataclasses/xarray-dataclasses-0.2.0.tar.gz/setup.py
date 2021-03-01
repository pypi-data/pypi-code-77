# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xarray_dataclasses']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19,<2.0', 'typing-extensions>=3.7,<4.0', 'xarray>=0.15,<0.16']

setup_kwargs = {
    'name': 'xarray-dataclasses',
    'version': '0.2.0',
    'description': 'xarray extension for dataarray classes',
    'long_description': '# xarray-dataclasses\n\n[![PyPI](https://img.shields.io/pypi/v/xarray-dataclasses.svg?label=PyPI&style=flat-square)](https://pypi.org/project/xarray-dataclasses/)\n[![Python](https://img.shields.io/pypi/pyversions/xarray-dataclasses.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/project/xarray-dataclasses/)\n[![Test](https://img.shields.io/github/workflow/status/astropenguin/xarray-dataclasses/Test?logo=github&label=Test&style=flat-square)](https://github.com/astropenguin/xarray-dataclasses/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nxarray extension for dataarray classes\n\n## TL;DR\n\nxarray-dataclasses is a third-party Python package which helps to create DataArray classes in the same manner as [the Python\'s native dataclass].\nHere is an introduction code of what the package provides:\n\n```python\nfrom xarray_dataclasses import DataArray, dataarrayclass\n\n\n@dataarrayclass\nclass Image:\n    """DataArray class to represent images."""\n\n    data: DataArray[(\'x\', \'y\'), float]\n    x: DataArray[\'x\', int] = 0\n    y: DataArray[\'y\', int] = 0\n```\n\nThe key features are:\n\n```python\n# create a DataArray instance\nimage = Image.new([[0, 1], [2, 3]], x=[0, 1], y=[0, 1])\n\n# create a DataArray instance filled with ones\nones = Image.ones((2, 2), x=[0, 1], y=[0, 1])\n```\n\n- Custom DataArray instances with fixed dimensions, datatype, and coordinates can easily be created.\n- NumPy-like special functions like ``ones()`` are provided as class methods.\n\n## Requirements\n\n- **Python:** 3.7, 3.8, or 3.9 (tested by the author)\n- **Dependencies:** See [pyproject.toml](pyproject.toml)\n\n## Installation\n\n```shell\n$ pip install xarray-dataclasses\n```\n\n<!-- References -->\n[the Python\'s native dataclass]: https://docs.python.org/3/library/dataclasses.html\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astropenguin/xarray-dataclasses/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
