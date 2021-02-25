import re


class Converter:
    """Convert raw value to expected format.

    For example: when you get port value from `os.environ`,
    you may get a '80', then you have to convert it into int.
    """
    def convert(self, value):
        return value

    def __call__(self, value):
        return self.convert(value)


class CSV(Converter):
    """Convert  csv like string into list.

    For example: you have 'a.com,b.com,c.com' as raw value
    and you can get ['a.com', 'b.com', 'c.com'] via CSV.

    >>> CSV(delimiter_pattern='[,|]').convert('a.com,b.com|c.com')
    ['a.com', 'b.com', 'c.com']
    """
    def __init__(self, cast_func=str, delimiter_pattern=','):
        self.cast_func = cast_func
        self.delimiter_pattern = delimiter_pattern

    def convert(self, value):
        result = []
        for item in re.split(self.delimiter_pattern, value):
            item = item.strip()
            if item:
                result.append(item)
        return result
