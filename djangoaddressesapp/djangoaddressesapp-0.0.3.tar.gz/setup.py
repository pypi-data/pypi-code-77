from setuptools import setup, find_packages

setup(
    name = 'djangoaddressesapp',
    version = '0.0.3',
    author = 'Julian de Almeida Santos',
    author_email = 'julian.santos.info@gmail.com',
    packages=find_packages(),
    description = 'Django app to register addresses.',
    long_description = 'Django app to register addresses.',
    url = 'https://github.com/juliansantosinfo/djangoaddressesapp.git',
    project_urls = {
        'Código fonte': 'https://github.com/juliansantosinfo/djangoaddressesapp.git',
        'Download': 'https://github.com/juliansantosinfo/djangoaddressesapp/archive/0.0.3.zip'
    },
    install_requires=[
        'djangosimplemodels',
    ],
    license = 'MIT',
    keywords = 'addresses app django',
)
