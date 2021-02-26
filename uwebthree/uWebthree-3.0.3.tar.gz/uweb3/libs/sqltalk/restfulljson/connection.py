#!/usr/bin/python3
"""This module implements the Connection class, which sets up a connection to
a Restfull Json API. From this connection, cursor objects can be created, which
use the escaping and character encoding facilities offered by the connection.
"""
__author__ = 'Jan Klopper <jan@underdark.nl>'
__version__ = '0.1'

# Standard modules
import requests
import logging
import os
import queue
import threading

# Application specific modules
from . import converters
from . import cursor

class Connection(object):
  def __init__(self, *args, **kwds):
    self.logger = logging.getLogger('jsonapi_%s' % kwds.get('url'))
    if kwds.pop('debug', False):
      self.logger.setLevel(logging.DEBUG)
    else:
      self.logger.setLevel(logging.WARNING)
    if kwds.pop('disable_log', False):
      self.logger.disable_logger = True
    self.url = kwds.get('url', '')
    self.version = kwds.get('version', None)

  def __enter__(self):
    """Starts a transaction."""
    return cursor.Cursor(self)

  def __exit__(self, exc_type, _exc_value, _exc_traceback):
    """End of transaction: commits , or rolls back on failure."""
    pass

  def commit(self):
    pass

  def rollback(self):
    pass

  @staticmethod
  def EscapeField(field):
    """We cannot escape, the server should do so.."""
    return field

  def EscapeValues(self, obj):
    """We cannot escape, the server should do so."""
    return obj


class JsonAPIResult:
  def __init__(self, result, description, rowcount, lastrowid):
    self.result = result
    self.description = description
    self.rowcount = rowcount
    self.lastrowid = lastrowid

  def fetchall(self):
    return self.result
