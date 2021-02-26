#!/usr/bin/env python
import re
from os.path import join

from setuptools import setup, Extension, find_packages
import sys
from distutils import ccompiler

include_dirs = []
libraries = []

sources = [
    'mtsmultitool/lz4.c',
    'mtsmultitool/bsdiff.c'
]

compiler = ccompiler.get_default_compiler()

extra_link_args = []
extra_compile_args = []

if compiler == 'msvc':
    extra_compile_args = ['/Ot', '/Wall', '/wd4711', '/wd4820']
elif compiler in ('unix', 'mingw32'):
    extra_compile_args = ['-O3', '-Wall', '-Wundef']
else:
    print('Unrecognized compiler: {0}'.format(compiler))
    sys.exit(1)

mtsmultitool_ext = Extension('mtsmultitool.bsdiff',
                           sources,
                           extra_compile_args=extra_compile_args,
                           extra_link_args=extra_link_args,
                           libraries=libraries,
                           include_dirs=include_dirs)

install_requires = []

kwds = {}
try:
    readme = open('README.md').read()
    index = readme.find('[//]: # (End long description)')
    kwds['long_description'] = readme[:index-1]
    kwds['long_description_content_type'] = "text/markdown"
except IOError:
    pass

# Read version from bsdiff/__init__.py
pat = re.compile(r'__version__\s*=\s*(\S+)', re.M)
data = open(join('mtsmultitool', '__init__.py')).read()
kwds['version'] = eval(pat.search(data).group(1))

setup(
    name="mtsmultitool",
    author="MultiTech Systems, Inc.",
    author_email="",
    url="",
    license="Proprietary",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Environment :: Console",
        "Programming Language :: C",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
    ],
    install_requires=['ecdsa>=0.15', 'cbor>=1.0.0', 'pyserial>=3.5', 'xmodem>=0.4.6'],
    python_requires='>=3.7',
    description="Library and command line tool for working with Multitech products.",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={
        'mtsmultitool': ['*.c', '*.h'],
    },
    ext_modules=[mtsmultitool_ext],
    entry_points={
        'console_scripts': [
            'multitool = mtsmultitool.cli:main'
        ],
    },
    **kwds
)
