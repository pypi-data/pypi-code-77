#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path

def setup(app):
    app.add_html_theme('supersk-python-docs', path.abspath(path.dirname(__file__)))
