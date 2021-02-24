from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'String analysis package.'
LONG_DESCRIPTION = 'A package that takes as input a string stream and a query word and returns which word ' \
                   'on the stream is most similar to the query word. String similarity is measured by the ' \
                   'Jaro distance.'

# Setting up
setup(
    name="ramon-stringanalysis",
    version=VERSION,
    author="Ramon Duraes",
    author_email="ramongduraes@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    py_modules=["stringanalysis"],
    package_dir={'': 'stringanalysis'},
    install_requires=['jellyfish'],
    keywords=['python', 'string', 'take'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English"
    ]
)
