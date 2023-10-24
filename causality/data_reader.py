from utils import scatter_plot_with_correlation_line, read_input_data


class data_reader:
    """
    it does not store the data because we keep different colls in each case
    """

    class __data_reader:
        def __init__(self, input_files):
            self.input_files = input_files

        def __str__(self):
            return repr(self) + self.input_files

    instance = None

    def __init__(self, input_files):
        if not data_reader.instance:
            data_reader.instance = data_reader.__data_reader(input_files)
        else:
            data_reader.instance.input_files = input_files

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def read_input_data(self, keep_cols):
        df = read_input_data(keep_cols, self.input_files)
        return df
