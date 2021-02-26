from setuptools import setup

setup(
    name = 'fakedadosbr',
    version = '0.0.1',
    author = 'Julian de Almeida Santos',
    author_email = 'julian.santos.info@gmail.com',
    packages = ['fakedadosbr'],
    description = 'Generic generator fake data for application and api development.',
    long_description = 'Generic generator fake data for application and api development.',
    url = 'https://github.com/juliansantosinfo/fakedadosbr.git',
    project_urls = {
        'Código fonte': 'https://github.com/juliansantosinfo/fakedadosbr.git',
        'Download': 'https://github.com/juliansantosinfo/fakedadosbr/archive/0.0.1.zip'
    },
    license = 'MIT',
    keywords = ['generic', 'fake', 'data', 'generator','application', 'api', 'development'],
    install_requires = ['beautifulsoup4']
)
