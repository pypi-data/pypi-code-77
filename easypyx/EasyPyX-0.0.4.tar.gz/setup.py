#oding = utf-8
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='EasyPyX',
    version='0.0.4',
    packages=['easyweb'],
    url='',
    license='',
    author='Yubadboy',
    author_email='2025677540@qq.com',
    description='so easy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['flask']
)
