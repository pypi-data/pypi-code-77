from distutils.core import setup
setup(
  name = 'jamestestpackage',
  packages = ['jamestestpackage'],   
  version = '0.4',
  license='MIT',
  description = 'test for making packages',
  author = 'James Doucette',
  author_email = 'jmdoucette41@gmail.com',
  url = 'https://github.com/jmdoucette/james_test_package',
  download_url = 'https://github.com/jmdoucette/james_test_package/archive/v0.4.tar.gz',
  keywords = ['TEST'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)