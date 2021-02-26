import setuptools

setuptools.setup(
    name='microt_preprocessing',
    version='0.0.3',
    description='A package that transforms raw sensor data collected from Time study app into intermediate CSV file '
                'for analysis of various purposes',
    url='https://bitbucket.org/mhealthresearchgroup/microt_preprocessing/src/master/',
    long_description='long_description',
    long_description_content_type="text/markdown",
    author='Jixin Li, Aditya Ponnada',
    author_email='li.jix@northeastern.edu',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7'
)