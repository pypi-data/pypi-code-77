from math import asinh


def is_numeric(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def is_empty(x):
    return x.strip() == ''


def strip_special(x):
    specials = ['.', ',', '[', ']', '(', ')', '-', '_',
                '*', '#', '!', '?', '~', '$', '%', '^',
                '&', '+', '=', '{', '}', '|', '/',
                '<', '>']

    for special in specials:
        x = x.replace(special, '')

    return x


def is_null(x):
    if is_empty(x):
        return True

    nulls = ['NULL', 'NA', 'NONE', 'N.A.', 'MISSING', 'NAN']
    if x in nulls:
        return True

    if strip_special(x) in nulls:
        return True

    return False


def n_words(x):
    return max(len(x.split()), 1)


def take_stream(stream, num):
    for i, item in enumerate(stream):
        if i == num:
            return
        yield item


def take(stream, num):
    return list(take_stream(stream, num))


def asinh_scale(x, scale=8.509181282393216):
    return asinh(x/scale)

