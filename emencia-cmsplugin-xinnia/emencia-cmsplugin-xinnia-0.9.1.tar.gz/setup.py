"""Setup script for cmsplugin_zinnia"""
from setuptools import setup
from setuptools import find_packages

import cmsplugin_zinnia

setup(
    name='emencia-cmsplugin-xinnia',
    version=cmsplugin_zinnia.__version__,

    description='Django-CMS plugins for django-blog-xinnia',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',

    keywords='django, blog, weblog, zinnia, cms, plugins, apphook',

    author=cmsplugin_zinnia.__author__,
    author_email=cmsplugin_zinnia.__email__,
    url=cmsplugin_zinnia.__url__,

    packages=find_packages(exclude=['demo_cmsplugin_zinnia']),
    classifiers=[
        'Framework :: Django',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules'],

    license=cmsplugin_zinnia.__license__,
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=2.2',
        'django-cms>=3.7',
    ]
)
