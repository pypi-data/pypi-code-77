from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='phlocation2',
    version='0.0.1',
    description='Area locator inside the Philippines',
    long_description=open('README.txt').read(),
    url='',
    author='Jorge Rojas III',
    author_email='jorgereluniarojas@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='phlocation',
    packages=find_packages(),
    install_requires=['']
)