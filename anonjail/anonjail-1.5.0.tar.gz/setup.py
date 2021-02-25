#!/usr/bin/python3
from setuptools import setup
from setuptools.command.install import install as anoninstall
import os
import sys

VERSION = "1.5.0"

try:
    import pypandoc
    long_description = pypandoc.convert_file("README.md", "rst")
except:
    long_description = ""

class InstallingClass(anoninstall):
    user_options = anoninstall.user_options +  [('autoinstall=', 'y', 'auto install all deps.')]
    
    def initialize_options(self):
        anoninstall.initialize_options(self)
        self.autoinstall = 'y'

    def finalize_options(self):
         anoninstall.finalize_options(self)

    def run(self):
        global autoinstall
        autoinstall = self.autoinstall
        if self.autoinstall == 'y':
            os.system("sudo sh -c 'scripts/anonjail-install.sh'")
        anoninstall.run(self)


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