from setuptools import setup, find_packages, Distribution

class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True

setup(
    name = "hqchart",
    version = "1.0.11",
    author = "jones2000",
    author_email = "jones_2000@163.com",
    description = "HQChartPy2 C++",
    license = "Apache License 2.0",
    keywords = "HQChart HQChartPy",
    url = "https://github.com/jones2000/HQChart",

    install_requires=['requests', 'pandas', 'numpy'],

    packages=find_packages(include=["hqchart",'hqchart.*py']), 

    package_data  = { "hqchart":["*.dll", "HQChartPy2.pyd"] },
   
    classifiers=
    [
        'Operating System :: Microsoft :: Windows'
    ],
)