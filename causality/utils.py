import matplotlib.pyplot as plt

import numpy as np


def scatter_plot_with_correlation_line(x, y):
    """ Plots the input columns
    Now, only the inference uses this function. """

    plt.scatter(x, y, c="#c23424")

    axes = plt.gca()
    m, b = np.polyfit(x, y, 1)
    X_plot = np.linspace(axes.get_xlim()[0], axes.get_xlim()[1], 100)

    plt.xlabel('Performance')
    plt.ylabel("CO2 emission")

    plt.plot(X_plot, m * X_plot + b, '-')

    # Figure 1
    plt.figure("Fig. 1: scatter_plot_with_correlation_line")
    plt.show(block=False)
    plt.close()
