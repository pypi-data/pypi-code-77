# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flow_py_sdk',
 'flow_py_sdk.cadence',
 'flow_py_sdk.client',
 'flow_py_sdk.examples',
 'flow_py_sdk.frlp',
 'flow_py_sdk.proto',
 'flow_py_sdk.proto.flow']

package_data = \
{'': ['*']}

install_requires = \
['betterproto[compiler]>=1.2.5,<2.0.0',
 'ecdsa>=0.16.1,<0.17.0',
 'grpcio-tools>=1.33.2,<2.0.0',
 'rlp>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['examples = flow_py_sdk.run_examples:run']}

setup_kwargs = {
    'name': 'flow-py-sdk',
    'version': '0.1.0',
    'description': 'A python SKD for the flow blockchain',
    'long_description': '# flow-py-sdk\n\nAnother unofficial flow blockchain python sdk.\n\nUnder development! I do not recommend you use this\n\n## Prerequisites\n\n- [poetry](https://python-poetry.org/docs/)\n\n## Examples\n\n- `poetry build` (only the first time)\n- `poetry run examples`',
    'author': 'Janez Podhostnik',
    'author_email': 'janez.podhostnik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/janezpodhostnik/flow-py-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
