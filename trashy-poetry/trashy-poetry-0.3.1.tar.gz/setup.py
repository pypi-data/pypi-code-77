# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prose']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.1.4,<2.0.0', 'python-dotenv>=0.15.0,<0.16.0']

entry_points = \
{'console_scripts': ['prose = prose.cli:main']}

setup_kwargs = {
    'name': 'trashy-poetry',
    'version': '0.3.1',
    'description': 'Poetry for everyday use',
    'long_description': '# Prose\n\nAn unpoetic version of [Poetry](https://python-poetry.org/).\n\nWhile the Poetry package is elegant and reduces a Python developers burden, every day usage has some small annoyances. Some of these things could be fixed but have been considered out of scope and unpoetic.\n\nProse is made to be the everyday version of Poetry and little bit more trashy. But the trashiness serves those well in the dirty jobs of life. Prose is a wrapper around Poetry so all commands and APIs should function the same with the addition of more features.\n\n## Installation\n\n```\npip install trashy-poetry\n```\n\n## Usage\n\nSubstitute all `poetry` commands for `prose`.\n\nSee [Poetry Docs](https://python-poetry.org/docs/). All commands and APIs function the same except for the additional features documented.\n\nFor Example:\n\n```\npoetry init -> prose init\n\npoetry shell -> prose shell\n```\n\n## Features\n\n### Hardcoded Environmental Variables\n\nInject environmental variables into the `run` and `shell` commands by hard coding them into you `pyproject.toml` file.\n\n**Example:**\n\n```\n[tool.prose.env]\nTEST_ENV = "hello world"\nTEST_PATH = "${PATH}:/narf"\n```\n\nAny variables set in the `tool.prose.env` section of your toml file will be injected into the environment for you.\n\n### Load DotEnv Files\n\n*coming soon*\n\n\n### Shortcut Commands\n\n*coming soon*\n',
    'author': 'Paul Bailey',
    'author_email': 'paul@neutron.studio',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pizzapanther/prose',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
