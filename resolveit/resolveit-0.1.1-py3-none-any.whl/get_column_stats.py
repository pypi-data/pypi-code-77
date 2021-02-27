from resolveit import column_stats as cs
from resolveit.utils import asinh_scale


def get_column_stats(col):
    n_most_common_values = 3
    n_most_common_words = 4
    n_most_common_shingles = 5
    shingle_length = 3

    most_common_values = cs.most_common_values(col, n_most_common_values)
    most_common_words = cs.most_common_words(col, n_most_common_words)
    most_common_shingles = cs.most_common_shingles(col,
                                                   n_most_common_shingles,
                                                   shingle_length)

    stats = {'frac_empty': cs.frac_empty(col),
             'frac_null': cs.frac_null(col),
             'frac_numeric': cs.frac_numeric(col),
             'avg_length': cs.avg_length(col),
             'avg_n_words': cs.avg_n_words(col),
             'cardinality': cs.cardinality(col),
             'median_length': cs.median_length(col),
             'median_n_words': cs.median_n_words(col)}
    
    for i in range(n_most_common_values):
        if i < len(most_common_values):
            stats['most_common_values_%s' % (i+1)] = most_common_values[i][0]
        else:
            stats['most_common_values_%s' % (i + 1)] = None

    for i in range(n_most_common_words):
        if i < len(most_common_words):
            stats['most_common_words_%s' % (i+1)] = most_common_words[i][0]
        else:
            stats['most_common_words_%s' % (i + 1)] = None

    for i in range(n_most_common_shingles):
        if i < len(most_common_shingles):
            stats['most_common_shingles_%s' % (i+1)] = most_common_shingles[i][0]
        else:
            stats['most_common_shingles_%s' % (i + 1)] = None

    return stats


def distance_most_common(stats_1, stats_2, name):
    template = 'most_common_%s' % name
    stat_names = []
    for stat_name in stats_1.keys():
        if template in stat_name:
            stat_names.append(stat_name)
    stat_names = sorted(stat_names)

    values_1 = [stats_1[stat_name] for stat_name in stat_names]
    values_2 = [stats_2[stat_name] for stat_name in stat_names]

    dist_1 = sum([v1 != v2 for v1, v2 in zip(values_1, values_2)])/len(values_1)
    n_intersect = len(set(values_1).intersection(values_2))
    n_union = len(set(values_1).union(values_2))
    jaccard_sim = n_intersect/n_union
    dist_2 = 1 - jaccard_sim

    return dist_1 + dist_2


def column_stats_distances(stats_1, stats_2):

    distances = {'frac_empty': abs(stats_1['frac_empty'] - stats_2['frac_empty']),
                 'frac_null': abs(stats_1['frac_null'] - stats_2['frac_null']),
                 'frac_numeric': abs(stats_1['frac_numeric'] - stats_2['frac_numeric']),
                 'avg_length': abs(asinh_scale(stats_1['avg_length'] - stats_2['avg_length'])),
                 'avg_n_words': abs(asinh_scale(stats_1['avg_n_words'] - stats_2['avg_n_words'])),
                 'cardinality': abs(asinh_scale(stats_1['cardinality'] - stats_2['cardinality'])),
                 'median_length': abs(asinh_scale(stats_1['median_length'] - stats_2['median_length'])),
                 'median_n_words': abs(asinh_scale(stats_1['median_n_words'] - stats_2['median_n_words'])),
                 'most_common_values': distance_most_common(stats_1, stats_2, 'values'),
                 'most_common_words': distance_most_common(stats_1, stats_2, 'words'),
                 'most_common_shingles': distance_most_common(stats_1, stats_2, 'shingles')}

    return distances


def column_stats_total_distance(stats_1, stats_2):
    distances = column_stats_distances(stats_1, stats_2)
    dist = list(distances.values())
    assert min(dist) >= 0
    return sum(dist)
