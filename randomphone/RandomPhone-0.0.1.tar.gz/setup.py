import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='RandomPhone',
    version='0.0.1',
    author='Richard Franks',
    author_email='richard.franks@securenetcoms.co.uk',
    packages=['random_phone'],
    url='https://github.com/rfranks-securenet/RandomPhone',
    license='LICENSE',
    description='A module to generate random phone numbers',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    include_package_data=True,
    install_requires=[],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    test_suite='random_phone.test.test_random_phone',
    extras_require={
        'testing': ['pytest'],
    },
)