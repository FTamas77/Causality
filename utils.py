import matplotlib.pyplot as plt

import pandas as pd
import numpy as np


def read_input_data(keep_cols, list_of_files):
    """ Read the input data from excel file and returns a pandas dataframe. """

    df = pd.read_excel(list_of_files[0], skiprows=2)

    df.columns = df.columns.str.replace(r'[', '')
    df.columns = df.columns.str.replace(r']', '')
    df.columns = df.columns.str.replace(r'.', '')
    df.columns = df.columns.str.replace(r'/', '')
    df.columns = df.columns.str.replace(r'(', '')
    df.columns = df.columns.str.replace(r')', '')
    df.columns = df.columns.str.replace(r'-', '')
    # df.columns = df.columns.str.replace(r' ', '')
    df.columns = df.columns.str.replace(r'%', '')

    # remove not used columns
    df = df[keep_cols]

    # remove nan lines
    df = df.dropna()
    return df


def scatter_plot_with_correlation_line(x, y, graph_filepath):
    """ Plots the input columns """

    # Create scatter plot
    plt.scatter(x, y, c="#c23424")

    # Add correlation line
    axes = plt.gca()
    m, b = np.polyfit(x, y, 1)
    X_plot = np.linspace(axes.get_xlim()[0], axes.get_xlim()[1], 100)

    plt.title("Input data")
    plt.xlabel('teljesítmény')
    plt.ylabel("CO2 kibocsátás gkm V7")

    plt.plot(X_plot, m*X_plot + b, '-')

    plt.show()
