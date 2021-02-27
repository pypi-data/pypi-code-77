"""Setup for imea package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Nils Kroell",
    author_email="nils.kroell@ants.rwth-aachen.de",
    name='imea',
    license="MIT",
    description='imea is an open source Python package for extracting 2D and 3D shape measurements from images.',
    version='v0.2.2',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://git.rwth-aachen.de/ants/sensorlab/imea',
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=['numpy', 'scipy', 'scikit-image', 'opencv-python', 'pandas'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Image Processing'
    ],
)