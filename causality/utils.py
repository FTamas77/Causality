import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

import io
import os
from pathlib import Path

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
INPUT_DATA_DIR = os.path.join(ROOT_DIR, 'input_data')


def read_input_data(keep_cols, list_of_files):
    """ Read the input data from excel file and returns a pandas dataframe. """

    list_of_files_with_path = []
    for file in list_of_files:
        input_file = os.path.join(INPUT_DATA_DIR, file)
        list_of_files_with_path.append(input_file)

    # TODO: store it and not calculate again (during one running, we use the same input)
    retdf = pd.DataFrame()
    for file in list_of_files_with_path:
        df = pd.read_excel(file, skiprows=2)

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

        retdf = pd.concat([retdf, df], ignore_index=True)

    return retdf


def scatter_plot_with_correlation_line(x, y):
    """ Plots the input columns """

    plt.scatter(x, y, c="#c23424")

    axes = plt.gca()
    m, b = np.polyfit(x, y, 1)
    X_plot = np.linspace(axes.get_xlim()[0], axes.get_xlim()[1], 100)

    plt.xlabel('Performance')
    plt.ylabel("CO2 emission")

    plt.plot(X_plot, m*X_plot + b, '-')

    plt.show()
