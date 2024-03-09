#
# Based on:
# https://github.com/jakobrunge/tigramite/blob/master/tutorials/causal_discovery/tigramite_tutorial_causal_discovery_overview.ipynb
#
# Good starting point to read more about this topic:
# https://medium.com/causality-in-data-science/introducing-conditional-independence-and-causal-discovery-77919db6159c
#
# More about PCMCI:
# https://www.iup.uni-bremen.de/PEP_master_thesis/thesis_2020/Karmouche_MScThesis_2020.pdf
#

import os
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

from tigramite import data_processing as pp
from tigramite import plotting as tp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.parcorr import ParCorr


from ts_configurator import config_bubi
from ts_configurator import config_co2mpas


class ts_tigramite:
    def __str__(self):
        return "Causal_discovery_on_time_series"

    def __init__(self, config):
        self.config = config

    def prepare_input_dataset(self):
        self.dataframe = self.config.read_causal_discovery_dataset()
        print(self.dataframe)
        print(type(self.dataframe))

    def plot_prepared_data(self):
        fig, axs = plt.subplots(
            nrows=len(self.config.selected_parameters), ncols=1, sharex=True
        )

        fig.suptitle("Selected parameters")
        for index, param in enumerate(self.config.selected_parameters):
            axs[index].set_title(param)
            axs[index].plot(self.dataframe[param], color="tab:green")
        plt.show()

    def PCMCI_causal_discovery(self):

        # TODO: why is it needed? -> var_names
        self.dataframe = pp.DataFrame(
            self.dataframe.to_numpy(),
            mask=None,
            var_names=self.config.selected_parameters,
        )

        parcorr = ParCorr(significance="analytic")
        pcmci = PCMCI(dataframe=self.dataframe, cond_ind_test=parcorr, verbosity=1)

        pcmci.verbosity = 1

        self.results = pcmci.run_pcmci(tau_max=8, pc_alpha=None, alpha_level=0.01)

    def show_results(self):
        tp.plot_graph(
            val_matrix=self.results["val_matrix"],
            graph=self.results["graph"],
            var_names=self.config.selected_parameters,
            link_colorbar_label="cross-MCI",
            node_colorbar_label="auto-MCI",
            show_autodependency_lags=False,
        )
        plt.show()

        tp.plot_time_series_graph(
            figsize=(6, 4),
            val_matrix=self.results["val_matrix"],
            graph=self.results["graph"],
            var_names=self.config.selected_parameters,
            link_colorbar_label="MCI",
        )
        plt.show()


# TODO: Integrating expert assumptions about links
# "Often one may have prior knowledge about the existence or absence of links and their orientations.
# Such expert knowledge can be intergrated via the link_assumptions argument.""

if __name__ == "__main__":

    bubi = config_bubi()
    # co2mpas = config_co2mpas()

    alg = ts_tigramite(bubi)

    alg.prepare_input_dataset()
    alg.plot_prepared_data()

    alg.PCMCI_causal_discovery()
    alg.show_results()

    print("Exiting..")
