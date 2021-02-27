from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Basic toolkit for neural networks'
LONG_DESCRIPTION = 'A package that allows to build simple neural networks and train them.'

# Setting up
setup(
    name="minnn",
    version=VERSION,
    author="Wadood Abdul",
    author_email="<wadood3003@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires= ['numpy'],
    keywords=['python', 'neural networks', 'dnn', 'deep learning'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
