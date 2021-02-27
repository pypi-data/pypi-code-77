from time import time
from random import Random
import numpy as np
from resolveit.files import get_files
from resolveit.files import stream_file
from resolveit.utils import take
from resolveit.get_column_stats import get_column_stats
from resolveit.get_column_stats import column_stats_total_distance


def get_all_stats_from_stream(stream, n_rows_max=500, check_distances=False,
                              extra_key=None):

    data = take(stream, n_rows_max)
    col_names = list(data[0].keys())
    n_cols = len(col_names)
    all_stats = {}
    for col_index in range(n_cols):
        col_name = col_names[col_index]
        # print('file: %s, col_index: %s, col_name: %s' % (file, col_index, col_name))
        col_data = [row[col_name] for row in data]
        stats = get_column_stats(col_data)

        if check_distances:
            dist = column_stats_total_distance(stats, stats)
            assert dist == 0

        if extra_key is None:
            key = (col_index, col_name)
        else:
            key = (extra_key, col_index, col_name)

        all_stats[key] = stats

    return all_stats


def get_all_stats(n_files_max=500, n_rows_max=500, check_distances=False):
    files = get_files()
    rand = Random()
    rand.seed(3654726)
    rand.shuffle(files)
    files = files[0:n_files_max]

    all_stats = {}

    for file in files:
        stream = stream_file(file)
        all_stats_file = get_all_stats_from_stream(stream,
                                                   n_rows_max=500,
                                                   check_distances=False,
                                                   extra_key=file)

        all_stats.update(all_stats_file)

    return all_stats


def get_stats_dist_matrix(n_files_max=500, n_rows_max=1000):
    start = time()
    all_stats = get_all_stats(n_files_max=n_files_max, n_rows_max=n_rows_max, check_distances=False)
    items = list(all_stats.items())
    n_stats = len(items)
    matrix = np.zeros((n_stats, n_stats))
    keys = []
    for row_num, item_1 in enumerate(items):
        row_key, stats_1 = item_1
        keys.append(row_key)
        print('row_key: ', row_key)
        for col_num, item_2 in enumerate(items):
            col_key, stats_2 = item_2
            if row_num <= col_num:

                dist = column_stats_total_distance(stats_1, stats_2)
                if row_key == col_key:
                    assert dist == 0.0

                matrix[row_num, col_num] = dist
            else:
                matrix[row_num, col_num] = matrix[col_num, row_num]
                # matrix[row_num, col_num] = 0

    runtime = int(time() - start)

    print('runtime: %s sec' % runtime)

    return keys, matrix, all_stats
