from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='chess-term',
      version='0.0.9',
      description='Play chess in your terminal',
      long_description=readme(),
      long_description_content_type='text/markdown',
      keywords='',
      url='http://gitlab.com/OldIronHorse/chess-term',
      author='Simon Redding',
      author_email='s1m0n.r3dd1ng@gmail.com',
      license='GPL3',
      packages=[
          'chessterm',
          'chessterm.ui',
          'chessterm.core',
          ],
      scripts=[
          'bin/chess-term',
          ],
      python_requires='>=3.7',
      install_requires=[
            'click',
            'chess',
          ],
      test_suite='nose.collector',
      tests_require=['nose', 'nosy'],
      include_package_data=True,
      zip_safe=False)
