#!/usr/bin/python3
"""SQLTalk Json API interface package."""

# Standard modules
import requests

# Application specific modules
from . import connection


def Connect(*args, **kwds):
  """Factory function for connection.Connection."""
  return connection.Connection(*args, **kwds)


DataError = requests.ConnectionError
DatabaseError = requests.HTTPError
Error = requests.RequestException
IntegrityError = requests.RequestException#sqlite3.IntegrityError
InterfaceError = requests.RequestException#sqlite3.InterfaceError
InternalError = requests.RequestException#sqlite3.InternalError
NotSupportedError = requests.RequestException#sqlite3.NotSupportedError
OperationalError = requests.RequestException#sqlite3.OperationalError
