import re
import networkx as nx

from IPython.display import Image, display

from dowhy import CausalModel
import dowhy

import numpy as np
import pandas as pd

import graphviz
import pygraphviz

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

# print(df)
# print(list(df.columns.values))

graph = """graph [directed 1 node
                                [
                                    id "gyártási év" label "gyártási év"]
                                    node [id "hengerűrtartalom" label "hengerűrtartalom"]
                                    node [id "teljesítmény" label "teljesítmény"]
                                    node [id "CO V1" label "CO V1"]
                                    node [id "CO2 kibocsátás gkm V7" label "CO2 kibocsátás gkm V7"]
                                    edge [source "gyártási év" target "CO2 kibocsátás gkm V7"]
                                    edge [source "gyártási év" target "CO V1"]
                                    edge [source "teljesítmény" target "CO2 kibocsátás gkm V7"]
                                    edge [source "teljesítmény" target "CO V1"]
                                    edge [source "hengerűrtartalom" target "teljesítmény"]
                                ]"""

# something similar called inside of CausalModel(...)
# nx.read_gml("KV-41762_202301_test.xlsx")

#
# Create the model
#
model = CausalModel(
    data=df,
    treatment='teljesítmény',
    outcome='CO2 kibocsátás gkm V7',
    graph=graph
)

# print(model.view_model())
# display(Image(filename="causal_model.png"))


#
# Identify effect
#
estimand = model.identify_effect()
print(estimand)


#
# Estimate effect
#
estimate = model.estimate_effect(
    identified_estimand=estimand,
    method_name='backdoor.linear_regression')
print(estimate)


#
# Test
#
