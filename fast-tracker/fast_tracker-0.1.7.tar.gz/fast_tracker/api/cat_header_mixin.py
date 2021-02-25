
class CatHeaderMixin(object):

    settings = None

    def __enter__(self):
        result = super(CatHeaderMixin, self).__enter__()
        if result is self and self.transaction:
            self.settings = self.transaction.settings or None
        return result

    def process_response_headers(self, response_headers):
        """
        不支持跨应用跟踪
        :param response_headers:
        :return:
        """
        pass

    def process_response_metadata(self, cat_linking_value):
        pass

    @classmethod
    def generate_request_headers(cls, transaction):

        if transaction is None:
            return []

        settings = transaction.settings

        fast_headers = []

        if settings.distributed_tracing.enabled:
            transaction.insert_distributed_trace_headers(fast_headers)
        return fast_headers

