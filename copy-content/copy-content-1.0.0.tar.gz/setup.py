import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="copy-content",
    version="1.0.0",
    author="Muhammad Faizan Qureshi",
    author_email="qfaizan401@gmail.com",
    description="This package is an automated tool for coping multiple files one folder/directory to another with your desired extension.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qfaizan401/pyPackage-copy-contain",
    project_urls={
        "Bug Tracker": "https://github.com/qfaizan401/pyPackage-copy-contain/issues",
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)