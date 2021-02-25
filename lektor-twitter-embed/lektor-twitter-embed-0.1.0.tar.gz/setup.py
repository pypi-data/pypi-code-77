# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lektor_twitter_embed']

package_data = \
{'': ['*']}

install_requires = \
['lektor>=3.0.0,<4.0.0', 'requests>=2.0.0,<3.0.0']

entry_points = \
{'lektor.plugins': ['twitter-embed = lektor_twitter_embed:TwitterEmbedPlugin']}

setup_kwargs = {
    'name': 'lektor-twitter-embed',
    'version': '0.1.0',
    'description': 'Lektor template filter to convert twitter links to embeds',
    'long_description': '# lektor-twitter-embed\n\n[![Run tests](https://github.com/cigar-factory/lektor-twitter-embed/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/cigar-factory/lektor-twitter-embed/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/cigar-factory/lektor-twitter-embed/branch/main/graph/badge.svg?token=teWLUZntKT)](https://codecov.io/gh/cigar-factory/lektor-twitter-embed)\n[![PyPI Version](https://img.shields.io/pypi/v/lektor-twitter-embed.svg)](https://pypi.org/project/lektor-twitter-embed/)\n![License](https://img.shields.io/pypi/l/lektor-twitter-embed.svg)\n![Python Compatibility](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Flektor-twitter-embed%2Fjson)\n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\nLektor template filter to convert twitter links to embeds\n\n## Installation\n\n```\npip install lektor-twitter-embed\n```\n\n## Usage\n\n```\n{{ "https://twitter.com/MaiaFranklyn/status/1277100235928621058" | tweet }}\n```\n\nIt is possible to pass an optional \'params\' object to configure the embed.\nAny of the params documented at\nhttps://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/get-statuses-oembed\nmay be supplied\n\n```\n{{\n  "https://twitter.com/MaiaFranklyn/status/1277100235928621058" | tweet(\n    params={\'align\': \'center\', \'hide_thread\': \'true\'}\n  )\n}}\n```\n\nBy default if the request to `publish.twitter.com` fails, your page will not build.\nThis behaviour can be changed so that a failed request to `publish.twitter.com` will fall back to rendering a link to the tweet.\n\n```\n{{ "https://twitter.com/lucaviftw/status/1347311486012686336" | tweet(fallback=True) }}\n```\n',
    'author': 'chris48s',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chris48s/lektor-twitter-embed',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
