from setuptools import setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ssjson",
    version="1.0.9",
    description="ssjson is JSON based python library with various json operation",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Sandeeppushp/ssjson",
    author="Sandeep Pushp",
    author_email="sandeepkumarpushp@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["ssjson"],
    python_requires='>=3.2',
    include_package_data=True,
    install_requires=["pathlib"],
)