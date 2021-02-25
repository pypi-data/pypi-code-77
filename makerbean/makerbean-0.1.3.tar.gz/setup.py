# -*- coding: utf-8 -*-
# @Author: Anderson
# @Date:   2019-11-14 17:45:03
# @Last Modified by:   ander
# @Last Modified time: 2021-02-25 15:37:46
import setuptools


setuptools.setup(
    name="makerbean",
    version="0.1.3",
    author="MakerBi",
    author_email="andersonby@163.com",
    description="A small educational purpose package",
    long_description_content_type="text/markdown",
    url="https://makerbean.com",
    packages=setuptools.find_packages(),
    install_requires=['openpyxl', 'requests', 'beautifulsoup4', 'lxml', 'jieba', 'pyecharts', 'pdfplumber', 'PyPDF2', 'python-docx', 'pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
