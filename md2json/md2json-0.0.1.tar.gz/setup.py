from setuptools import find_packages, setup

from md2json.version import VERSION

long_description = ""
with open("README.md") as ifp:
    long_description = ifp.read()

setup(
    name="md2json",
    version=VERSION,
    packages=find_packages(),
    install_requires=["mistune>=2.0.0rc1"],
    extras_require={
        "dev": ["black", "mypy", "wheel", "setuptools"],
        "distribute": ["twine"],
    },
    description="md2json: md2json and json2md",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Neeraj Kashyap",
    author_email="neeraj@bugout.dev",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
    ],
    url="https://github.com/bugout-dev/md2json",
    entry_points={},
)
