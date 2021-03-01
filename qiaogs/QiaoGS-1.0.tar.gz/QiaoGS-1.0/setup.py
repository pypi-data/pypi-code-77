#!/bin/usr/env python
from distutils.core import setup, Extension

module1 = Extension("QiaoGS", sources=["QiaoGS.c"])

setup( 
    name="QiaoGS", 
    version="1.0", 
    description="个人信息",
    ext_modules=[module1],
    author='QiaoGS',
    author_email='qiaoguosong@sina.com',
    url="https://github.com/puwow",
    keywords=['QiaoGS'],
    )
