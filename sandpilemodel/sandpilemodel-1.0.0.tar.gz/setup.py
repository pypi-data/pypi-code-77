
from setuptools import setup

# reading long description from file
with open('DESCRIPTION.txt') as file:
    long_description = file.read()


# specify requirements of your package here
REQUIREMENTS = ['pylab', 'matplotlib', 'numpy']

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Physics',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    ]

keywords = ['sandpile', 'cellular automaton']

# calling the setup function
setup(name='sandpilemodel',
      version='1.0.0',
      description='A small package for simulating sandpile model',
      long_description=long_description,
      url='https://github.com/bhavishrg/sandpile',
      author='Bhavish Raj Gopal',
      author_email='gbhavish@gmail.com',
      license='MIT',
      packages=['sandpilemodel'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS
      )
