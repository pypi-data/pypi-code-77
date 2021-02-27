from setuptools import find_packages, setup
setup(
    name='fastapi_quickstart',
    version='0.3',
    packages=find_packages(),
    py_modules=['fastapi_quickstart'],
    author='Lokendra Bairwa',
    author_email='lokendrabairwa@gmail.com',
    url='https://www.lokendrabohra.tech',
    description='Common Helper functions which gets you kickstart with your fastapi development.',
    download_url='https://github.com/lokendra1704/fastapi_quickstart/archive/v_03.tar.gz',
    install_requires=[
        'fastapi[all]',
        'pydantic',
        'python-multipart',
        'SQLAlchemy',
        'passlib',
        'bcrypt',
        'fastapi-jwt-auth',
        'python-jose[cryptography]'
    ]
)


# pip install fastapi-quickstart==0.2
