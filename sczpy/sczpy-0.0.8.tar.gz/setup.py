from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sczpy',
    version='0.0.8',
    description='Azure Percept Model Management Python SDK',
    py_modules=["sczpy"],
    package_dir={'': 'src'},
    url="https://github.com/microsoft/azure-percept-advanced-development/secured_locker",
    author="Microsoft Corporation",
    author_email="SCZAIMLDataProtect@microsoft.com",
    license='MIT License',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "pycryptodome>=3.9.8",
        "requests>=2.24.0",
        "azure-keyvault-secrets>=4.2.0",
        "azure-core>=1.8.0",
        "azure-identity<1.3.0,>=1.2.0",
        "cryptography>=3.2",
        "adal>=1.2.4", 
        "PyJWT>=1.7.1",
        "opentelemetry-api==0.15b0",
        "opentelemetry-sdk==0.15b0"
    ],
    extras_require = {
        "dev": [
            "pytest>=3.7",
        ],
    }
)