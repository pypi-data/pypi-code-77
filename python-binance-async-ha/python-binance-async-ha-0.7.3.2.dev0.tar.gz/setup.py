#!/usr/bin/env python
from setuptools import setup
import codecs
import os
import re


with codecs.open(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'binance',
            '__init__.py'
        ), 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'$", fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

setup(
    name='python-binance-async-ha',
    version=version,
    packages=['binance'],
    description='Async Binance REST API Python implementation',
    url='https://github.com/DevSecNinja/python-binance',
    author='Sam McHardy',
    license='MIT',
    author_email='',
    install_requires=[
        'requests', 'six', 'pyOpenSSL', 'service-identity', 'dateparser', 'urllib3', 'chardet', 'certifi',
        'cryptography', 'aiohttp'
    ],
    keywords='binance exchange rest api bitcoin ethereum btc eth neo',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
