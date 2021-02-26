import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='word2lex',
    author="L. Rheault",
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Sentiment dictionary induction for political texts using word embeddings",
    license="MIT license",
    long_description=long_description,
    include_package_data=True,
    keywords='word2lex',
    packages=setuptools.find_packages(),
    url='https://github.com/lrheault/word2lex',
    version='0.0.1',
    zip_safe=False,
)
