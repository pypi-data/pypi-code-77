from bokeh.plotting import figure, output_file, show, ColumnDataSource


def show_matrix(array):
    plot = figure(tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")],
                  height=800, width=800)

    plot.x_range.range_padding = plot.y_range.range_padding = 0

    # must give a vector of image data for image parameter
    # plot.image(image=[array], x=0, y=0, dw=10, dh=10, palette="Spectral11", level="image")
    # plot.grid.grid_line_width = 0.5
    n, m = array.shape

    plot.image(image=[array], x=0, y=0, dw=m, dh=n, palette="Spectral11", level="image")
    plot.grid.grid_line_width = 0

    output_file("matrix_image.html", title="matrix")

    show(plot)
