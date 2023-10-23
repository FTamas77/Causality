import re
import networkx as nx

from IPython.display import Image, display

from dowhy import CausalModel
import dowhy.plotter
import dowhy

import numpy as np
import pandas as pd

import graphviz
import pygraphviz

import os
from pathlib import Path

import matplotlib.pyplot as plt

from utils import scatter_plot_with_correlation_line, read_input_data

import matplotlib
matplotlib.use('TKAgg')

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent


class Causal_inference:
    """Causal inference class:
    only the configuration is stored, calculated causal inference object are not """

    def __init__(self, input_files):
        self.input_files = input_files
        self.keep_cols = ["teljesítmény", "CO2 kibocsátás gkm V7",
                          "hengerűrtartalom", "Elhaladási zaj dBA"]

    def read_input_data(self):
        df = read_input_data(self.keep_cols, self.input_files)

        print("\nSize of the input data: " +
              str(df.shape[0]) + "x" + str(df.shape[1]) + "\n\nAnd the input data:\n")
        print(df)

        # correlation between the treatment and the outcome
        scatter_plot_with_correlation_line(
            df['teljesítmény'], df["CO2 kibocsátás gkm V7"])

        return df

    def create_model(self, df):
        graph = """graph    [
                                            directed 1    
                                            node [id "hengerűrtartalom" label "hengerűrtartalom"]
                                            node [id "teljesítmény" label "teljesítmény"]
                                            node [id "Elhaladási zaj dBA" label "Elhaladási zaj dBA"]
                                            node [id "CO2 kibocsátás gkm V7" label "CO2 kibocsátás gkm V7"]
                                            edge [source "hengerűrtartalom" target "teljesítmény"]
                                            edge [source "hengerűrtartalom" target "CO2 kibocsátás gkm V7"]
                                            edge [source "teljesítmény" target "Elhaladási zaj dBA"]
                                            edge [source "teljesítmény" target "CO2 kibocsátás gkm V7"]
                                            edge [source "Elhaladási zaj dBA" target "CO2 kibocsátás gkm V7"]
                            ]"""

        model = CausalModel(
            data=df,
            treatment='teljesítmény',
            outcome='CO2 kibocsátás gkm V7',
            graph=graph
        )

        # Figure 2.
        # plt.figure("Fig. 2. Manually created input causal graph")
        # CAUSAL_MODEL_FILE = os.path.join(ROOT_DIR, 'doc', 'causal_input_graph')
        # model.view_model(layout="dot", file_name=CAUSAL_MODEL_FILE)
        # plt.close()

        return model

    def identify_effect(self, model):
        estimand = model.identify_effect(proceed_when_unidentifiable=True)

        print("**** estimand:\n")
        print(estimand)

        print("**** estimand.backdoor_variables:\n")
        print(estimand.backdoor_variables)

        return estimand

    def estimate_effect(self, model, estimand):
        estimate = model.estimate_effect(
            identified_estimand=estimand,
            method_name='backdoor.linear_regression',
            method_params=None)

        print("**** estimate:\n")
        print(estimate)

        return estimate

    def refute(self, model, estimand, estimate):
        res_random = model.refute_estimate(
            estimand, estimate, method_name="random_common_cause")

        print("**** random_common_cause:\n")
        print(res_random)
