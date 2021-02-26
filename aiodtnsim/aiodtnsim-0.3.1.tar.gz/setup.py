#!/usr/bin/env python
# encoding: utf-8

"""Setup script for the aiodtnsim module."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiodtnsim",
    version="0.3.1",
    author="Felix Walter",
    author_email="code@felix-walter.eu",
    description=(
        "A framework for performing DTN simulations based on asyncio."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/d3tn/aiodtnsim",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "tqdm",
        "dtn-tvg-util",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
