import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

SRC = 'src'
setuptools.setup(
    name="ioutliers",
    version="0.1.2",
    author="ira",
    author_email="ira.saktor@gmail.com",
    description="Package to easily detect or remove potential outliers",
    long_description=long_description,
    package_dir={'': SRC},
    long_description_content_type="text/markdown",
    url="https://gitlab.com/i19/outliers",
    packages=setuptools.find_packages(SRC),
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'pandas',
          'rrcf',
          'sklearn',
          'idfops'
      ],
    python_requires='>=3.6',
)
