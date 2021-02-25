""" Unit tests for db health check """
from utils_package.data_controller.scripts.health_check import HealthCheck
from unittest import TestCase


class TestHealthCheck(TestCase):
    """ Unit tests for db health check """

    def setUp(self):
        """ Set up class variables """
        self.db_health_check = HealthCheck()

    def test_health_check(self):
        """ Validate the health check endpoints
        1. Hit get queries for both reader and writer
        2. Validate responses for each
        """
        # 1. Hit get queries for both reader and writer
        reader_response = self.db_health_check.validate_reader_up()
        writer_response = self.db_health_check.validate_writer_up()
        responses = [reader_response, writer_response]

        # 2. Validate responses for each
        for response in responses:
            self.assertEqual(response[0], 1)
            self.assertEqual(response[1][0][0], 'UP')
