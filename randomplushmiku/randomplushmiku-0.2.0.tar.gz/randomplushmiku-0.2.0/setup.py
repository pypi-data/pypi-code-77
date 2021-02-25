from setuptools import find_packages, setup

setup(
    name="randomplushmiku",
    packages=find_packages(include=["mypythonlib"]),
    version="0.2.0",
    description="My first Python library,it downloads random images of plush mikus to a local directory.",
    author="Nucl3arsn3k",
    license="MIT",
    install_requires=["requests", "bs4"],
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    setup_requires=["pytest-runner"],
    tests_require=["pytest==4.4.1"],
    test_suite="tests",
)