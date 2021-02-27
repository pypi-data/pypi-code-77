from setuptools import setup, find_packages

setup(
    name="person_age",
    version="0.2.0",
    author="Łukasz Tkaczyk",
    author_email="lukasztkaczyk@hotmail.com",
    packages=find_packages(),
    python_requires=">=3.7",
    description="Our super useful library",
    install_requirements=["pytest==6.0.0","black","wheel"],
)
