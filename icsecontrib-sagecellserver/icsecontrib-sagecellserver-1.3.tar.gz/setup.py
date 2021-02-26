import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="icsecontrib-sagecellserver", # Replace with your own username
    version="1.3",
    author='Krzysztof Kajda',
    author_email='kajda.krzysztof@gmail.com',
    description='Sphinx sagecellserver extension',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/kriskda/sphinx-sagecell",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6'
)