import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EmailSender-jma", # Replace with your own username
    version="0.0.1",
    author="Jinghan Ma",
    author_email="jinghan.m@helium10.com",
    description="A package to send auto email",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jm-h10/utility_jma/AutoEmailSender",
    project_urls={
        "Bug Tracker": "https://github.com/jm-h10/utility_jma/AutoEmailSender"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
