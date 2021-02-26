from pathlib import Path
from setuptools import setup

current_dir = Path(__file__).parent
readme = current_dir.joinpath("README.md").read_text()

setup(
    name="jsonx-py",
    version="1.0.0",
    description="JSON flattening and expansion",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/getformative/jsonx-py",
    author="Formative",
    author_email="hello@getformative.com",
    license="MIT",
    packages=["jsonx"],
)
