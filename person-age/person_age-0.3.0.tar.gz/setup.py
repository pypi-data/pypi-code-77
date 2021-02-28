from setuptools import setup, find_packages

setup(
    name="person_age",
    version="0.3.0",
    author="Łukasz Tkaczyk",
    author_email="lukasztkaczyk@hotmail.com",
    packages=find_packages(),
    python_requires=">=3.7",
    description="Our super useful library",
    install_requires=["pytest==6.0.0", "black", "wheel"],
    entry_points="""
    [console_scripts]
    person_age=person.main:start_app
    """,
)
