from setuptools import setup , find_packages

classifiers = [
    #'Development Status :: 5 - Production/Stable',
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3 :: Only',
]

with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'oecx',
  packages = find_packages('src'),
  package_dir={'': 'src'},
  version = '0.2.0',
  description = 'Network builder for the Observatory for Economic Complexity ',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Francisco R. Lanza',
  author_email = 'frjrodriguezla@unal.edu.co',
  license='MIT',
  url = 'https://github.com/frjrodriguezla/oecx',
  keywords = ['oec', 'network'],
  classifiers = classifiers,
  install_requires=['requests','networkx'],
  python_requires='~=3.3',
  py_modules=['oecx'],
  #package_data={'': ['country_names.tsv']},
  include_package_data=True,
  data_files=[('oecx_contry_names', ['src/country_names.tsv'])]
)
