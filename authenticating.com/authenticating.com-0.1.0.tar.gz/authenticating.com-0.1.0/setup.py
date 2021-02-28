from setuptools import find_packages, setup


setup(
    name = 'authenticating.com',
    packages = find_packages(exclude=("tests",)),
    version = '0.1.0',
    description = 'authenticating.com-python',
    author = 'SmokingGoaT',
    license = 'MIT',
    url = 'https://github.com/SmokingTheGoaT/authenticating.com-python',
    install_requires = [
        'requests',
        'requests_oauthlib',
        'simplejson',
    ]
)