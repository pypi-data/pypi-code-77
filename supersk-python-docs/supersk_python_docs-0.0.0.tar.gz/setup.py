#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    entry_points = {
        'sphinx.html_themes': [
            'supersk-python-docs = supersk_python_docs',
        ]
    }
)
