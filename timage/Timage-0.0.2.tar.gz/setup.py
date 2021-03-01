from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Hide text into image'
LONG_DESCRIPTION = 'A package that allows to hide text into image send it public and then get text from image'

# Setting up
setup(
    name="Timage",
    version=VERSION,
    author="Hayk Sardaryan",
    author_email="<hayk4536@gmail.com>",
    description=DESCRIPTION,
    url='https://github.com/HaykSD/Text-into-image',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy', 'Pillow'],
    keywords=['python', 'steganography', 'text image', 'text coder',],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
