#!/usr/bin/env python

"""Tests for `pandag` package."""

import pytest
import pandas as pd
import numpy as np

from click.testing import CliRunner

from pandag import pandag
from pandag.nodes import Assert, Output, Dummy
from pandag import cli


@pytest.fixture
def simple():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    size = 1000
    df = pd.DataFrame({
        'buyside': np.random.choice(['gemini', 'outbrain', 'taboola'], size),
        'bid': np.random.uniform(low=0.0, high=2, size=size),
        'campaign_bid': np.random.uniform(low=0.0, high=5, size=size),
        'ctr_7': np.random.uniform(low=0.0, high=10, size=size),
        'rpc_weighted_3': np.random.uniform(low=0.0, high=10, size=size),
        'npm_target': np.random.uniform(low=0.0, high=3, size=size),
    })
    return df


def test_simple(simple):
    """Sample pytest test function with the pytest fixture as an argument."""
    algo = {
        Assert(f'om_sessions >= {min_pub_sessions}', _label=f'sessions >= min_pub_sessions ({min_pub_sessions})'): {
            True: [
                Output(bid_target=calc_rolling_mean_bid, _label='bid = ctr_7 * rpc_weighted_3 * (1 - npm_target)'),
                (BID_TARGET := Output(_label='BID_TARGET',
                                      bid_rec=lambda df: df['bid_target']))
                   ],
            False: [
                Output(_label='bid_old', bid_target=lambda df: df['bid_old']),
                BID_TARGET
                ]},
        BID_TARGET: BLOCKED
    }

    dag = pandag.Pandag(algo)


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'pandag.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
