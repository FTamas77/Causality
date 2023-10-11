from IPython.display import Image, display

from dowhy import CausalModel
import dowhy

import numpy as np
import pandas as pd

import graphviz
import pygraphviz

data = pd.read_excel('KV-41762_202301_test.xlsx', skiprows=2)
print(data)


graph = """graph [directed 1 node [id "vizsga dátum" label "vizsga dátum"]
                                node [id "gyártási év" label "gyártási év"]
                                node [id "teljesítmény" label "teljesítmény"]
                                edge [source "vizsga dátum" target "teljesítmény"]
                                edge [source "vizsga dátum" target "gyártási év"]
                                edge [source "gyártási év" target "vizsga dátum"]]"""

print(graph)

model = CausalModel(
    data=data,
    treatment='gyártási év',
    outcome='teljesítmény',
    graph=graph
)

print(model.view_model())
display(Image(filename="causal_model.png"))


estimand_1 = model.identify_effect()
print(estimand_1)

estimate_1 = model.estimate_effect(
    identified_estimand=estimand_1,
    method_name='backdoor.linear_regression')
