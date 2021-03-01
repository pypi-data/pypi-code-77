from pathlib import Path

from setuptools import setup

setup(
    name="sendgrify",
    version="1.0.1",
    url="https://github.com/sdelquin/sendgrify.git",
    author="Sergio Delgado Quintero",
    author_email="sdelquin@gmail.com",
    license='MIT',
    description="SendGrid for Humans",
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=["sendgrify"],
    install_requires=["sendgrid"],
    python_requires='>=3.6',
)
