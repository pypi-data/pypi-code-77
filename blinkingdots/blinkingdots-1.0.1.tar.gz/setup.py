from setuptools import setup, find_packages

with open(file="README.md", mode="r") as readme_handle:
    long_description = readme_handle.read()

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name="blinkingdots",
    version='1.0.1',
    description='Principally a module that allows you to use a custom loading bar',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/SciRcher/BlinkingDots",
    author="scircher",
    author_email="scircher@gmail.com",
    license='MIT',
    classifiers=classifiers,
    keywords='loadingbars',
    packages=find_packages(),
    install_requires=['']
)