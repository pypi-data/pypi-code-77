"""
# A sample import catcher that redirects clients to the proper package #

This library helps users of Arcesium services avoid using improperly installed
Arcesium Python Client libraries or [falling prey to dependency chain attacks.](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610)
"""

from setuptools import setup

setup(
    name="arcesium-python",
    version="0.0.1",
    description="Arcesium Python Client redirector",
    url="http://arcesium.com",
    author="Arcesium Inc.",
    author_email="help@arcesium.com",
    long_description=__doc__,
    long_description_content_type="text/markdown",
    license="Proprietary",
    packages=["arcesium"],
    classifiers=[
        "Intended Audience :: Financial and Insurance Industry",
        "License :: Other/Proprietary License",
    ],
)
