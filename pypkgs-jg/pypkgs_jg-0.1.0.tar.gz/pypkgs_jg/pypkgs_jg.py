import pandas as pd


def catbind(*args):
    """
    Concatenates multiple pandas categoricals.

    Parameters
    ----------
    *args : pandas.core.arrays.categorical.Categorical
        Any number of pandas categoricals.

    Returns
    -------
    pandas.core.arrays.categorical.Categorical
        The new concatenated pandas categorical.

    Examples
    --------
    >>> from pypkgs import pypkgs
    >>> a = pd.Categorical(["character", "hits", "your", "eyeballs"])
    >>> b = pd.Categorical(["but", "integer", "where it", "counts"])
    >>> c = pd.Categorical(["macgrubie", "dont", "play", "like", "homie"])
    >>> pypkgs.catbind(a, b, c)
    ['character', 'hits', 'your', 'eyeballs', 'but', ..., 'macgrubie', 'dont', 'play', 'like', 'homie']
    Length: 13
    Categories (13, object): ['but', 'character', 'counts', 'dont', ..., 'macgrubie', 'play', 'where it', 'your']
    """
    concatenated = pd.concat([pd.Series(arg.astype('str')) for arg in args])
    return pd.Categorical(concatenated)