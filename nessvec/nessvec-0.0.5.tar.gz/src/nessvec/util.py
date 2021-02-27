""" Utilities for loading word2vec and GloVe word embeddings for vector reasoning """
import os
import re
import requests
from zipfile import ZipFile
from pathlib import Path

import pandas as pd
import numpy as np
import scann  # noqa
from tqdm import tqdm


DATA_DIR = os.path.expanduser(os.path.join('~', 'nessvec-data'))

if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)

# size: 6B | 42B | 84B | twitter.27B
GLOVE_ZIP_FILENAME_TEMPLATE = 'glove.{size}B.zip'
GLOVE_URL_TEMPLATE = 'http://nlp.stanford.edu/data/' + GLOVE_ZIP_FILENAME_TEMPLATE

# dim: 50 | 100 | 300 | 1000
GLOVE_FILENAME_TEMPLATE = 'glove.{size}B.{dim}d.txt'


def unzip(zip_filepath, dest_filename=None, dim=50):
    """ Extract txt files from ZipFile and place them all in the dest_filepath or DATA_DIR """
    zip_filepath = Path(zip_filepath)
    sizematch = re.search(r'[.](\d{1,3})B[.]', str(zip_filepath))
    size = 6
    if sizematch:
        size = int(sizematch.groups()[0])
    dest_filename = Path(dest_filename or GLOVE_FILENAME_TEMPLATE.format(dim=dim, size=size))
    zip_filepath = Path(Path(zip_filepath).expanduser().absolute())
    with ZipFile(str(zip_filepath), 'r') as zipobj:
        zipobj.extract(str(dest_filename), path=DATA_DIR)
    dest_filepath = zip_filepath.parent.joinpath(dest_filename)
    return dest_filepath


def download_glove(size=6, url=None, dest_filepath=None):
    """ download and extract text file containig pairs of translated phrases

    Inputs:
        corpus (str): 6B | 42B | 84B | twitter.27B
        url (full url to the zip file containing a GloVe vector model)
    Returns:
        path_to_zipfile (str)
    """
    size = str(size).lower().strip()
    size = size.rstrip('b')
    if size.endswith('27'):
        size = 'twitter.27'
    url = url or GLOVE_URL_TEMPLATE.format(size=size)

    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)

    if not dest_filepath:
        dest_filepath = os.path.split(url)[-1]  # this separates url by '/' and takes the last part
        dest_filepath = os.path.join(DATA_DIR, dest_filepath)

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko)"
    headers = {'User-Agent': user_agent}

    # using requests to download and open file
    with requests.get(url, stream=True, headers=headers) as resp:
        with open(dest_filepath, 'wb') as fout:
            for chunk in tqdm(resp.iter_content(chunk_size=8192)):
                fout.write(chunk)
    return dest_filepath


def load_glove(dim=50, size=6, filepath=None):
    """ Download and return the specified GloVe word vectors dict from Stanford

    >>> wv = load_glove(dim=100, size=6, filepath='.')
    >>> len(wv)
    400000
    """
    dim = str(dim).lower().rstrip('d')
    filepath = Path(filepath or Path(DATA_DIR).joinpath(GLOVE_FILENAME_TEMPLATE.format(
        dim=dim, size=size)))
    zippath = Path(filepath).parent.joinpath(GLOVE_ZIP_FILENAME_TEMPLATE.format(size=size))
    # if filepath.lower()[-4:] == '.zip':
    #     filepath = unzip(filepath)

    if not filepath.is_file():
        if not zippath.is_file():
            zippath = download_glove(size=size)
        unzip(zippath)

    f = open(filepath, 'r')
    wv = {}
    for i, line in tqdm(enumerate(f)):
        splitLines = line.split()
        word = splitLines[0]
        embedding = np.array([float(value) for value in splitLines[1:]])
        wv[word] = embedding
    return wv


def check_load_glove():
    # filepath=os.path.join(BIGDATA_PATH, 'GoogleNews-vectors-negative300.bin.gz')
    wv = load_glove(50, )
    assert len(wv) == 400000
    return wv


def cosine_similarity(a, b):
    """ 1 - cos(angle_between(a, b))

    >>> cosine_similarity([0, 1, 1], [0, 1, 0])  # 45 deg
    .707...
    """
    a = np.array(a).flatten()
    b = np.array(b).flatten()
    a /= np.linalg.norm(a)
    b /= np.linalg.norm(b)
    return (a * b).sum()


class IndexedVectors:
    def __init__(self, vectors=None, index=None):
        if vectors is None:
            self.load()
        elif isinstance(vectors, dict):
            self.df = pd.DataFrame(vectors)
        else:
            self.df = pd.DataFrame(vectors, index=(index or range(len(vectors))))

    def load(self, dim=50, size=6):
        self.df = pd.DataFrame(load_glove(dim=dim, size=size))
        return self

    def get(self, key, default=None):
        if key in self.df.columns:
            return self.df[key]
        return default

    def __getitem__(self, key):
        try:
            return self.df[key]
        except KeyError:
            print(f"Unable to find '{key}' in {self.df.shape} DataFrame of vectors")
        lowered_key = key.lower()
        try:
            return self.df[lowered_key]
        except KeyError:
            print(f"Unable to find '{lowered_key}' in {self.df.shape} DataFrame of vectors")
        normalized_key = lowered_key.strip().replace('_', ' ')
        try:
            return self.df[normalized_key]
        except KeyError:
            pass
        raise(KeyError(f"Unable to find any of {set([key, lowered_key, normalized_key])} in self.df.shape DataFrame of vectors"))

    def keys(self):
        return self.df.columns.values

    def values(self):
        return self.df.T.values

    def iteritems(self):
        return self.df.T.iterrows()

    def iterrows(self):
        return self.df.T.iterrows()
