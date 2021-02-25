"""Mars Rovers Catalogue setup."""

import re

from setuptools import setup, find_packages


with open('catalog/version.py') as f:
    __version__ = re.findall(
        r'__version__ = \'(\d+\.\d+\.\d+)\'',
        f.read()
    )[0]

with open('README.md', encoding='utf-8') as f:
    readme = f.read()


setup(
    name='mars-rovers-catalog',
    version=__version__,
    description='Mars Rovers Catalog toolbox',
    author='Benoit Seignovert',
    author_email='benoit.seignovert@univ-nantes.fr',
    url='https://gitlab.univ-nantes.fr/mars-rovers/catalog/',
    license='BSD',
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'Pillow>=8.0',
        'ipython',
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords=['nasa', 'catalog', 'mars2020', 'perseverance', 'msl', 'curiosity'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
    ],
    long_description=readme,
    long_description_content_type='text/markdown',
)
