#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect

google_addr = '8.8.8.8'
google_country_name = 'United States'
google_name = 'dns.google'
password_addr = '54.39.133.155'
ping_addr = '24.24.23.2'

__all__ = [item for item in globals() if not item.startswith('_') and not inspect.ismodule(globals().get(item))]
