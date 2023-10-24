
from utils import scatter_plot_with_correlation_line, read_input_data


class data_reader:

    def __init__(self, input_files):
        self.input_files = input_files
        self.df = None

    def read_input_data(self, keep_cols):
        self.df = read_input_data(keep_cols, self.input_files)
        return self.df

    def print_numpy():
        if self.df is not None:
            print("**** Numpy:\n")
            print(self.df.to_numpy())

    def print_pandas_frame():
        if self.df is not None:
            print("**** Header:\n")
            print(self.df.head())

    def print_size():
        if self.df is not None:
            print("\nSize of the input data: " +
                  str(df.shape[0]) + "x" + str(df.shape[1]) + "\n\n")
