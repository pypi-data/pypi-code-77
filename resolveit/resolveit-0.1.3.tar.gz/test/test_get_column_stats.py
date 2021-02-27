from resolveit.get_all_stats import get_all_stats, get_stats_dist_matrix
from resolveit.show_matrix import show_matrix


def print_stats(stats):
    line = '-'*40
    for k, v in stats.items():
        print("%s: %s" % (k, v))

    print(line)


def test_get_column_stats():
    _ = get_all_stats(n_files_max=500, n_rows_max=500, check_distances=True)


def test_stats_dist_matrix():
    n_files_max = 3
    n_rows_max = 100
    keys, matrix, stats = get_stats_dist_matrix(n_files_max=n_files_max, n_rows_max=n_rows_max)
    print(keys)
    print(matrix.shape)
    n = len(keys)
    print(n)
    assert matrix.shape == (n, n)
    # matrix_max = 5.0
    # matrix[matrix > matrix_max] = matrix_max
    # show_matrix(matrix)


def test_stats_dist_matrix_all():
    n_files_max = 20000
    n_rows_max = 4000
    keys, matrix, stats = get_stats_dist_matrix(n_files_max=n_files_max, n_rows_max=n_rows_max)
    print('shape', matrix.shape)
    n = len(keys)
    print(n)
    assert matrix.shape == (n, n)
    # matrix_max = 5.0
    # matrix[matrix > matrix_max] = matrix_max
    show_matrix(matrix)
