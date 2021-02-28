
from setuptools import setup, find_packages



setup(
    name='weworkhelper',
    version='0.0.1',
    description='send messages through wework',
    long_description='send messages through wework',
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    author='skygongque',
    author_email='1243650225@qq.com',
    include_package_data=True,
    install_requires=['requests', 'json'],
    packages=find_packages()
)