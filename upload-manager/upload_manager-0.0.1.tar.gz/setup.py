import setuptools

with open('requirements.txt') as infile:
    requirements = infile.read().splitlines()

setuptools.setup(
    name="upload_manager",
    version="0.0.1",
    author="bb-tech",
    author_email="asodiyadharmesh@gmail.com",
    description="Upload manager",
    url="https://github.com/Bigbasket/bbuploadmanager",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
    install_requires=requirements
)
