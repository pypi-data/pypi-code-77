
from setuptools import setup, find_packages
long_description = 'optional longer description of your project '

setup(

    name='aps_hello_pypi_beta', #
    version='1.0.3',  #
    description='A sample Python project',  # Optional
    long_description=long_description,  
    long_description_content_type='text/markdown',  
    url='https://github.com/aps010191/',  # Optional
    author='Akhand pratap singh',  # Optional'
    author_email='akhand2802@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='sample, learning',  # Optional
    packages=find_packages(),  
    python_requires='>=3.7, <4',
    install_requires=['tabulate', 'colorama'],  # Optional
    entry_points={  # Optional
        'console_scripts': [
            'sample=calculator:add',
        ],
    },
    project_urls={  # Optional
        'Source': 'https://github.com/aps010191/ONS/tree/master/sample-package'
    },
)

