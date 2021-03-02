#!/usr/bin/env python
# coding: utf-8

# https://github.com/jeremiedecock/neural-network-figures.git
import nnfigs.core as nnfig
import matplotlib.pyplot as plt

def tex(tex_str):
    return r"$" + tex_str + r"$"

def plot_logistic_regression_fig():
    fig, ax = nnfig.init_figure(size_x=8, size_y=4)

    nnfig.draw_synapse(ax, (0, -6), (10, 0), label=tex(r"\theta_4"), label_position=0.3, label_offset_y=-0.8, fontsize=14)
    nnfig.draw_synapse(ax, (0, -2), (10, 0), label=tex(r"\theta_3"), label_position=0.3, label_offset_y=-0.8, fontsize=14)
    nnfig.draw_synapse(ax, (0, 2),  (10, 0), label=tex(r"\theta_2"), label_position=0.3, fontsize=14)
    nnfig.draw_synapse(ax, (0, 6),  (10, 0), label=tex(r"\theta_1"), label_position=0.3, fontsize=14)

    nnfig.draw_synapse(ax, (10, 0), (12, 0))

    nnfig.draw_neuron(ax, (0, -6), 0.5, empty=True)
    nnfig.draw_neuron(ax, (0, -2), 0.5, empty=True)
    nnfig.draw_neuron(ax, (0, 2),  0.5, empty=True)
    nnfig.draw_neuron(ax, (0, 6),  0.5, empty=True)

    plt.text(x=-2.5, y=-6 - 0.2,    s=tex(r"s_4"), fontsize=14)
    plt.text(x=-2.5, y=-2 - 0.2,    s=tex(r"s_3"), fontsize=14)
    plt.text(x=-2.5, y=2 - 0.2,    s=tex(r"s_2"), fontsize=14)
    plt.text(x=-2.5, y=6 - 0.2,    s=tex(r"s_1"), fontsize=14)

    plt.text(x=12.5, y=-0.2,    s=tex(r"\pi_{\theta}(s) \in [0, 1]") + " = probability to draw the action 1 \"push RIGHT\"",  fontsize=14)
    plt.text(x=9.2,  y=-1.8, s=tex(r"x"),     fontsize=14)

    nnfig.draw_neuron(ax, (10, 0), 1, ag_func="sum", tr_func="sigmoid")

    plt.show()

