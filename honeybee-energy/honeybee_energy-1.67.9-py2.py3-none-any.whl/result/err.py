# coding=utf-8
"""Module for parsing EnergyPlus Error (.err) files."""
from __future__ import division

import os


class Err(object):
    """Object for parsing EnergyPlus Error (.err) files.

    Args:
        file_path: Full path to an Err file that was generated by EnergyPlus.

    Properties:
        * file_path
        * file_contents
        * warnings
        * severe_errors
        * fatal_errors
    """

    def __init__(self, file_path):
        """Initialize Err"""
        assert os.path.isfile(file_path), 'No file was found at {}'.format(file_path)
        assert file_path.endswith('.err'), \
            '{} is not an error file ending in .err.'.format(file_path)
        self._file_path = file_path
        self._file_contents = None
        self._warnings = None
        self._severe_errors = None
        self._fatal_errors = None

    @property
    def file_path(self):
        """Get the path to the .err file."""
        return self._file_path

    @property
    def file_contents(self):
        """Get a string of all contents in the file."""
        if not self._file_contents:
            self._parse_file_contents()
        return self._file_contents

    @property
    def warnings(self):
        """Get a list of strings for all of the warnings found in the .err file.

        Warnings are usually not important enough to bring to the front-end users'
        attention but they can be helpful for developers and advanced users.
        """
        if not self._warnings:
            self._sort_warnings_errors()
        return self._warnings

    @property
    def severe_errors(self):
        """Get a list of strings for all of the severe errors found in the .err file.

        Severe errors are important enough that front-end users should be made aware of
        them even though they do not necessarily mean that the simulation has failed.
        """
        if not self._severe_errors:
            self._sort_warnings_errors()
        return self._severe_errors

    @property
    def fatal_errors(self):
        """Get a list of strings for all of the fatal errors found in the .err file.

        Fatal errors indicate the reason why the simulation has failed.
        """
        if not self._fatal_errors:
            self._sort_warnings_errors()
        return self._fatal_errors

    def _parse_file_contents(self):
        """Parse all of the contents of a file path."""
        with open(self._file_path) as err_file:
            self._file_contents = err_file.read()

    def _sort_warnings_errors(self):
        """Sort the contents of the error file into warnings and errors."""
        self._warnings = []
        self._severe_errors = []
        self._fatal_errors = []
        for line in self.file_contents.split('\n'):
            if '** Warning **' in line:
                self._warnings.append(line.split('** Warning **')[-1])
            elif '**  Fatal  **' in line:
                self._fatal_errors.append(line)
            elif '** Severe  **' in line:
                self._severe_errors.append(line)

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __repr__(self):
        return 'Energy Error Result: {}'.format(self.file_path)
