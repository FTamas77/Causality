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

from utils import scatter_plot_with_correlation_line, read_input_data

import matplotlib
matplotlib.use('TKAgg')

#######################
### Read input data ###
#######################

keep_cols = ["teljesítmény", "CO2 kibocsátás gkm V7",
             "hengerűrtartalom", "Elhaladási zaj dBA", "motor működési mód"]

list_of_files = ['KV-41762_202301_test.xlsx']

df = read_input_data(keep_cols, list_of_files)


patternDel = "Diesel|Otto"
filter = df['motor működési mód'].str.contains(patternDel) == False
df = df[~filter]


df['motor működési mód'].replace("Diesel", 0, inplace=True)
df['motor működési mód'].replace("Otto", 1, inplace=True)

print("\nSize of the input data: " +
      str(df.shape[0]) + "x" + str(df.shape[1]) + "\n\nAnd the input data:\n")
print(df)

########################
### Create the model ###
########################

# structural causal model (SCM)
# NetworkX is used
graph = """graph    [
                                    directed 1    
                                    node [id "hengerűrtartalom" label "hengerűrtartalom"]
                                    node [id "teljesítmény" label "teljesítmény"]
                                    node [id "Elhaladási zaj dBA" label "Elhaladási zaj dBA"]
                                    node [id "CO2 kibocsátás gkm V7" label "CO2 kibocsátás gkm V7"]
                                    node [id "motor működési mód" label "motor működési mód"]
                                    edge [source "hengerűrtartalom" target "teljesítmény"]
                                    edge [source "hengerűrtartalom" target "CO2 kibocsátás gkm V7"]
                                    edge [source "teljesítmény" target "Elhaladási zaj dBA"]
                                    edge [source "teljesítmény" target "CO2 kibocsátás gkm V7"]
                                    edge [source "Elhaladási zaj dBA" target "CO2 kibocsátás gkm V7"]
                                    edge [source "motor működési mód" target "CO2 kibocsátás gkm V7"]
                    ]"""

# Note:
# something similar called inside of CausalModel(...)
# nx.read_gml("KV-41762_202301_test.xlsx")

########################
### Create the model ###
########################

# API: https://www.pywhy.org/dowhy/v0.10.1/dowhy.html#dowhy.causal_model.CausalModel
model = CausalModel(
    data=df,
    treatment='motor működési mód',
    outcome='CO2 kibocsátás gkm V7',
    graph=graph
)

model.view_model(layout="dot")
display(Image(filename="causal_model.png"))


#######################
### Identify effect ###
#######################

estimand = model.identify_effect(proceed_when_unidentifiable=True)
print("**** Estimand:\n")
print(estimand)
print("estimand.backdoor_variables:\n")
print(estimand.backdoor_variables)

#######################
### Estimate effect ###
#######################
causal_estimate_strat = model.estimate_effect(estimand,
                                              method_name="backdoor.propensity_score_matching",
                                              target_units="att")
print(causal_estimate_strat)
print("Causal Estimate is " + str(causal_estimate_strat.value))


# Plot Slope of line between action and outcome = causal effect
dowhy.plotter.plot_causal_effect(
    estimate, df["motor működési mód"], df["CO2 kibocsátás gkm V7"])


print("**** estimate:\n")
print(estimate)
print("Causal Estimate is " + str(estimate.value))

##################
### Refutation ###
##################

res_random = model.refute_estimate(
    estimand, estimate, method_name="random_common_cause")
print(res_random)
