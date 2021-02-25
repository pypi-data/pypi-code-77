from setuptools import setup

# reading long description from file
with open('README.md', encoding='utf-8') as file:
    long_description = file.read()


# specify requirements of your package here
REQUIREMENTS = ['requests', 'tabulate']

# some more details
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    ]

# calling the setup function
setup(name='eduAlgo',
      version='1.2.1.4',
      description='An educational software to make Algorithm learning & implementation easier in python',
      long_description=long_description,
      long_description_content_type = 'text/markdown',
      url='https://github.com/edualgo/eduAlgo',
      author='Abhijit Tripathy',
      author_email='founder@edualgoacademy.com',
      license='MIT',
      packages=['edualgo'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='algorithms'
      )
