from setuptools import setup, find_packages

setup(
    name='elly',
    version='1.0.1',
    description='elly.love',
    author='lihao',
    author_email='it_fk@163.com',
    url='http://elly.love',
    packages=['elly'],
    # py_modules=['elly.util', 'elly.count_down_latch', 'elly.exception_ignore']

    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3.9',
    ],
)
