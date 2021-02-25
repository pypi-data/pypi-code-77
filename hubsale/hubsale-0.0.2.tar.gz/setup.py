from setuptools import setup


setup(name='hubsale',
    version='0.0.2',
    url='https://github.com/Fr4ncisTaylor/HubSale-api',
    license='Apache License',
    author='Francis Taylor',
    long_description_content_type="text/markdown",
    author_email='Francistrapp2000@gmail.com',
    keywords='hubsale',
    description=u'Hubsale Api python connection',
    packages=['HubSale/HubSale-api/Hubsale'],
    install_requires=['requests'],)