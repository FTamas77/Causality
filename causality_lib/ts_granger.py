import matplotlib
import matplotlib.pyplot as plt

import pandas as pd

from statsmodels.tsa.stattools import grangercausalitytests

from ts_configurator import config_bubi

#
# https://www.statology.org/granger-causality-test-in-python/
#


class ts_granger:
    def __init__(self, config) -> None:
        self.config = config

    def prepare_input_dataset(self, parameters):
        self.data = self.config.read_causal_discovery_dataset(
            parameters, resample=False
        )
        self.parameters = parameters

    def plot_prepared_data(self):
        plt.figure("Prepared input data")

        # plot the intervention and the control
        fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)

        axs[0].set_title("intervention")
        axs[0].plot(self.data[parameters[0]], color="tab:green")

        axs[1].set_title("control")
        axs[1].plot(self.data[parameters[1]], color="tab:blue")

    def run_granger_causality_test(self):
        grangercausalitytests(self.data[[parameters[0], parameters[1]]], maxlag=[10])


if __name__ == "__main__":
    config = config_bubi()
    my_run = ts_granger(config)
    # parameters = ["precipitation", "end_trip_no"]
    parameters = ["end_trip_no", "precipitation"]
    my_run.prepare_input_dataset(parameters)
    my_run.plot_prepared_data()
    my_run.run_granger_causality_test()

    # another example, this shall work
    url = (
        "https://raw.githubusercontent.com/Statology/Miscellaneous/main/chicken_egg.txt"
    )
    df = pd.read_csv(url, sep="  ")
    df.head()
    grangercausalitytests(df[["chicken", "egg"]], maxlag=[3])

    print("end")
