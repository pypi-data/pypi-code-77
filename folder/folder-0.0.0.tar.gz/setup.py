import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
setup(
    name = "folder",
    version = '0.0.0',
    license = 'MIT',
    long_description = README,
    long_description_content_type="text/markdown",
    author = "Aditta Das Nishad",
    author_email = "nishad009adi@gmail.com",
    packages=['folder']    
)