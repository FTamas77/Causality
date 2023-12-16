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


class config:
    pass


class config_bubi(config):
    __ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
    __INPUT_DATA_FILE = os.path.join(
        __ROOT_DIR, "dataset", "bubi-weather_export_2212-2312.csv"
    )

    selected_parameters = [
        "start_trip_no",
        "temperature",
        "max_wind_speed",
    ]

    def prepare_dataset(self):
        bubi = pd.read_csv(self.__INPUT_DATA_FILE, nrows=3000, index_col="ts_0")
        bubi = bubi[self.selected_parameters + ["station_name"]]

        # Change to datetime format -> we use ts_0 as index col
        # bubi["ts_0"] = pd.to_datetime(bubi["ts_0"])

        # Filter on stations
        bubi = bubi.loc[bubi["station_name"] == "0101-Batthyány tér"]

        # After filtering, remove the station name
        bubi = bubi[self.selected_parameters]

        return bubi


class config_co2mpas(config):
    __ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
    __INPUT_DATA_FILE = os.path.join(
        __ROOT_DIR, "co2mpas", "output", "20231118_142209-co2mpas_conventional.xlsx"
    )

    # TODO: outcome: co2_emissions
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

    def prepare_dataset(self):
        nedc_h = pd.read_excel(
            self.__INPUT_DATA_FILE,
            sheet_name="output.prediction.nedc_h.ts",
            skiprows=1,
            index_col="times",  # TODO: ?
            nrows=1500,
        )

        return nedc_h[self.selected_parameters]


class Causal_discovery_on_time_series:
    def __str__(self):
        return "Causal_discovery_on_time_series"

    def __init__(self):
        self.config = config_bubi()
        # self.config = config_co2mpas()

    def prepare_input_dataset(self):
        self.dataframe = self.config.prepare_dataset()

    def plot_prepared_data(self):
        fig, axs = plt.subplots(
            nrows=len(self.config.selected_parameters), ncols=1, sharex=True
        )

        fig.suptitle("Selected parameters")
        for index, param in enumerate(self.config.selected_parameters):
            axs[index].set_title(param)
            axs[index].plot(self.dataframe[param], color="tab:green")
        plt.show()

    def data_depedencies_and_lag_fn(self):
        # TODO: https://stackoverflow.com/questions/77670433/dataframe-object-has-no-attribute-n-when-i-want-to-plot-my-data
        self.dataframe = pp.DataFrame(self.dataframe.to_numpy())

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

        return

        correlations = pcmci.get_lagged_dependencies(tau_max=20, val_only=True)[
            "val_matrix"
        ]

        lag_func_matrix = tp.plot_lagfuncs(
            name="plot_lagfuncs",
            val_matrix=correlations,
            setup_args={
                "var_names": self.config.selected_parameters,
                "x_base": 5,
                "y_base": 0.5,
            },
        )
        plt.show()

    def PCMCI_causal_discovery(self):
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
    alg.data_depedencies_and_lag_fn()
    alg.PCMCI_causal_discovery()
    alg.plotting()

    print("Exiting..")
