import setuptools

long_description = '''
Yandex Speller API. How to use:
```
>>> from yaspeller import check
>>> res = check('привет', lang='ru')
>>> res.is_ok
True
>>> res.first_match()
None
```
'''

setuptools.setup(
    name="YandexSpeller",
    version="1.0.0",
    author='Vadim Simakin',
    author_email="sima.vad@yandex.ru",
    description="Yandex Speller API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['yaspeller'],
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)