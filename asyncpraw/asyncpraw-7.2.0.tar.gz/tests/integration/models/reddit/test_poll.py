"""Test asyncpraw.models.poll."""


import pytest

from asyncpraw.models import PollData, PollOption

from ... import IntegrationTest


class TestPollData(IntegrationTest):
    async def test_get_attrs(self):
        poll_id = "fo7p5b"
        with self.use_cassette():
            submission = await self.reddit.submission(poll_id)
            poll_data = submission.poll_data
            assert isinstance(poll_data, PollData)
            assert isinstance(poll_data.options, list)
            assert all(isinstance(option, PollOption) for option in poll_data.options)
            assert poll_data.user_selection is None  # not logged in

            with pytest.raises(KeyError):
                poll_data.option("badID")

    async def test_get_user_selection(self):
        poll_id = "hlzjkc"
        self.reddit.read_only = False
        with self.use_cassette():
            submission = await self.reddit.submission(poll_id)
            poll_data = submission.poll_data
            # For this test to pass, the authenticated user should have
            # voted in the poll specified.
            assert isinstance(poll_data.user_selection, PollOption)
