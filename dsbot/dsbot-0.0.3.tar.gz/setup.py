from setuptools import setup, find_packages

setup(
   name='dsbot',
   version='0.0.3',
   author='Jefry',
   author_email='jefry.sastre@gmail.com',
   packages=find_packages(),
   url='http://pypi.python.org/pypi/dsbot/',
   license='LICENSE.txt',
   description='Chatbot framework ...',
   install_requires=[
      'matplotlib==3.3.1',
      'nltk==3.5',
      'numpy==1.18.5',
      'TPOT==0.11.5',
      'pyod==0.8.2',
      'tqdm==4.48.2',
      'tensorflow==2.3.0',
      'scipy==1.4.1',
      'scikit-learn==0.23.2',
      'requests==2.24.0',
      'regex==2020.7.14',
      'pandas==1.1.1',
      'Keras==2.4.3',
      'sentence-transformers==0.3.8'
   ],
)