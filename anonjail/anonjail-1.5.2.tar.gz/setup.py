#!/usr/bin/python3
from setuptools import setup
from setuptools.command.install import install as anoninstall
import os
from os import path

VERSION = "1.5.2"

try:
    import pypandoc
    long_description = pypandoc.convert_file("README.md", "rst")
except:
    long_description = ""

here = path.abspath(path.dirname(__file__))

def PostInstall():
    from subprocess import check_call
    os.system("scripts/anonjail-install.sh")

class InstallingClass(anoninstall):
    def run(self):      
        anoninstall.run(self)
        PostInstall()
               
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
    #scripts=['scripts/anonjail-install.sh'],
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
    cmdclass={
        'install': InstallingClass,
    },
)