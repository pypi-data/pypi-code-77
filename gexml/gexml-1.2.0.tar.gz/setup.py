#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is the gexml setuptools script.
Originally developed by Ryan Kelly, 2009.

This script is placed in the public domain.

Source:: https://github.com/ampledata/gexml
Copyright:: Copyright (c) 2009-2011 Ryan Kelly
License:: MIT License
"""

import os
import sys

import setuptools


__title__ = "gexml"
__version__ = "1.2.0"
__author__ = "Ryan Kelly <oss@undef.net>"
__copyright__ = "Copyright (c) 2009-2011 Ryan Kelly"
__license__ = "MIT"


setuptools.setup(
    version=__version__,
    name=__title__,
    packages=[__title__],
    package_dir={__title__: __title__},
    url=f"https://github.com/ampledata/{__title__}",
    description="A dead-simple Object-XML mapper for Python.",
    author="Ryan Kelly",
    author_email="oss@undef.net",
    package_data={"": ["LICENSE.txt"]},
    license=open("LICENSE.txt").read(),
    long_description=open("README.rst").read(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup",
        "Topic :: Text Processing :: Markup :: XML",
    ]
)
