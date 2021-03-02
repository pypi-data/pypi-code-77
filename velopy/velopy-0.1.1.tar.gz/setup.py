# Usage:
# python setup.py sdist
# python setup.py install

from setuptools import setup, find_packages

config = {
    'name': 'velopy',
    'version': '0.1.1',
    'license': 'BSD New License',
    'description': 'Library for simple calculations with respect to road cycling and training',
    'keywords': ['cycling', 'training with power', 'training zones', 'TSS', 'PMC', 'power model'],
    'author': 'Christoph Ernst',
    'url': 'https://gitlab.com/ce72/velo',
    'packages': find_packages(),
    'include_package_data': True,
    'py_modules': ['velopy'],
    'python_requires': '>3.6'
}

setup(**config)
