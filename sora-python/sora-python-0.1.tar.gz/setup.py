import os

from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.sdist import sdist
import pkg_resources

desc = "Python client for Sora ID: soraid.com"

setup(
    name=f'sora-python',
    version='0.1',
    author="Sora ID, Inc.",
    author_email="support@soraid.com",
    description="Python client for Sora ID: soraid.com",
    long_description=desc,
    classifiers=[
    	"Programming Language :: Python :: 3",
    	"Operating System :: OS Independent",
    ],
    packages=["sora"],
    python_requires=">=3.7",
    install_requires=['requests>=2.24'],
)
