
from utils import scatter_plot_with_correlation_line, read_input_data


class data_reader:

    def __init__(self, input_files):
        self.input_files = input_files

    def read_input_data(self, keep_cols):
        df = read_input_data(keep_cols, self.input_files)
        return df

    """
    
        print(df)

        print("**** Header:\n")
        print(df.head())

        print("**** Numpy:\n")
        print(df.to_numpy())
       
               print("\nSize of the input data: " +
              str(df.shape[0]) + "x" + str(df.shape[1]) + "\n\nAnd the input data:\n")
        print(df)

        # correlation between the treatment and the outcome
        scatter_plot_with_correlation_line(
            df['teljesítmény'], df["CO2 kibocsátás gkm V7"])
        
    """
