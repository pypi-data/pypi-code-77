import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KuulKaggleTools", # Replace with your own username
    version="0.0.1",
    author="Ted Troxell",
    author_email="ted@tedtroxell.com",
    description="Just some kuul Kaggle tools I like to use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tedtroxell/KaggleTools",
    project_urls={
        "Bug Tracker": "https://github.com/tedtroxell/KaggleTools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)