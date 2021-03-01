
class NoData(Exception):
    """
    No data on the TCP connection, or less than expected
    """

    def __init__(self, expected_bytes: int, got_bytes: int, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.expected_bytes = expected_bytes
        self.got_bytes = got_bytes
