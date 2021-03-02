import logging
import traceback


class NoData(Exception):
    """
    No data on the TCP connection, or less than expected
    """

    def __init__(self, expected_bytes: int, got_bytes: int, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.expected_bytes = expected_bytes
        self.got_bytes = got_bytes


def log_exception(e: Exception):
    try:
        traceback.print_exc(e)
    except:
        pass

    try:
        logging.error(e)
    except:
        pass
