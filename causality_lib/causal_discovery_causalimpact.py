from causalimpact import CausalImpact

import numpy as np
import pandas as pd

import os
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

from causal_discovery_tigramite import config_bubi


class Causal_discovery_on_time_series_with_intervention:
    def prepare_input_dataset(self):
        self.config = config_bubi()
        self.dataframe = self.config.prepare_dataset()

    def plot_prepared_data(self):
        plt.figure("Prepared input data")

        fig, axs = plt.subplots(
            nrows=len(self.config.selected_parameters), ncols=1, sharex=True
        )

        for index, param in enumerate(self.config.selected_parameters):
            axs[index].set_title(param)
            axs[index].plot(self.dataframe[param], color="tab:green")

        plt.show()


if __name__ == "__main__":
    my_run = Causal_discovery_on_time_series_with_intervention()
    my_run.prepare_input_dataset()
    my_run.plot_prepared_data()
    print("end")
