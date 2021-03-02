from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='pymspyt',
    version='0.1.1',
    description='Module CLI to install YouTube Video/Audio',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    entry_points={'console_scripts': ['mspyt = pymspyt:main']},
    license='MIT',
    author='Siva Pranav Mandadi',
    author_email='msivapranav@gmail.com',
    packages=find_packages(),
    install_requires=['pytube']
)
