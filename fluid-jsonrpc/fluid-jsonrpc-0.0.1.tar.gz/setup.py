from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="fluid-jsonrpc",
    author="Blinktrade",
    version="0.0.1",
    install_requires=["requests"],
    license="BSD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["fluid"],
    url="https://github.com/blinktrade/fluid-jsonrpc",
)
