# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['layerview',
 'layerview.app',
 'layerview.app.dialog_info',
 'layerview.app.dialog_load',
 'layerview.app.main_window',
 'layerview.app.pyuic',
 'layerview.common',
 'layerview.gcode',
 'layerview.simulation',
 'layerview.visualization',
 'layerview.visualization.nodes',
 'layerview.visualization.point_cloud',
 'layerview.visualization.world',
 'tests',
 'tests.gcode',
 'tests.visualization',
 'tests.visualization.point_cloud',
 'tests.visualization.world']

package_data = \
{'': ['*'],
 'layerview.app.dialog_info': ['res/md/*', 'res/md/img/*'],
 'layerview.visualization.nodes': ['assets/textures/*'],
 'tests': ['assets/gcode/*']}

install_requires = \
['Panda3D>=1.10.7,<2.0.0',
 'Pillow>=8.0.1,<9.0.0',
 'PyQt5>=5.15.2,<6.0.0',
 'QPanda3D>=0.2.7,<0.3.0',
 'numpy==1.19.3']

entry_points = \
{'console_scripts': ['layerview = layerview.cli:main']}

setup_kwargs = {
    'name': 'layerview',
    'version': '0.1.4',
    'description': 'LayerView is a G-code visualizer and inspector.',
    'long_description': '=========\nLayerView\n=========\n\n.. image:: https://img.shields.io/pypi/v/layerview?style=flat\n    :alt: Latest package version on PyPi\n    :target: https://pypi.org/project/layerview/\n\n.. image:: https://img.shields.io/pypi/status/LayerView\n    :alt: PyPI Status\n    :target: https://pypi.org/project/layerview/\n\n.. image:: https://img.shields.io/github/license/majabojarska/LayerView?style=flat\n    :target: https://github.com/majabojarska/LayerView/blob/main/LICENSE\n    :alt: License\n\n.. image:: https://img.shields.io/pypi/pyversions/layerview?style=flat\n    :alt: Supported Python versions\n    :target: https://pypi.org/project/layerview/\n\n.. image:: https://img.shields.io/pypi/implementation/layerview?style=flat\n    :alt: Supported Python implementation\n    :target: https://pypi.org/project/layerview/\n\n.. image:: https://img.shields.io/github/workflow/status/majabojarska/LayerView/build?label=build&style=flat\n    :alt: LayerView build status on GitHub Actions\n    :target: https://github.com/majabojarska/LayerView/actions/workflows/build.yml\n\n.. image:: https://img.shields.io/github/workflow/status/majabojarska/LayerView/docs?label=docs&style=flat\n    :alt: Documentation build status on GitHub Actions\n    :target: https://github.com/majabojarska/LayerView/actions/workflows/docs.yml\n\n.. image:: https://img.shields.io/github/workflow/status/majabojarska/LayerView/lint?label=lint&style=flat\n    :alt: Code linting status on GitHub Actions\n    :target: https://github.com/majabojarska/LayerView/actions/workflows/lint.yml\n\n.. image:: https://img.shields.io/readthedocs/layerview?label=Read%20the%20Docs&style=flat\n    :target: https://layerview.readthedocs.io/en/latest/\n    :alt: Read the Docs documentation Status\n\n.. image:: https://github.com/majabojarska/LayerView/raw/main/docs/_static/app.png\n    :alt: Main window of LayerView application.\n    :target: https://pypi.org/project/layerview/\n\nLayerView is a G-code file visualizer and inspector.\n\n* Source code: `majabojarska/LayerView <https://github.com/majabojarska/LayerView>`_\n* License: `GPLv3`_\n* Documentation: https://layerview.readthedocs.io.\n\nFeatures\n--------\n\n* 3D visualization and inspection of G-code files.\n\n  * Parametrized layer coloring.\n  * Adjustable visible layer range.\n  * Parameter inspection for model and layers.\n\n* Supports `RepRap`_ G-code flavour and its derivatives.\n  `Marlin`_ also works fine with the current feature set.\n* Hardware accelerated 3D rendering via `Panda3D`_.\n* Runs on x86_64 variants of Linux, Windows, MacOS.\n\nQuickstart\n----------\n\nInstall the latest LayerView package via pip:\n\n.. code-block:: console\n\n    pip install -U layerview\n\nRun LayerView:\n\n.. code-block:: console\n\n    layerview\n\nSee the `full documentation <https://layerview.readthedocs.io/en/latest/index.html>`_\nfor more details on `installation <https://layerview.readthedocs.io/en/latest/installation.html>`_\nand `usage <https://layerview.readthedocs.io/en/latest/usage.html>`_.\n\nContributing\n------------\n\nContributions are welcome, and they are greatly appreciated!\nEvery little bit helps, and credit will always be given.\nSee the `Contributing <https://layerview.readthedocs.io/en/latest/contributing.html>`_\npage for more details on how to contribute to this project.\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n.. _`GPLv3`: http://www.gnu.org/licenses/gpl-3.0.en.html\n.. _`Panda3D`: https://www.panda3d.org/\n.. _`RepRap`: https://reprap.org/wiki/G-code\n.. _`Marlin`: https://marlinfw.org/meta/gcode/\n.. _`CPython`: https://en.wikipedia.org/wiki/CPython\n',
    'author': 'Maja Bojarska',
    'author_email': 'majabojarska98@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/majabojarska/LayerView',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
