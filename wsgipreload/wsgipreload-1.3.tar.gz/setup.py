from __future__ import unicode_literals
from __future__ import absolute_import
from distutils.core import setup
import setuptools  # for extra commands

setup(
    name='wsgipreload',
    py_modules=['wsgipreload'],
    version='1.3',
    description='Preload WSGI applications by running a few URLs through the app immediately when it starts',
    author='Dave Brondsema',
    author_email='dave@brondsema.net',
    license='Apache License',
    url='https://sourceforge.net/p/wsgipreload/',
    requires=['webob'],
)
