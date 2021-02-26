import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sthlmkollektivtrafik",
    version="0.1.5",
    author="William Grunder",
    author_email="William.grunder@gmail.com",
    description="Python library for easier use of www.trafiklab.se api's'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WIGRU/sthlmkollektivtrafik",
    packages=setuptools.find_packages(),
    install_requires=[
          'requests',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)