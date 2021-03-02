from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'CLI for highlighting tab spaces in a file'

# Setting up
setup(
    name="Taby",
    version=VERSION,
    author="Sombodee (Landon Hutchins)",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'tabs', 'highlight', 'CLI'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)