#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='unzlib',
    version='0.0.1',
    description='a python command that can decompress the zlib data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ramwin/unzlib',
    author='Xiang Wang',
    author_email='ramwin@qq.com',
    license='GNU',
    keywords='unzlib pipe zlib decompress',
    install_requires=[''],
    scripts=[
        "unzlib/unzlib.py",
    ]
)
