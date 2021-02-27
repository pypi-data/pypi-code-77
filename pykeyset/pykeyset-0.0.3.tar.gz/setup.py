# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pykeyset',
 'pykeyset.core',
 'pykeyset.core.font',
 'pykeyset.core.icon',
 'pykeyset.core.profile',
 'pykeyset.resources',
 'pykeyset.resources.fonts',
 'pykeyset.resources.icons',
 'pykeyset.resources.profiles',
 'pykeyset.utils',
 'pykeyset.utils.path']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'enum-tools>=0.6.1,<0.7.0',
 'recordclass>=0.14.0,<0.15.0',
 'rich>=9.0.0,<10.0.0',
 'toml>=0.10.1,<0.11.0',
 'typer[all]>=0.3.0,<0.4.0']

extras_require = \
{':python_version < "3.7"': ['importlib-resources>=4.0,<5.0']}

entry_points = \
{'console_scripts': ['pykeyset = pykeyset.__main__:app']}

setup_kwargs = {
    'name': 'pykeyset',
    'version': '0.0.3',
    'description': 'A Python-based tool to create pretty keyset layout diagrams using correct fonts and icons.',
    'long_description': "# pykeyset\n\nA Python-based tool to create pretty keyset layout diagrams using correct fonts and icons.\n\n[![Build Status](https://img.shields.io/github/workflow/status/staticintlucas/pykeyset/Build?style=flat-square)][actions]\n[![Test Status](https://img.shields.io/github/workflow/status/staticintlucas/pykeyset/Tests?label=tests&style=flat-square)][actions]\n[![Test coverage](https://img.shields.io/codecov/c/github/staticintlucas/pykeyset?style=flat-square)][coverage]\n[![Python Version](https://img.shields.io/pypi/pyversions/pykeyset?style=flat-square)][pypi]\n[![Code style](https://img.shields.io/badge/code_style-black-black?style=flat-square)][black]\n[![PyPI](https://img.shields.io/pypi/v/pykeyset?style=flat-square)][pypi]\n[![PyPI downloads](https://img.shields.io/pypi/dm/pykeyset?style=flat-square)][pypi]\n[![License](https://img.shields.io/github/license/staticintlucas/pykeyset?style=flat-square)][licence]\n\n## Warning\n\n**This project is currently in the early stages of development.\nIt currently supports exactly what I need for TA Origins, and not much else.\nAt the moment it has only just over 75% test coverage, but this is continuously increasing.\nIf you do find any bug or experience any crashes, please report them on the [GitHub repo][pykeyset].\nIn future I hope to stabilise this project, add more extensive support for different profiles, fonts, file formats, etc; and have a more extensive API.**\n\nFeel free to help this project improve by opening bug reports, feature requests, etc; or contributing directly to the code by opening a pull request.\n\n## Example usage\n\n`pykeyset` uses commands to tell it what to do.\nThe easiest way is to use it is to create a *.cmdlist* (command list) file.\nEach line of the command list is a command for pykeyset to execute.\n\nFor example, a file called *example.cmdlist* contains the following commands:\n\n    load kle http://www.keyboard-layout-editor.com/#/gists/102f1fb614275f50e39d970d691e1030\n    load profile cherry\n    load font cherry\n    generate layout\n    save svg example.svg\n\nTo execute the command list run:\n\n    pykeyset run example.cmdlist\n\nThe output in *example.svg* is:\n\n![example.svg](example/example.png)\n\n## Python API\n\nCurrently you *can* use `pykeyset` directly as a Python module, but as it is still in early development the API will probably change *a lot* until a 0.1 release.\nAfter that there will be a relatively stable API, so you don't need to mess around with *.cmdlist* files if you're familiar with Python.\n\n## Installation\n\n`pykeyset` is available on [PyPI]. To install with `pip` run:\n\n    pip install pykeyset\n\nOr to install the latest source directly from GitHub, run:\n\n    git clone https://github.com/staticintlucas/pykeyset.git pykeyset\n    cd pykeyset\n    pip install .\n\nThis project uses [Poetry] as it's dependency manager and build system.\nTo install this package locally for development, run:\n\n    poetry install\n\nTo build the source distribution and wheel run:\n\n    poetry build\n\n## Contributing\n\n`pykeyset` uses [Black] and [isort] for formatting, and all code must pass [Flake8]'s checks.\nThese are checked by GitHub on all pull requests.\nTo run these tools automatically when committing, install the [pre-commit] hook in [`.pre-commit-config.yaml`].\n\n## Credits\n\nThe builtin `cherry` font is based on [Open Cherry] by Dakota Felder.\n\n[pykeyset]: https://github.com/staticintlucas/pykeyset\n[actions]: https://github.com/staticintlucas/pykeyset/actions\n[coverage]: https://codecov.io/gh/staticintlucas/pykeyset\n[licence]: LICENCE\n[pypi]: https://pypi.org/project/pykeyset/\n[black]: https://github.com/psf/black\n[isort]: https://pycqa.github.io/isort/\n[Poetry]: https://python-poetry.org/\n[open cherry]: https://github.com/dakotafelder/open-cherry\n[flake8]: https://flake8.pycqa.org/en/latest/\n[pre-commit]: https://pre-commit.com/\n[`.pre-commit-config.yaml`]: .pre-commit-config.yaml\n",
    'author': 'Lucas Jansen',
    'author_email': '7199136+staticintlucas@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/staticintlucas/pykeyset',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
