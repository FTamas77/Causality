from causallearn.search.FCMBased.lingam.utils import make_dot
from causallearn.search.FCMBased import lingam
from causallearn.search.ConstraintBased.FCI import fci
from causallearn.search.ConstraintBased.PC import pc
from causallearn.utils.GraphUtils import GraphUtils

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

import io

from utils import read_input_data

import networkx as nx


#######################
### Read input data ###
#######################

keep_cols = ["teljesítmény", "CO2 kibocsátás gkm V7",
             "hengerűrtartalom", "Elhaladási zaj dBA"]

#   "Összevont átlagfogy", "Korr abszorp együttható", "kilométeróra állás", "gy fogy ért orszúton"]


list_of_files = ['KV-41762_202301_test.xlsx']

df = read_input_data(keep_cols, list_of_files)

print("Header:\n")
print(df.head())
print("Numpy:\n")
print(df.to_numpy())


###########
### PCI ###
###########

# https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html#usage

# default parameters
cg = pc(df.to_numpy())

# visualization using pydot
# cg.draw_pydot_graph()

# use translated versio for plots
keep_cols = ["Performance", "CO2 emission",
             "Cylinder cap.", "Passing noise"]
# "Sum. consumption", "Corr. abs. co.", "Actual kilometers", "Cons. on roads"]

pyd = GraphUtils.to_pydot(cg.G, labels=keep_cols)
pyd.write_png('pc.png')
# tmp_png = pyd.create_png(f="png")
# fp = io.BytesIO(tmp_png)
# img = mpimg.imread(fp, format='png')
# plt.axis('off')
# plt.imshow(img)
# plt.show()


# visualization using networkx
# cg.to_nx_graph()
# cg.draw_nx_graph(skel=False)


###########
### FCI ###
###########

# default parameters
g, edges = fci(df.to_numpy())

# visualization

pdy = GraphUtils.to_pydot(g, labels=keep_cols)
pdy.write_png('fci.png')

#################
### ICALiNGAM ###
#################

model = lingam.ICALiNGAM()
model.fit(df.to_numpy())

make_dot(model.adjacency_matrix_, labels=keep_cols)
# Obtain valid dot format
# graph_dot = make_graph(model.adjacency_matrix_, labels=labels)
