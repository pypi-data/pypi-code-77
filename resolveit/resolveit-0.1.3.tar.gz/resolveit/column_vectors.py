from collections import Counter
from resolveit.shingle import count_shingles


def count_values_col(col):
    counter = Counter()
    for i in col:
        counter[i] += 1

    return counter


def count_words_col(col):
    counter = Counter()
    for item in col:
        for word in item.split():
            counter[word] += 1

    return counter


def count_shingles_col(col, length):
    counter = Counter()
    for string in col:
        count_shingles(counter, string, length)

    return counter
