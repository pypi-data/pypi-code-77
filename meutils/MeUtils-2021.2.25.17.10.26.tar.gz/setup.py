#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.iapp
# @File         : setup
# @Time         : 2019-06-17 16:12
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : https://note.qidong.name/2018/01/python-setup-requires/


import time
import pandas as pd
from pathlib import Path
from setuptools import find_packages, setup

# rename
package_name = Path(__file__).absolute().parent.name
version = time.strftime("%Y.%m.%d.%H.%M.%S", time.localtime())

get_requirements = lambda p='requirements.txt': pd.read_csv(p, comment='#', names=['name']).name.tolist()

with open("README.md", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=package_name,
    version=version,
    url=f'https://github.com/Jie-Yuan/{package_name}',
    keywords=['utils'],
    description=('description'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='yuanjie',
    maintainer='yuanjie',
    author_email='313303303@qq.com',
    maintainer_email='313303303@qq.com',
    license='MIT License',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.*']},
    platforms=["all"],
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
    ],

    python_requires='>=3.6',
    setup_requires=["pandas"],
    install_requires=get_requirements(),
    extras_require={
        'plus': get_requirements('requirements_plus.txt'),  # pip install -U meutils\[plus\]
    },

    entry_points={
        'console_scripts': [
            'mecli=meutils.clis:cli',
            'mecli-cron=meutils.clis.cron:main',

            'mi-ann=meutils.clis.ann:main',
            'mi-dsl=meutils.clis.dsl:main',

            # 'mecli=meutils.cli:cli',
            'mecli-conf=meutils.clis.conf:conf_cli',
            'mecli-pipe=meutils.pipe:cli',
        ]

    },

)

if __name__ == '__main__':
    print(__file__)
