from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyautoai",
    version="0",
    author="Christian O'Leary",
    author_email="pyautoai@gmail.com",
    description='An auto-ML/AI package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/chris.oleary/pyautoai',
    packages=find_packages(),
    install_requires=[
        # 'numpy!=1.9.4',
        'numpy==1.9.3',
        'setuptools',
        'scikit-learn>=0.22.0',
        'imbalanced-learn',
        'statsmodels',
        'scipy',
        # 'scipy>=0.14.1',
        'pandas',
        'joblib',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
