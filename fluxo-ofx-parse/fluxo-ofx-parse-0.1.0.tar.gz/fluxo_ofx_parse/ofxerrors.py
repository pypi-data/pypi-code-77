class OfxParserException(Exception):
    pass


class EmptyOFXException(OfxParserException):
    pass


class EmptyTransactionNameException(OfxParserException):
    pass


class InvalidTransactionDateException(OfxParserException):
    pass


class NoTransactionAmountException(OfxParserException):
    pass
