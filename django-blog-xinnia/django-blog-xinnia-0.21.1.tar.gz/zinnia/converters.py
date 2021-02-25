"""URL converters for the Zinnia project"""
class FourDigitYearConverter:
    """
    Pattern converter for a Year on four digits exactly
    """
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        # Enforce integer since some code may try to pass a number as a string
        return '%04d' % int(value)


class TwoDigitMonthConverter:
    """
    Pattern converter for a Month on four digits exactly
    """
    regex = '[0-9]{2}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        # Enforce integer since some code may try to pass a number as a string
        return '%02d' % int(value)


class TwoDigitDayConverter(TwoDigitMonthConverter):
    """
    Pattern converter for a Day on four digits exactly.

    Just an explicit Class which inherit from 'TwoDigitMonthConverter'.
    """
    pass


class UsernamePathConverter:
    """
    Pattern converter for Author username string
    """
    regex = '[a-zA-Z0-9_.+-@]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class PathPathConverter:
    """
    Pattern converter for path string (such as ``foo/bar``)
    """
    regex = '[-\/\w]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class TagPathConverter:
    """
    Pattern converter for tag string
    """
    regex = '[^/]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class TokenPathConverter:
    """
    Pattern converter for token string
    """
    regex = '[\dA-Z]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
