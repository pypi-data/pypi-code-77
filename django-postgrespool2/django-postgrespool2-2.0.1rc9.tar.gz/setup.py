#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from django_postgrespool2 import __version__, __author__
import codecs

required = [
    "sqlalchemy>=1.1",
    "django>=2.2",
]

setup(
    name="django-postgrespool2",
    version=__version__,
    description="Postgres Connection Pooling for Django.",
    long_description=codecs.open("README.rst", "r", "utf-8").read(),
    author=__author__,
    author_email="malexey1984@gmail.com",
    url="https://github.com/lcd1232/django-postgrespool2",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=required,
    license="MIT",
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Topic :: Database",
    ),
)
