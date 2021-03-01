# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gatoniel_utils', 'gatoniel_utils.segmentation']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.1,<2.0.0', 'scikit-image>=0.18.1,<0.19.0', 'scipy>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'gatoniel-utils',
    'version': '0.1.0',
    'description': 'Library with utils and helpers for myself.',
    'long_description': '# gatoniel-utils\n\n[![Build Status](https://github.com/gatoniel/gatoniel-utils/workflows/test/badge.svg?branch=master&event=push)](https://github.com/gatoniel/gatoniel-utils/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/gatoniel/gatoniel-utils/branch/master/graph/badge.svg)](https://codecov.io/gh/gatoniel/gatoniel-utils)\n[![Python Version](https://img.shields.io/pypi/pyversions/gatoniel-utils.svg)](https://pypi.org/project/gatoniel-utils/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nLibrary with utils and helpers for myself.\n\n\n## Features\n\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n- Add yours!\n\n\n## Installation\n\n```bash\npip install gatoniel-utils\n```\n\n\n## Example\n\nShowcase how your project can be used:\n\n```python\nfrom gatoniel_utils.example import some_function\n\nprint(some_function(3, 4))\n# => 7\n```\n\n## License\n\n[MIT](https://github.com/gatoniel/gatoniel-utils/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [0c5619079cb74e7dc72e1f18e9176b3b3a1a843f](https://github.com/wemake-services/wemake-python-package/tree/0c5619079cb74e7dc72e1f18e9176b3b3a1a843f). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/0c5619079cb74e7dc72e1f18e9176b3b3a1a843f...master) since then.\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gatoniel/gatoniel-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
