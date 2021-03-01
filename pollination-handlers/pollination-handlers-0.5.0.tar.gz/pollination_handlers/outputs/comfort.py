"""Handlers for comfort mapping simulation."""
import os
import json


def read_comfort_percent_from_folder(result_folder):
    """Read comfort percent values from a folder with .csv result files.

    The result with be a matrix with each sub-list containing the percent
    values for each of the sensor grids.
    """
    # check that the required files are present
    if not os.path.isdir(result_folder):
        raise ValueError('Invalid result folder: %s' % result_folder)
    grid_json = os.path.join(result_folder, 'grids_info.json')
    if not os.path.isfile(grid_json):
        raise ValueError('Result folder contains no grids_info.json.')

    # load the list of grids and gather all of the results
    with open(grid_json) as json_file:
        grid_list = json.load(json_file)
    results = []
    for grid in grid_list:
        result_file = os.path.join(result_folder, '{}.csv'.format(grid['id']))
        if os.path.isfile(result_file):
            with open(result_file) as inf:
                results.append([float(line) for line in inf])
    return results
