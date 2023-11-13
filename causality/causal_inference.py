from dowhy import CausalModel

import dowhy

import os
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib

from utils import scatter_plot_with_correlation_line
from configurator import configurator

matplotlib.use("TKAgg")


class Causal_inference:

    def create_model(self, df):
        """
        https://en.wikipedia.org/wiki/Graph_Modelling_Language
        """

        c = configurator()

        graph = c.get_causal_graph()

        model = CausalModel(
            data=df,
            treatment=c.get_treatment(),
            outcome=c.get_outcome(),
            graph=graph,
        )

        # Figure 1.
        # use checkbox to enable or disable it, or config file
        scatter_plot_with_correlation_line(df[c.get_treatment()],
                                           df[c.get_outcome()])

        # Figure 2.
        plt.figure("Fig. 2. Manually created input causal graph")
        c = configurator()
        CAUSAL_MODEL_FILE = os.path.join(c.get_ROOT_DIR(), 'doc',
                                         'causal_input_graph')
        model.view_model(layout="dot", file_name=CAUSAL_MODEL_FILE)
        plt.close()

        return model

    def identify_effect(self, model):
        estimand = model.identify_effect(proceed_when_unidentifiable=True)

        print("*** estimand begin ***\n")
        print(estimand)
        print("*** estimand end ***\n")

        print("*** estimand.backdoor_variables begin ***\n")
        print(estimand.backdoor_variables)
        print("*** estimand.backdoor_variables end ***\n")

        return estimand

    def estimate_effect(self, model, estimand):
        estimate = model.estimate_effect(
            identified_estimand=estimand,
            method_name="backdoor.linear_regression",
            method_params=None,
        )

        # Figure 3.
        #dowhy.plotter.plot_causal_effect(estimate, df["teljesítmény"],
        #df["CO2 kibocsátás gkm V7"])

        print("*** estimate begin ***\n")
        print(estimate)
        print("*** estimate end ***\n")

        return estimate

    def refute(self, model, estimand, estimate):
        res_random = model.refute_estimate(estimand,
                                           estimate,
                                           method_name="random_common_cause")

        print("*** random_common_cause begin ***\n")
        print(res_random)
        print("*** random_common_cause end ***\n")
