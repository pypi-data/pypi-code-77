# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prose']

package_data = \
{'': ['*']}

install_requires = \
['poethepoet>=0.10.0,<0.11.0',
 'poetry>=1.1.4,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0']

entry_points = \
{'console_scripts': ['prose = prose.cli:main']}

setup_kwargs = {
    'name': 'trashy-poetry',
    'version': '1.0.3',
    'description': 'Poetry for everyday use',
    'long_description': '# Prose\n\nAn unpoetic version of [Poetry](https://python-poetry.org/).\n\nWhile the Poetry package is elegant and reduces a Python developers burden, every day usage has some small annoyances. Some of these things could be fixed but have been considered out of scope and unpoetic.\n\nProse is made to be the everyday version of Poetry and little bit more trashy. But the trashiness serves those well in the dirty jobs of life. Prose is a wrapper around Poetry so all commands and APIs should function the same with the addition of more features.\n\n## Installation\n\n```\npip install trashy-poetry\n```\n\n## Usage\n\nSubstitute all `poetry` commands for `prose`.\n\nSee [Poetry Docs](https://python-poetry.org/docs/). All commands and APIs function the same except for the additional features documented.\n\nFor Example:\n\n```\npoetry init -> prose init\n\npoetry shell -> prose shell\n```\n\n## Features\n\n### Task Runner\n\nProse includes [Poe the Poet](https://github.com/nat-n/poethepoet) by default. Poe the Poet lets you create shortcuts to common tasks such as shell scripts and Python functions. The usage and API functions the same as documented except for the addition of the `poe` shortcut.\n\n`prose run poe [options] task [task_args]`\n\ncan also be run as\n\n`prose poe [options] task [task_args]`\n\n### Hardcoded Environmental Variables\n\nInject environmental variables into the `run` and `shell` commands by hard coding them into you `pyproject.toml` file.\n\n**Example:**\n\n```\n[tool.prose.env]\nTEST_ENV = "hello world"\nTEST_PATH = "${PATH}:/narf"\n```\n\nAny variables set in the `tool.prose.env` section of your toml file will be injected into the environment for you.\n\n### Load DotEnv Files\n\n### Default DotEnv Files\n\nProse loads `.env` files if it finds it in the current working directory. See [python-dotenv](https://pypi.org/project/python-dotenv/) for usage documentation.\n\n## Custom DotEnv Files\nProse allows you to add custom `.env` files with a command line switch for the `poe`, `run`, and `shell` commands.\n\n```\nOPTIONS\n  -e (--env)             Dotenv file to load (multiple values allowed)\n```\n\n**Examples:**\n\n```\nprose shell -e path/custom.env\nprose run -e path/custom.env printenv NARF\nprose poe -e path/custom.env mycommand\n```\n\n*Note: When using the `run` and `poe` commands, the `-e` and `--env` options must be used before your command arguments*\n',
    'author': 'Paul Bailey',
    'author_email': 'paul@neutron.studio',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pizzapanther/prose',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
