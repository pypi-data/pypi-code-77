# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['racetrack', 'racetrack.tracks']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['racetrack = racetrack.__main__']}

setup_kwargs = {
    'name': 'racetrack',
    'version': '0.1.0',
    'description': 'A formal model of the Racetrack benchmark.',
    'long_description': '# Racetrack',
    'author': 'Maximilian Köhl',
    'author_email': 'koehl@cs.uni-saarland.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/koehlma/momba',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
