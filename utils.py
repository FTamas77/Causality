import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from pandas import DataFrame
from typing import Set, Any


def remove_others(df: DataFrame, columns: Set[Any]):
    cols_total: Set[Any] = set(df.columns)
    diff: Set[Any] = cols_total - columns
    df.drop(diff, axis=1, inplace=True)


def scatter_plot_with_correlation_line(x, y, graph_filepath):
    """ Plots the input columns """

    # Create scatter plot
    plt.scatter(x, y, c="#c23424")

    # Add correlation line
    axes = plt.gca()
    m, b = np.polyfit(x, y, 1)
    X_plot = np.linspace(axes.get_xlim()[0], axes.get_xlim()[1], 100)

    plt.xlabel('teljesítmény')
    plt.ylabel("CO2 kibocsátás gkm V7")

    plt.plot(X_plot, m*X_plot + b, '-')

    plt.show()
