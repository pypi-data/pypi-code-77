import pathlib
from setuptools import find_packages, setup
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name="csv-processor",
    version="1.0.0",
    description="Python 3+ CSV file processor",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Harvard90873",
    author_email="harvard90873@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=("tests", "build")),
    include_package_data=False,
    install_requires=["python-algorithms-3x", "termcolor", "data-structures3x", "and-or-not", "spell-checker", "word-scramble"],
)