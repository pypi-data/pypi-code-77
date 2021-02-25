""" Contains function to create figures that are to be added to TensorBoard for events logging. """
from collections import Counter
from typing import List, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np


def create_categorical_plot(value: Union[List[Tuple[int, int]], List[int], List[float]]):
    """ Checks the type of value and calls the correct plotting function accordingly.

    :param value: Output of an reducer function
    :return: plt.figure that contains a bar plot
    """
    fig = None
    if isinstance(value[0], tuple):
        # in this case, we have the discrete action events and need the relative bar plot for plotting
        fig = create_relative_bar_plot(value)
    elif isinstance(value[0], int):
        fig = create_histogram(value)
    elif isinstance(value[0], float):
        raise NotImplementedError('plotting for this data type not implemented yet')

    return fig


def create_histogram(value):
    """
    Creates simple matplotlib histogram of value.

    :param value: output of an event
    :return: plt.figure that contains a bar plot
    """
    fig = plt.figure()
    plt.hist(x=value)
    return fig


def create_relative_bar_plot(value: List[Tuple[int, int]]):
    """
    Counts the categories in value and prepares a relative bar plot of these.

    :param value: List of Tuples of (action, action_dim)
    :return: plt.figure that contains a bar plot
    """
    # This plotting function can be used by several events. depending on whether
    categories = [action_dim_tuple[0] for action_dim_tuple in value]
    action_dim = value[0][1]
    # count the action categories
    category_counts = Counter(categories)
    # assemble counts for all categories. To make sure that actions that have not been chosen are still
    # represented in the plot, fill their counts with 0s
    cat_dict = {}
    for cat in range(action_dim):
        if cat in category_counts:
            cat_dict[cat] = category_counts[cat]
        else:
            cat_dict[cat] = 0
    # make bar plot where the frequencies of the categories are divided by the sum of the frequencies
    # in order to imitate a probability distribution
    fig = plt.figure()
    plt.bar(x=cat_dict.keys(), height=np.array(list(cat_dict.values())) / sum(cat_dict.values()))
    plt.ylim([0, 1])
    return fig


def create_violin_distribution(value: List[np.ndarray]) -> None:
    """
    Creates simple matplotlib violin plot of value.

    :param value: output of an event (expected to be a list of numpy vectors)
    :return: plt.figure that contains a bar plot
    """

    # extract array
    value_array = np.stack(value)

    fig = plt.figure()
    plt.violinplot(value_array, showmeans=True)
    plt.grid(True)
    return fig
