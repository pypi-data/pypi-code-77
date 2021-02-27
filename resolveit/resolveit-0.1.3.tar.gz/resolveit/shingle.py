def get_shingles(string, length):
    n = len(string)
    if n <= length:
        return [string]

    shingles = []

    for start in range(n-length+1):
        shingle = string[start: start+length]
        shingles.append(shingle)

    return shingles


def get_flat_shingles(string_list, length):
    shingles = []
    for string in string_list:
        shingles += get_shingles(string, length)

    return shingles


def count_shingles(counter, string, length):
    n = len(string)
    if n <= length:
        counter[string] += 1
        return

    for start in range(n - length + 1):
        shingle = string[start: start + length]
        counter[shingle] += 1
