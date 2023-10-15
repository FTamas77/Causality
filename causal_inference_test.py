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

from utils import scatter_plot_with_correlation_line, remove_others

import matplotlib
matplotlib.use('TKAgg')

#
# Create the graph
# In the first step, the model is created by hand
#
df = pd.read_excel('KV-41762_202301_test.xlsx', skiprows=2)


df.columns = df.columns.str.replace(r'[', '')
df.columns = df.columns.str.replace(r']', '')
df.columns = df.columns.str.replace(r'.', '')
df.columns = df.columns.str.replace(r'/', '')
df.columns = df.columns.str.replace(r'(', '')
df.columns = df.columns.str.replace(r')', '')
df.columns = df.columns.str.replace(r'-', '')
# df.columns = df.columns.str.replace(r' ', '')
df.columns = df.columns.str.replace(r'%', '')


col_list = ["teljesítmény", "CO2 kibocsátás gkm V7",
            "hengerűrtartalom", "Elhaladási zaj dBA", ]
df = df[col_list]
df = df.dropna()  # remove nans
print(df)
print(df.size)


# print the selected values to see the correlation between them
scatter_plot_with_correlation_line(
    df['teljesítmény'], df["CO2 kibocsátás gkm V7"], 'scatter_plot.png')

# print(df)
# print(list(df.columns.values))

# structural causal model (SCM)
# therefore NetworkX is used
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

# something similar called inside of CausalModel(...)
# nx.read_gml("KV-41762_202301_test.xlsx")

#
# Create the model
#
# API: https://www.pywhy.org/dowhy/v0.10.1/dowhy.html#dowhy.causal_model.CausalModel
#
model = CausalModel(
    data=df,
    treatment='teljesítmény',
    outcome='CO2 kibocsátás gkm V7',
    graph=graph
)

# print(model.view_model())

model.view_model(layout="dot")
display(Image(filename="causal_model.png"))


#
# Identify effect
#
estimand = model.identify_effect(proceed_when_unidentifiable=True)
print(estimand)


#
# Estimate effect
#
# Create a namedtuple to store the name of the estimator and the parameters passed
# https://github.com/py-why/dowhy/blob/main/docs/source/example_notebooks/dowhy_ranking_methods.ipynb
#
estimator_list = [
    "backdoor.linear_regression",
    # "backdoor.propensity_score_stratification",
    "backdoor.propensity_score_matching",
    "backdoor.propensity_score_weighting",
    "backdoor.econml.dml.DML",
    "backdoor.econml.dr.LinearDRLearner",
    # "backdoor.econml.metalearners.TLearner",
    # "backdoor.econml.metalearners.XLearner",
    # "backdoor.causalml.inference.meta.LRSRegressor",
    # "backdoor.causalml.inference.meta.XGBTRegressor",
    # "backdoor.causalml.inference.meta.MLPTRegressor",
    # "backdoor.causalml.inference.meta.BaseXRegressor"
]


estimate = model.estimate_effect(
    identified_estimand=estimand,
    method_name='backdoor.linear_regression')


# Plot Slope of line between action and outcome = causal effect
# dowhy.plotter.plot_causal_effect(
# estimate, df["teljesítmény"], df["CO2 kibocsátás gkm V7"])

print(estimate)
print("Causal Estimate is " + str(estimate.value))

#
# Test
#

res_random = model.refute_estimate(
    estimand, estimate, method_name="random_common_cause")
print(res_random)
