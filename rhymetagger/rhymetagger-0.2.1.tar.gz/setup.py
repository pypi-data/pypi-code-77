from distutils.core import setup

setup(
  name = 'rhymetagger',       
  include_package_data = True,  
  packages = ['rhymetagger'],   
  version = '0.2.1',      
  license='MIT',        
  description = 'A simple collocation-driven recognition of rhymes',   
  author = 'Petr Plechac',                   
  author_email = 'plechac@ucl.cas.cz',      
  url = 'https://github.com/versotym/rhymetagger',
  download_url = 'https://github.com/versotym/rhymeTagger/archive/v0.2.tar.gz',
  keywords = ['poetry', 'rhyme', 'versification'],
  package_data={'rhymetagger': ['models/*.json']},
  data_files=[('models', ['models/*.json'])],
  install_requires=[           
          'ujson',
          'string',
          'nltk',
          'subprocess',
          'collections',
          'ast',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',      
    'Topic :: Text Processing :: Linguistic',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.1',      
    'Programming Language :: Python :: 3.2',      
    'Programming Language :: Python :: 3.3',      
    'Programming Language :: Python :: 3.4',      
    'Programming Language :: Python :: 3.5',      
    'Programming Language :: Python :: 3.6',      
    'Programming Language :: Python :: 3.7',      
    'Programming Language :: Python :: 3.8',      
    'Programming Language :: Python :: 3.9',      
    'Programming Language :: Python :: 3.10',      
  ],
)
