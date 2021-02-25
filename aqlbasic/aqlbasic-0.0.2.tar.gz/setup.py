from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'A simple package to connect to mysql easily'
LONG_DESCRIPTION = 'A simple package to connect to mysql easily'

# Setting up
setup(
    name="aqlbasic",
    version=VERSION,
    author="Pratyush Roy",
    author_email="<pratyushroy.whj@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['mysql.connector'],
    keywords=['python', 'sql', 'mysql', 'database', 'data'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)