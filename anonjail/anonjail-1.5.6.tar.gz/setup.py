#!/usr/bin/python3
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import os
from os import path

VERSION = "1.5.6"

try:
    import pypandoc
    long_description = pypandoc.convert_file("README.md", "rst")
except:
    long_description = ""

here = path.abspath(path.dirname(__file__))

def PostInstall():
    from subprocess import check_call
    os.system("scripts/anonjail-install.sh")

class install(_install):
    def initialize_options(self):
        _install.initialize_options(self)

    def finalize_options(self):
        _install.finalize_options(self)

    def run(self):      
        _install.run(self)
        self.execute(PostInstall,self.install_lib, msg="Installing external dependencies")
               
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
    scripts=['scripts/anonjail-install.sh'],
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