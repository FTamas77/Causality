from utils import read_input_data
import cdt
import networkx as nx

# https://github.com/FenTechSolutions/CausalDiscoveryToolbox/issues/81
cdt.SETTINGS.rpath = 'C:/Program Files/R/R-4.3.1/bin/Rscript.exe'


# g = nx.DiGraph()  # initialize a directed graph
# l = list(g.nodes())  # list of nodes in the graph
# a = nx.adj_matrix(g).todense()  # Output the adjacency matrix of the graph
# e = list(g.edges())  # list of edges in the graph

#######################
### Read input data ###
#######################

keep_cols = ["teljesítmény", "CO2 kibocsátás gkm V7",
             "hengerűrtartalom", "Elhaladási zaj dBA"]

list_of_files = ['KV-41762_202301_test.xlsx']

df = read_input_data(keep_cols, list_of_files)

###############
### Predict ###
###############

# https://fentechsolutions.github.io/CausalDiscoveryToolbox/html/tutorial_1.html
# skeleton object is a networkx.Graph
glasso = cdt.independence.graph.Glasso()
skeleton = glasso.predict(df)
print(skeleton)
print(nx.adjacency_matrix(skeleton).todense())

new_skeleton = cdt.utils.graph.remove_indirect_links(skeleton, alg='aracne')
print(nx.adjacency_matrix(new_skeleton).todense())

model = cdt.causality.graph.GES()
output_graph = model.predict(df, new_skeleton)
print(nx.adjacency_matrix(output_graph).todense())
