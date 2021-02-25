""" Quick queries to ensure that the database is up """
from utils_package.data_controller.pg_util import PGUtil


class HealthCheck(object):
    """ Quick queries to ensure that the database is up """

    def __init__(self):
        """ Set up class variables """
        self.writer_check = PGUtil(user='app_writer')
        self.reader_check = PGUtil(user='app_reader')

    def validate_writer_up(self):
        """
        Simple check to confirm the database connection is working
        :return: Row count and SQL response
        """
        sql = """
        SELECT ('UP')
        """
        response = self.writer_check.execute_query(sql)
        return response

    def validate_reader_up(self):
        """
        Simple check to confirm the database connection is working
        :return: Row count and SQL response
        """
        sql = """
        SELECT ('UP')
        """
        response = self.reader_check.execute_query(sql)
        return response
