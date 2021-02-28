import colorsys
import random

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.colors import Normalize
import numpy as np


def list_colormaps():
    return plt.colormaps()


def parse_colormap(colormap):
    if colormap is None:
        _colormap = colormap
    elif type(colormap) == str:
        if colormap.lower() == "none":
            _colormap = None
        elif colormap.lower() == "baker":
            from matplotlib.colors import LinearSegmentedColormap
            import flow_vis

            colorw = flow_vis.make_colorwheel()
            _colormap = LinearSegmentedColormap.from_list('Baker', colorw / 255)
        else:
            assert colormap in plt.colormaps()
            _colormap = plt.cm.get_cmap(colormap)
    else:
        _colormap = colormap

    return _colormap


# color functions
def create_color(use_alpha=False):
    hue, saturation, luminance = random.random(), 0.5 + random.random() / 2.0, 0.6 + random.random() / 5.0
    red, green, blue = colorsys.hls_to_rgb(hue, saturation, luminance)

    if use_alpha:
        return np.array([red, green, blue, 1])
    else:
        return np.array([[[red, green, blue]]])


def get_colors(inputs, colormap, colormap_min=None, colormap_max=None):
    if colormap_min is None and colormap_max is None:
        percentile = np.nanpercentile(inputs, [0.1, 99.9])
        max_value = round(np.max(np.abs(percentile)), 2)
        norm = matplotlib.colors.TwoSlopeNorm(0, -max_value, max_value)
        colormap_min = -max_value
        colormap_max = max_value
    else:
        if colormap_min is None:
            colormap_min = np.min(inputs)
        if colormap_max is None:
            colormap_max = np.max(inputs)
        norm = matplotlib.colors.Normalize(colormap_min, colormap_max)
    return colormap(norm(inputs)), colormap_min, colormap_max


def save_colorwheel(colormap,
                    filename=None,
                    figsize=(8, 8)):
    """
    Output colormap as a color wheel

    Parameters
    ----------
    colormap : str or None
        Colormap to plot
    output_folder : str
        Folder name that will be created in the main directory to store the vector trace images
    filename : str
        File name of the output
    figsize : (int, int)
        Size of output figure

    Returns
    -------

    See Also
    --------

    """
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        # See: https://stackoverflow.com/questions/31940285/plot-a-polar-color-wheel-based-on-a-colormap-using-python-matplotlib
        # Generate a figure with a polar projection
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection='polar')

        # Define colormap normalization for 0 to 2*pi
        norm = Normalize(np.pi, 3 * np.pi)

        # Plot a color mesh on the polar plot
        # with the color set by the angle
        n = 500  # the number of secants for the mesh
        t = np.linspace(np.pi, 3 * np.pi, n)  # theta values
        r = np.linspace(.8, 1, 2)  # radius values change 0.6 to 0 for full circle
        rg, tg = np.meshgrid(r, t)  # create a r,theta meshgrid
        c = tg  # define color values as theta value
        ax.pcolormesh(t, r, c.T, shading='auto', norm=norm,
                      cmap=colormap)  # plot the colormesh on axis with colormap
        ax.set_yticklabels([])  # turn of radial tick labels (yticks)
        ax.tick_params(pad=20, labelsize=24)  # cosmetic changes to tick labels
        ax.spines['polar'].set_visible(False)  # turn off the axis spine.

        if filename is not None:
            fig.savefig(filename, dpi=200)

        fig.canvas.draw()
        buf = fig.canvas.buffer_rgba()
        colorwheel = np.asarray(buf, dtype=np.uint8)[..., :3]
        colorwheel = colorwheel[np.newaxis, ...]  # to facilitate loading into the imageviewer widget
        plt.close(fig)

        return colorwheel


def save_colorbar(colormap, filename=None, colormap_min=-1, colormap_max=1, orientation='horizontal'):
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        fig, ax = plt.subplots(figsize=(6, 1))
        fig.subplots_adjust(bottom=0.5)

        norm = matplotlib.colors.Normalize(vmin=colormap_min, vmax=colormap_max)

        fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=colormap),
                     cax=ax, orientation=orientation)
        plt.xticks(fontsize=18)
        plt.tight_layout()

        if filename is not None:
            fig.savefig(filename, dpi=200)

        fig.canvas.draw()
        buf = fig.canvas.buffer_rgba()
        colorbar = np.asarray(buf, dtype=np.uint8)[..., :3]
        colorbar = colorbar[np.newaxis, ...]  # to facilitate loading into the imageviewer widget
        plt.close(fig)

        return colorbar
