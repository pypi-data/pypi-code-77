import os
import codecs
import setuptools
import voken

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines() if not line.startswith('#')]


setuptools.setup(
    name='voken',
    python_requires='>=3.8.0',
    version=voken.__version__,
    description="For Voken Project",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    author="@voken1000g",
    author_email='pmvoken@protonmail.com',
    url='https://github.com/voken1000g/pypi_voken/',
    packages=setuptools.find_packages(),
    install_requires=read_requirements('requirements.txt'),
    include_package_data=True,
    license="GPLv3+",
    keywords=[
        "voken",
        "voken1000g",
        "crypto",
        "cryptography"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
)
