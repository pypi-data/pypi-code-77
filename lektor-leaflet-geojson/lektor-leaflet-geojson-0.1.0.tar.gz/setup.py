# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lektor_leaflet_geojson']

package_data = \
{'': ['*']}

install_requires = \
['lektor>=3.0.0,<4.0.0']

entry_points = \
{'lektor.plugins': ['leaflet-geojson = '
                    'lektor_leaflet_geojson:LeafletGeoJsonPlugin']}

setup_kwargs = {
    'name': 'lektor-leaflet-geojson',
    'version': '0.1.0',
    'description': 'Lektor template filter to convert geojson objects to Leaflet maps',
    'long_description': '# lektor-leaflet-geojson\n\n[![Run tests](https://github.com/cigar-factory/lektor-leaflet-geojson/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/cigar-factory/lektor-leaflet-geojson/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/cigar-factory/lektor-leaflet-geojson/branch/main/graph/badge.svg?token=cL2LogCTnu)](https://codecov.io/gh/cigar-factory/lektor-leaflet-geojson)\n[![PyPI Version](https://img.shields.io/pypi/v/lektor-leaflet-geojson.svg)](https://pypi.org/project/lektor-leaflet-geojson/)\n![License](https://img.shields.io/pypi/l/lektor-leaflet-geojson.svg)\n![Python Compatibility](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Flektor-leaflet-geojson%2Fjson)\n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\nLektor template filter to convert geojson objects to Leaflet maps\n\n## Installation\n\n```\npip install lektor-leaflet-geojson\n```\n\n## Usage\n\nImport the leaflet JS and CSS. You can skip this step if you are managing Leaflet yourself (e.g: with NPM)\n\n```\n{{ import_leaflet(\'1.7.1\') }} {# using a specified version #}\n```\n\n```\n{{ import_leaflet() }} {# default to "latest" #}\n```\n\nThe `|map()` filter can be used to render a GeoJSON feature on a map. Pass some inline CSS to style the map div.\n\n```\n{{\n  \'{"type": "Feature", "geometry": {"type": "Point", "coordinates": [125.6, 10.1]}}\' | map("height: 300px; width: 300px;")\n}}\n```\n',
    'author': 'chris48s',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cigar-factory/lektor-leaflet-geojson',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
