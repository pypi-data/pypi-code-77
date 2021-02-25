from setuptools import find_packages, setup


setup(
    name="horo",
    packages=find_packages(include=["horo"]),
    version="1.0.1",
    description="A program that displays your horoscope right from the terminal",
    author="George Munyoro",
    author_email="george.guva@outlook.com",
    license="MIT",
    entry_points="""
    [console_scripts]
    horo=horo.__main__:main
    """
)

