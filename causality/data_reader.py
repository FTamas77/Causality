import os
import pandas as pd
from configurator import configurator
from utils import scatter_plot_with_correlation_line


class data_reader:

    @staticmethod
    def read_input_data(keep_cols, list_of_files):

        c = configurator()
        list_of_files_with_path = []
        for file in list_of_files:
            input_file = os.path.join(c.get_INPUT_DATA_DIR(), file)
            list_of_files_with_path.append(input_file)

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

        # use checkbox to enable or disable it
        scatter_plot_with_correlation_line(df['teljesítmény'],
                                           df["CO2 kibocsátás gkm V7"])
        return retdf
