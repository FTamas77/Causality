#
# Based on: https://github.com/jakobrunge/tigramite/blob/master/tutorials/causal_discovery/tigramite_tutorial_causal_discovery_overview.ipynb
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


from causality_ts_configurator import config_bubi
from causality_ts_configurator import config_co2mpas


class Causal_discovery_on_time_series:
    def __str__(self):
        return "Causal_discovery_on_time_series"

    def __init__(self):
        self.config = config_bubi()
        # self.config = config_co2mpas()

    def prepare_input_dataset(self):
        # TODO: only read the data
        self.dataframe = self.config.only_read_dataset()
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

        self.dataframe = pp.DataFrame(
            self.dataframe.to_numpy(),
            mask=None,
            var_names=self.config.selected_parameters,
        )

        parcorr = ParCorr(significance="analytic")
        pcmci = PCMCI(dataframe=self.dataframe, cond_ind_test=parcorr, verbosity=1)

        pcmci.verbosity = 1
        # TODO: we use it in the next function
        self.results = pcmci.run_pcmci(tau_max=8, pc_alpha=None, alpha_level=0.01)

        print("p-values")
        print(self.results["p_matrix"].round(3))

        print("MCI partial correlations")
        print(self.results["val_matrix"].round(2))

        #
        # False-discovery rate control
        #

        q_matrix = pcmci.get_corrected_pvalues(
            p_matrix=self.results["p_matrix"], tau_max=8, fdr_method="fdr_bh"
        )

        pcmci.print_significant_links(
            p_matrix=q_matrix, val_matrix=self.results["val_matrix"], alpha_level=0.01
        )

        graph = pcmci.get_graph_from_pmatrix(
            p_matrix=q_matrix,
            alpha_level=0.01,
            tau_min=0,
            tau_max=8,
            link_assumptions=None,
        )

        self.results["graph"] = graph

    def plotting(self):
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

        # export results
        # tp.write_csv(val_matrix=results["val_matrix"], graph=results["graph"],
        #              var_names=var_names,save_name="test_graph.csv", digits=5)


# TODO: Integrating expert assumptions about links
# "Often one may have prior knowledge about the existence or absence of links and their orientations.
# Such expert knowledge can be intergrated via the link_assumptions argument.""

if __name__ == "__main__":
    alg = Causal_discovery_on_time_series()
    alg.prepare_input_dataset()
    alg.plot_prepared_data()
    # alg.data_depedencies_and_lag_fn()
    alg.PCMCI_causal_discovery()
    alg.plotting()

    print("Exiting..")