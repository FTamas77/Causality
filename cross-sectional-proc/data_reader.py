import os
import pandas as pd
from configurator import configurator
from utils import scatter_plot_with_correlation_line


class data_reader:
    """
    Simple static method:
    It reads only the selected columns and returns the pandas data frame.
    """

    @staticmethod
    def read_input_data(causality_scenario="Causal inference"):

        c = configurator()
        if causality_scenario == "Causal inference":
            keep_cols = c.get_causal_inference_keep_cols()
        else:
            keep_cols = c.get_causal_discovery_keep_cols()

        # TODO: this could be done by the configurator
        list_of_files_with_path = []
        for file in c.applied_input_files:
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

            df = df[keep_cols]

            # remove nan lines
            df = df.dropna()

            retdf = pd.concat([retdf, df], ignore_index=True)

        return retdf
