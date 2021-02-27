# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bods_client']

package_data = \
{'': ['*']}

install_requires = \
['gtfs-realtime-bindings>=0.0.7,<0.0.8',
 'pydantic>=1.7.3,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'bods-client',
    'version': '0.2.0',
    'description': 'A Python client for the Department for Transport Bus Open Data Service API',
    'long_description': '# bods-client\n\n[![Build Status](https://github.com/ciaranmccormick/python-bods-client/workflows/test/badge.svg?branch=master&event=push)](https://github.com/ciaranmccormick/python-bods-client/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/ciaranmccormick/python-bods-client/branch/master/graph/badge.svg)](https://codecov.io/gh/ciaranmccormick/python-bods-client)\n[![Python Version](https://img.shields.io/pypi/pyversions/bods-client.svg)](https://pypi.org/project/bods-client/)\n\nA Python client for the Department for Transport Bus Open Data Service API\n\n\n## Installation\n\n```bash\npip install bods-client\n```\n\n\n## Example\n\n\n### GTFS RT\n\nAll the vehicle locations for vehicles in a geographical location can be obtained\nusing the `get_gtfs_rt_data_feed` method with a boundng box.\n\n```python\n\nfrom bods_client.client import BODSClient\nfrom bods_client.models import BoundingBox\n\n# An API key can be obtained by registering with the Bus Open Data Service\n# https://data.bus-data.dft.gov.uk/account/signup/\n>> API_KEY = "api-key"\n\n>> bods = BODSClient(api_key=API_KEY)\n>> box = BoundingBox(min_longitude=-0.54, min_latitude=51.26, max_longitude=0.27, max_latitide=51.75)\n>> message = bods.get_gtfs_rt_data_feed(bounding_box=box)\n>> message.entity[0]\nid: "421354378097713049"\nvehicle {\n  trip {\n    trip_id: ""\n    route_id: ""\n  }\n  position {\n    latitude: 51.712860107421875\n    longitude: -0.38401100039482117\n    bearing: 170.0\n  }\n  timestamp: 1614396229\n  vehicle {\n    id: "7214"\n  }\n}\n\n```\n\nThis returns a `google.transit.gtfs_realtime_pb2.FeedMessage` object. More details about\nGeneral Transit Feed Specification Realtime Transit (GTFS-RT) can be found\n[here](https://developers.google.com/transit/gtfs-realtime/).\n\n\n## License\n\n[MIT](https://github.com/ciaran.mccormick/bods-client/blob/master/LICENSE)\n\n\n',
    'author': 'Ciaran McCormick',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ciaranmccormick/python-bods-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
