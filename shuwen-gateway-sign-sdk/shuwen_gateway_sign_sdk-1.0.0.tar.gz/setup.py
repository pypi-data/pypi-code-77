#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys
import shuwen_gateway_sign_sdk.pkg_info

if sys.version_info <= (2, 5):
    sys.stderr.write("ERROR: mq python sdk requires Python Version 2.5 or above.\n")
    sys.stderr.write("Your Python version is %s.%s.%s.\n" % sys.version_info[:3])
    sys.exit(1)

setup(name=shuwen_gateway_sign_sdk.pkg_info.name,
      version=shuwen_gateway_sign_sdk.pkg_info.version,
      author="lawrence",
      author_email="",
      url=shuwen_gateway_sign_sdk.pkg_info.url,
      packages=["shuwen_gateway_sign_sdk"],
      license=shuwen_gateway_sign_sdk.pkg_info.license,
      description=shuwen_gateway_sign_sdk.pkg_info.short_description,
      long_description=shuwen_gateway_sign_sdk.pkg_info.long_description)
