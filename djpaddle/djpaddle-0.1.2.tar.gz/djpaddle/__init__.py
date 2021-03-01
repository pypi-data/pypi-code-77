"""
Django + Paddle Made Easy.
"""
import pkg_resources

__version__ = pkg_resources.require("djpaddle")[0].version

default_app_config = "djpaddle.apps.DjpaddleConfig"
