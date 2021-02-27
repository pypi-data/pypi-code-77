#!/usr/bin/python3
from setuptools import setup
from setuptools.command.install import install
import os
from os import path
from subprocess import call

VERSION = "1.6.2"

try:
    import pypandoc
    long_description = pypandoc.convert_file("README.md", "rst")
except:
    long_description = ""

setup(
    name = 'anonjail',
    version=VERSION,
    description="Control firejail and tor desktop integration.",
    long_description=long_description,
    url="https://boards.420chan.org/",
    license="GPLv2+",   
    py_modules=["anonjail"],
    install_requires=["click"],
    entry_points={"console_scripts": ["anonjail=anonjail:cli"]},
    scripts=['scripts/install.bash'],
    author="K",
    author_email="anon@anon.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Security"
    ],
    keywords="firejail and tor sandbox desktop integration",
)