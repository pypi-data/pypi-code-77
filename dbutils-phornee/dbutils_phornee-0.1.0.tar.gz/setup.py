import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dbutils_phornee",
    version="0.1.0",
    author="Ismael Raya",
    author_email="phornee@gmail.com",
    description="DB management wrapper over mariaDB, mongoDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Phornee/dbutils_phornee",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'mariadb>=1.0.5',
        'pymongo>=3.11.3',
        'dnspython>=2.1.0'
    ],
    python_requires='>=3.6',
)