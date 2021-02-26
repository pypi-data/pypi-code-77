#import pathlib
from setuptools import setup

# The directory containing this file
HERE = ""
#pathlib.Path(__file__).parent

# The text of the README file
README = open("./README.md").read()

# This call to setup() does all the work
setup(
    name="common-io-python",
    version="0.0.1",
    description="h4ck3d",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://pudim.com.br",
    author="Zero Cool",
    author_email="zcoollllllllllll@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["common-io-python"],
    include_package_data=True,
    install_requires=[],
)
