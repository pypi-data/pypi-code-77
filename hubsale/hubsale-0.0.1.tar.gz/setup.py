from setuptools import setup

with open("HubSale/HubSale-api/README.md", "r") as fh:
    readme = fh.read()

setup(name='hubsale',
    version='0.0.1',
    url='https://github.com/Fr4ncisTaylor/HubSale-api',
    license='Apache License',
    author='Francis Taylor',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='Francistrapp2000@gmail.com',
    keywords='hubsale',
    description=u'Hubsale Api python connection',
    packages=['HubSale/HubSale-api/Hubsale'],
    install_requires=['requests'],)