#!/usr/bin/env python

import os
import sys

from setuptools import setup, find_packages

os.chdir(os.path.dirname(sys.argv[0]) or ".")

classifiers = [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
]

setup(
    name='pijavski',
    version='0.0.1',
    description='Python CFFI bindings for Pijavski C++ function to calculate minimum of a given function.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    #url='',
    author='Santiago Velasquez',
    author_email='js.velasquez123@gmail.com',
    license='MIT',
    lincese_file='LICENSE',
    classifiers=classifiers,
    packages=find_packages(),
    #py_modules=['pijavski'],
    install_requires=['cffi>=1.0.0'],
    setup_requires=['cffi>=1.0.0'],
    cffi_modules=['pij_build.py:ffibuilder'],
    #extras_require={
    # 	"dev": [
    #	    "pytest>=3.7",
    #	],
    #}
)
