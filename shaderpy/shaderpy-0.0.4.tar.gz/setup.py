from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='shaderpy',
    version='0.0.4',
    description='A simple shader package for Pyglet.',
    long_description=open('README.md').read() + '\n' + open('CHANGELOG.md').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Samuel Karabetian',
    license='MIT',
    classifiers=classifiers,
    keywords=['opengl', 'shader'],
    packages=find_packages(),
    install_requires=['pyglet', 'numpy']
)