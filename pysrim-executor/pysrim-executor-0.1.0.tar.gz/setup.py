# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['srim', 'srim.executor']

package_data = \
{'': ['*']}

install_requires = \
['pysrim>=0.5.10,<0.6.0']

setup_kwargs = {
    'name': 'pysrim-executor',
    'version': '0.1.0',
    'description': 'Abstracted executor for PySRIM',
    'long_description': "# pysrim-docker\n[![pypi-badge][]][pypi] \n\n[pypi-badge]: https://img.shields.io/pypi/v/pysrim-docker\n[pypi]: https://pypi.org/project/pysrim-docker\n\nDocker executor for PySRIM\n\n## Getting Started\nTo use this package, simply remove calls to `run()` method of `SR` and `TRIM`, and replace them with a call to the executor `run` dispatch method, e.g.:\n\n```python\nfrom srim.executor import DockerExecutor\nfrom srim import TRIM\n\nexecutor = DockerExecutor()\n\ntrim = TRIM(...)\nresult = executor.run(trim)\n```\n\nOut of the box, the `DockerExecutor` uses the `costrouc/srim` Docker image, and writes the input and output files to a temporary directory. \n\n### Example\n```python3\nfrom srim.executor import DockerExecutor\nfrom srim import Ion, Layer, Target, TRIM\n\nfrom matplotlib import pyplot as plt\n\n# Construct a 3MeV Nickel ion\nion = Ion('Ni', energy=3.0e6)\n\n# Construct a layer of nick 20um thick with a displacement energy of 30 eV\nlayer = Layer({\n        'Ni': {\n            'stoich': 1.0,\n            'E_d': 30.0,\n            'lattice': 0.0,\n            'surface': 3.0\n        }}, density=8.9, width=20000.0)\n\n# Construct a target of a single layer of Nickel\ntarget = Target([layer])\n\n# Initialize a TRIM calculation with given target and ion for 25 ions, quick calculation\ntrim = TRIM(target, ion, number_ions=25, calculation=1)\n\n# Create executor and run TRIM\nexecutor = DockerExecutor()\nresult = executor.run(trim)\n\n# Pull out ionization\nioniz = result.ioniz\n\n# Plot results\n_, ax = plt.subplots()\nax.plot(ioniz.depth, ioniz.ions, label='Ionization from Ions')\nax.plot(ioniz.depth, ioniz.recoils, label='Ionization from Recoils')\nplt.show()\n```\n\n## Why?\nThere are a number of different ways that SRIM can be invoked to run simulations. Unix-like OS users have the option of using `wine` with or without `xvfb`.\nWindows users can directly call the binaries. Docker users can choose to defer to a pre-built SRIM container.\n\nBy abstracting the executor from the SRIM input file generation, executors can easily be swapped in and out, or extended as necessary.",
    'author': 'Angus Hollands',
    'author_email': 'goosey15@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agoose77/pysrim-executor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
