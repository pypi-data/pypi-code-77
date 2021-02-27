#!/usr/bin/env python

"""Tests for `work_report_tool` package."""


import unittest
from click.testing import CliRunner

from work_report_tool import work_report_tool
from work_report_tool import cli


class TestWork_report_tool(unittest.TestCase):
    """Tests for `work_report_tool` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'work_report_tool.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
