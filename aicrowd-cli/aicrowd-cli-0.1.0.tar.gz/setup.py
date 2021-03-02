#!/usr/bin/env python
"""
Build and install the CLI
"""

from pathlib import Path

from setuptools import setup, find_packages

import versioneer

long_description = r"""
aicrowd-cli

A CLI app to interact with AIcrowd
"""

current_dir = Path(__file__).resolve().parent
version = versioneer.get_version()

with open(str(current_dir / "requirements" / "build.txt")) as reqs_file:
    reqs = reqs_file.read().split()

setup(
    name="aicrowd-cli",
    description="A CLI app to interact with AIcrowd",
    long_description=long_description,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version=version,
    cmdclass=versioneer.get_cmdclass(),
    install_requires=reqs,
    entry_points={
        "console_scripts": [
            "aicrowd=aicrowd.cli:cli",
        ]
    },
    python_requires=">=0.0.1",
    license="MIT",
    author="Yoogottam Khandelwal",
    author_email="yoogottamk@outlook.com",
    url="https://github.com/AIcrowd/aicrowd-cli",
    download_url=f"https://github.com/AIcrowd/aicrowd-cli/archive/{version}.tar.gz",
    keywords=["AIcrowd", "CLI"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    include_package_data=True,
)
