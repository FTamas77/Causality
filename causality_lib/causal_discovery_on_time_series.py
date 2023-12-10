import os
from pathlib import Path
import pandas as pd
from matplotlib import pyplot as plt

from tigramite import data_processing as pp
from tigramite import plotting as tp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.parcorr import ParCorr

#
# Based on: https://github.com/jakobrunge/tigramite/blob/master/tutorials/causal_discovery/tigramite_tutorial_causal_discovery_overview.ipynb
#

# outcome: co2_emissions

# temporally removed:
# "engine_temperature_derivatives",
# "wheel_speeds",
#  "motor_p1_maximum_powers",
# "active_cylinders",

#  it is in different file: "velocities",

# TODO: temporally copied here from ontology.py
selected_parameters = [
    "engine_temperatures",
    "motor_p0_speeds",
    "engine_powers_out",
    "co2_emissions",
    "fuel_consumptions_liters_value",
]

# Good starting point to read more about this topic:
# https://medium.com/causality-in-data-science/introducing-conditional-independence-and-causal-discovery-77919db6159c
#
# More about PCMCI:
# https://www.iup.uni-bremen.de/PEP_master_thesis/thesis_2020/Karmouche_MScThesis_2020.pdf
#


class Causal_discovery_on_time_series:
    __ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
    __INPUT_DATA_FILE = os.path.join(
        __ROOT_DIR, "co2mpas", "output", "20231118_142209-co2mpas_conventional.xlsx"
    )

    def __str__(self):
        return "Causal_discovery_on_time_series"

    def __init__(self, selected_parameters):
        self.selected_parameters = selected_parameters
        return

    def prepare_input_dataset(self):
        """
        Input: requested parameters and the files
        Output: dataframe object has been created.

        self.nedc_h
        self.dataframe
        """

        # output.prediction.nedc_h.ts
        self.nedc_h = pd.read_excel(
            self.__INPUT_DATA_FILE,
            sheet_name="output.prediction.nedc_h.ts",
            skiprows=1,
            index_col="times",
            nrows=1500,
        )

        self.nedc_h = self.nedc_h[selected_parameters]
        print(self.nedc_h.to_string(index=True, max_rows=10))

        self.dataframe = pp.DataFrame(
            self.nedc_h.to_numpy(), var_names=self.selected_parameters
        )

    def plot_prepared_data(self):
        """
        Check things like:
            Stationary and
            Doesn't contain missing values
            Lagged dependencies
        """

        plt.figure("Prepared input data")
        fig, axs = plt.subplots(
            nrows=len(self.selected_parameters), ncols=1, sharex=True
        )
        fig.suptitle("Selected parameters")

        for index, param in enumerate(self.selected_parameters):
            axs[index].set_title(param)
            axs[index].plot(self.nedc_h[param], color="tab:green")

    def data_depedencies_and_lag_fn(self):
        """
        Investigating data dependencies and lag functions

        tau_max: maximum time lag
        """

        # First investigation:
        matrix_lags = None
        tp.plot_scatterplots(
            name="plot_scatterplots",
            dataframe=self.dataframe,
            add_scatterplot_args={"matrix_lags": matrix_lags},
        )
        plt.show()

        # Second investigation:
        tp.plot_densityplots(
            name="plot_densityplots",
            dataframe=self.dataframe,
            add_densityplot_args={"matrix_lags": matrix_lags},
        )
        plt.show()

        # Next: plot the lagged unconditional dependencies
        parcorr = ParCorr(significance="analytic")

        # Lagged unconditional dependencies -> helps to find the tau
        pcmci = PCMCI(dataframe=self.dataframe, cond_ind_test=parcorr, verbosity=1)

        correlations = pcmci.get_lagged_dependencies(tau_max=20, val_only=True)[
            "val_matrix"
        ]

        lag_func_matrix = tp.plot_lagfuncs(
            name="plot_lagfuncs",
            val_matrix=correlations,
            setup_args={
                "var_names": self.selected_parameters,
                "x_base": 5,
                "y_base": 0.5,
            },
        )
        plt.show()

    def PCMCI_causal_discovery(self):
        """
        _summary_
        """

        # TODO: we have already created this in the prev function
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
        """ """

        tp.plot_graph(
            val_matrix=self.results["val_matrix"],
            graph=self.results["graph"],
            var_names=self.selected_parameters,
            link_colorbar_label="cross-MCI",
            node_colorbar_label="auto-MCI",
            show_autodependency_lags=False,
        )
        plt.show()

        tp.plot_time_series_graph(
            figsize=(6, 4),
            val_matrix=self.results["val_matrix"],
            graph=self.results["graph"],
            var_names=self.selected_parameters,
            link_colorbar_label="MCI",
        )
        plt.show()

        # export results
        # tp.write_csv(val_matrix=results["val_matrix"], graph=results["graph"],
        #              var_names=var_names,save_name="test_graph.csv", digits=5)


# TODO: Integrating expert assumptions about links
# "Often one may have prior knowledge about the existence or absence of links and their orientations.
# Such expert knowledge can be intergrated via the link_assumptions argument.""

alg = Causal_discovery_on_time_series(selected_parameters)
alg.prepare_input_dataset()
# Optional:
# alg.plot_prepared_data()
# alg.data_depedencies_and_lag_fn()
alg.PCMCI_causal_discovery()
alg.plotting()

print("Exiting..")
