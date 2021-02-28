from setuptools import setup, find_packages

# from papyrus import __version__


def read_file(fname):
    try:
        with open(fname) as f:
            return f.read()
    except IOError:
            return ''


setup(
    name='sphinx-papyrus-theme',
    # version=__version__,
    version='0.0.1.dev0',
    license='BSD 3-Clause',
    description='A modern and responsive sphinx theme for live documentations.',
    long_description=read_file('README.rst'),
    long_description_content_type='text/x-rst',
    author='Nizar DELLELI',
    author_email='nizar.delleli@gmail.com',
    # maintainer='',
    # maintainer_email='',
    keywords='sphinx theme papyrus bootstrap materialdesign',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Theme',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Documentation',
    ],
    url='https://github.com/cizario/sphinx-papyrus-theme/',
    download_url='https://github.com/cizario/sphinx-papyrus-theme/',
    project_urls={
        'Tracker': 'https://github.com/cizario/sphinx-papyrus-theme/issues',
        'Source': 'https://github.com/cizario/sphinx-papyrus-theme/',
        # 'Funding': 'https://patreon.com/cizario',
        # 'Say Thanks!': 'http://saythanks.io/to/cizario',
        'Release notes': 'https://github.com/cizario/sphinx-papyrus-theme/releases',
        'Documentation': 'https://sphinx-papyrus-theme.readthedocs.io/en/latest/',
    },
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        'Sphinx',
    ],
    entry_points={
        # Distribute the theme as a python package
        # https://www.sphinx-doc.org/en/master/development/theming.html#distribute-your-theme-as-a-python-package
        'sphinx.html_themes': [
            'bootstrap = papyrus',
            # 'materialdesign = papyrus',
        ],
    },
    platforms='any',
)
