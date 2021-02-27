from statistics import median
from resolveit.utils import is_numeric, is_empty, is_null, n_words
from resolveit.column_vectors import count_words_col
from resolveit.column_vectors import count_shingles_col


def frac_is(col, function):
    n = float(len(col))
    condition = [function(i) for i in col]
    return sum(condition) / n


def avg_func(col, function):
    n = float(len(col))
    sum_func = sum([function(i) for i in col])
    return sum_func/n


def median_func(col, function):
    return median([function(i) for i in col])


def frac_numeric(col):
    return frac_is(col, is_numeric)


def frac_empty(col):
    return frac_is(col, is_empty)


def frac_null(col):
    return frac_is(col, is_null)


def avg_length(col):
    return avg_func(col, len)


def avg_n_words(col):
    return avg_func(col, n_words)


def cardinality(col):
    return len(set(col))


def median_length(col):
    return median_func(col, len)


def median_n_words(col):
    return median_func(col, n_words)


def most_common_values(col, num):
    counter = count_words_col(col)
    return counter.most_common()[0:num]


def most_common_words(col, num):
    counter = count_words_col(col)
    return counter.most_common()[0:num]


def most_common_shingles(col, num, shingle_length):
    counter = count_shingles_col(col, shingle_length)
    return counter.most_common()[0:num]
