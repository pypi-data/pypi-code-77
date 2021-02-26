def remove_duplicate_dicts(list_of_dicts):
    list_tuples = list(set([tuple([(k, v) for k, v in obs.items()]) for obs in list_of_dicts]))
    return [dict(obs) for obs in list_tuples]


def remove_dict_keys(dict, list_of_keys):
    for key in list_of_keys:
        dict.pop(key)
    return dict


def flatten_list(list):
    ### Flattens a list of lists ###
    return [item for sublist in list for item in sublist]


def dict_to_tuples(dict):
    return tuple(sorted(tuple((k, v) for k, v in dict.items())))


def clean(obj):
    return obj.replace('\n', '').replace(u'\xa0', u' ').replace('  ', '').replace('\r', '').replace('\t', '')


def to_pickle(obj, pickle_filename):
    import pickle
    with open(pickle_filename, 'wb') as f:
        pickle.dump(obj, f)


def from_pickle(pickle_filename):
    import pickle
    with open(pickle_filename, 'rb') as f:
        obj = pickle.load(f)
    return obj


def write_list_of_dicts2CSV(in_list, outfile):
    import csv
    varlist = [x for x in in_list[0].keys()]
    with open(outfile, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(sorted(varlist))
        for line in in_list:
            var_data = [v for k, v in sorted(line.items())]
            writer.writerow(var_data)


class namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def load_csv(file, delimiter=','):
    import csv
    with open(file, 'r') as infile:
        load_parms = [{k: empty_to_None(v) for k, v in dict(obs).items()} for obs in
                      csv.DictReader(infile, delimiter=delimiter)]
    return load_parms


def load_csv_utf8(file, delimiter=','):
    import csv
    with open(file, 'r', encoding='utf-8-sig') as infile:
        load_parms = [{k: empty_to_None(v) for k, v in dict(obs).items()} for obs in
                      csv.DictReader(infile, delimiter=delimiter)]
    return load_parms


def f2(x):
    return '{:,.2f}'.format(x)


def f4(x):
    return '{:,.4f}'.format(x)


def f0(x):
    return '{:,.0f}'.format(x)


def prt(obj):
    if type(obj) is list:
        for obs in obj:
            print(obs)
    elif type(obj) is dict:
        for key, val in sorted(obj.items()):
            print(key, '\t:\t', val)
    else:
        print(obj)


def print_df(df):
    from tabulate import tabulate
    print(tabulate(df, headers='keys', tablefmt='grid'))


def print_namespace(args):
    for d in vars(args):
        print(d, '\t', vars(args)[d])


class dict_to_namespace(object):
    def __init__(self, adict):
        self.__dict__.update(adict)


def print_time(txt='', st=0):
    from datetime import datetime
    seconds = datetime.utcnow().timestamp() - st
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print(txt, '{:1d}:{:02d}:{:05.2f}'.format(int(h), int(m), s))


def empty_to_None(x):
    if x == '':
        return None
    else:
        return x
