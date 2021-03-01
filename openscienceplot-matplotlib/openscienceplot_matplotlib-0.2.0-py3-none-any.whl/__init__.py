'''
This module provides methods to save data from a matplotlib plot.

:dependencies:

    * numpy
    * matplotlib
    * h5py

:copyright:

    | Tom de Geus
    | tom@geus.me
    | http://www.geus.me
'''

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import h5py
import operator
import functools
from functools import singledispatch


def info():
    r'''
Return basic library information.
    '''

    return [
        'openscienceplot_matplotlib={0:s}'.format(__version__),
        'matplotlib={0:s}'.format(matplotlib.__version__)]


@singledispatch
def dump(handle):
    r'''
Return to be stored data from a handle.

Essential attributes are outputted as well, as follows:

*   matplotlib.lines.Line2D ('artist'): 'color', `linestyle', 'marker', 'label'.
*   matplotlib.container.ErrorbarContainer ('artist'): 'color', `linestyle', 'marker', 'label'.
    Warning: for now saved as matplotlib.lines.Line2D, without error-bars.

:argument:

    **handle**
        The object's handle.

:return:

    **data** (``<numpy.ndarray>``)
        The data.

    **attributes** (``<dict>``)
        Essential attributes.
    '''

    import warnings

    if len(handle) == 1:
        handle = handle[0]

    if isinstance(handle, matplotlib.lines.Line2D):
        return (
            handle.get_xydata(),
            {
                "artist" : 'matplotlib.lines.Line2D',
                "color" : handle.get_color(),
                "linestyle" : handle.get_linestyle(),
                "marker" : handle.get_marker(),
                "label" : handle.get_label(),
            })

    if isinstance(handle, matplotlib.container.ErrorbarContainer):
        warnings.warn('Error-bars not saved, help wanted.', Warning)
        return (
            handle.get_xydata(),
            {
                "artist" : 'matplotlib.lines.Line2D',
                "color" : handle[0].get_color(),
                "linestyle" : handle[0].get_linestyle(),
                "marker" : handle[0].get_marker(),
            })

    raise IOError('Unknown handle. Store manually, or consider filing a bug-report.')


@dump.register(h5py.File)
def _(f, key, handle):
    r'''
Save plot and attributes to HDF5-file.

:arguments:

    **f** (``<h5py.File>``)
        Opened HDF5 file.

    **key** (``<str>``)
        Name of the dataset to which to write.

    **handle**
        The handle to write.
    '''

    data, attributes = dump(handle)

    dset = f.create_dataset(key, data.shape, dtype=data.dtype)
    dset[:] = data

    for key in attributes:
        dset.attrs[key] = attributes[key]


@dump.register(dict)
def _(f, key, handle):
    r'''
Save plot and attributes to a dictionary.

:arguments:

    **f** (``<dict>``)
        Dictionary.

    **key** (``<str>`` | ``<list>``)
        Name of the dataset to which to write.
        Path separated by "/", or as list.

    **handle**
        The handle to write.

:returns:

    Dictionary.
    '''

    if type(key) == str:
        key = list(filter(None, key.split("/")))

    data, attributes = dump(handle)
    attributes["data"] = data

    functools.reduce(operator.getitem, key[:-1], f)[key[-1]] = attributes


def restore_h5py(data, key, axis=None):
    r'''
Restore plot from HDF5-file.

:arguments:

    **data** (``h5py.File``)
        Opened HDF5 file.

    **key** (``<str>``)
        Name of the dataset from which to read.

:options:

    **axis** ([``plt.gca()``] | ...)
        Specify the axis on which to plot.

:returns:

    **handle**
        The handle of the created plot.
    '''

    if axis is None:
        plt.gca()

    dset = data[key]

    if dset.attrs['artist'] == 'matplotlib.lines.Line2D':

        xy = dset[...]
        opts = {}

        for key in ['color', 'linestyle', 'marker', 'label']:
            if key in dset.attrs:
                opts[key] = dset.attrs[key]

        return axis.plot(xy, **opts)

    raise IOError('Data-set not interpretable. Please consider filing a bug-report.')
