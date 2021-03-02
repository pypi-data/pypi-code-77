import setuptools


def get_long_description():
    with open('README.md', 'rb') as f:
        return f.read().decode('utf-8')


with open('requirements.txt') as infile:
    requirements = infile.read().splitlines()

setuptools.setup(
    name="upload_manager",
    version="0.0.2",
    author="bb-tech",
    author_email="asodiyadharmesh@gmail.com",
    description="Upload manager",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/Bigbasket/bbuploadmanager",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Framework :: Django :: 2.1",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires='>=3.6',
    install_requires=requirements
)
