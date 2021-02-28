# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:29:08 2021

@author: hp
"""
from setuptools import setup, find_packages

setup(
    name='prueba_ifsER',
    packages=find_packages(include=['prueba_ifsER', 'prueba_ifsER.*']),
    install_requires= ['tkinter','matplotlib','numpy','astropy','opencv-python','scikit-image','scipy','Pillow'],
    version='0.1.0',
    description='paquete de prueba prueba_ifsER',
    url='https://github.com/NildaX/python-prueba_ifsER',
    author='Nilda G.Xolo  Tlapanco',
    author_email='nilda_gaby_9745@live.com.mx',
    license='MIT',
    classifiers=['Programming Language :: Python :: 3.4'], 
    keywords=['testing', 'IFS', 'example'],
)