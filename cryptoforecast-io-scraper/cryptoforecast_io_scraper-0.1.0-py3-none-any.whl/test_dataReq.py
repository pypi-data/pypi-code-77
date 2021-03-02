from unittest import TestCase

from cryptoforecast_io_scraper.request import DataReq


# Sync
class TestSyncDataReq(TestCase):

    def test__get_data(self):
        """Should use same values as in the documentation"""
        data_req = DataReq()
        get_data = data_req._get_data()
        self.assertIsNotNone(get_data)
        self.assertNotEqual(get_data, {})
        self.assertIn('items', get_data)
