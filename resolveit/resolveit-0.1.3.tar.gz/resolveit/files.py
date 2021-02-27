from glob import glob
from csv import DictReader
from resolveit.utils import take


def get_files():
    all_files = glob('data/*.csv')
    return [file for file in all_files]


def force_upper(row):
    return {k: v.upper() for k, v in row.items() if k is not None}


def stream_file(filename):
    print('reading: %s' % filename)
    for row in DictReader(open(filename, 'r', encoding='utf-8-sig')):
        try:
            row = force_upper(row)
            yield row
        except AttributeError:
            pass


def head_all():
    line = '-'*50
    files = get_files()
    for file in files:
        stream = stream_file(file)
        head = next(stream)
        cols = list(head.keys())
        print('file: %s' % file)
        # print('columns: %s' % cols)
        print(head)

        if cols[0] == '\ufeff':
            print(head)
        print(line)
        junk = input('ok')
        if junk == 'q':
            return


def get_col_from_key(key, n_rows_max):
    file, index, col_name = key
    data = take(stream_file(file), n_rows_max)
    return [d[col_name] for d in data]
