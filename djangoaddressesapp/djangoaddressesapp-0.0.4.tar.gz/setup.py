from setuptools import setup

setup(
    name = 'djangoaddressesapp',
    version = '0.0.4',
    author = 'Julian de Almeida Santos',
    author_email = 'julian.santos.info@gmail.com',
    packages=[
        'djangoaddressesapp',
        'djangoaddressesapp.management',
        'djangoaddressesapp.management.commands',
        'djangoaddressesapp.migrations',
    ],
    description = 'Django app to register addresses.',
    long_description = 'Django app to register addresses.',
    url = 'https://github.com/juliansantosinfo/djangoaddressesapp.git',
    project_urls = {
        'Código fonte': 'https://github.com/juliansantosinfo/djangoaddressesapp.git',
        'Download': 'https://github.com/juliansantosinfo/djangoaddressesapp/archive/0.0.4.zip'
    },
    install_requires=[
        'djangosimplemodels',
    ],
    license = 'MIT',
    keywords = 'addresses app django',
)
