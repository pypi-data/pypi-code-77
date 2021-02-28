#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os

from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


setup(
    name='django-js-reverse-thread',
    version='0.0.1',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Django',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT',
    description='Javascript url handling for Django that doesn\'t hurt.',
    long_description=read('README.rst'),
    author='Thread Engineering',
    author_email='tech@thread.com',
    url='https://github.com/thread/django-js-reverse',
    download_url='https://pypi.python.org/pypi/django-js-reverse-thread/',
    packages=find_packages(),
    package_data={
        'django_js_reverse': [
            'templates/django_js_reverse/*',
        ]
    },
    install_requires=[
        'Django>=1.5',
    ]
)
