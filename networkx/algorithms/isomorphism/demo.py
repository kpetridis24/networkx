import collections
import random
import time

import networkx as nx
from networkx.algorithms.isomorphism.VF2pp import VF2pp

# Graph initialization
# G1 = nx.gnp_random_graph(350, 0.7, 42)
# G2 = nx.gnp_random_graph(350, 0.7, 42)
#
# colors = [
#     "white",
#     "black",
#     "green",
#     "purple",
#     "orange",
#     "red",
#     "blue",
#     "pink",
#     "yellow",
#     "none",
# ]
#
# # VF2++ initialization
# for node in G1.nodes():
#     color = colors[random.randrange(0, len(colors))]
#     G1.nodes[node]["label"] = color
#     G2.nodes[node]["label"] = color
#
# G1_labels = nx.get_node_attributes(G1, "label")
# G2_labels = nx.get_node_attributes(G2, "label")
#
# # VF2++
# t0 = time.time()
# m = VF2pp(G1, G2, G1_labels, G2_labels)
# print(f"VF2++ elapsed time: {time.time() - t0}")
#
# assert m
#
# t0 = time.time()
# nx.is_isomorphic(G1, G2)
# print(f"VF2 elapsed time: {time.time() - t0}")

# G1 = nx.MultiGraph([(i, j) for i in range(250) for j in range(65)] * 10)
# G2 = nx.MultiGraph([(i, j) for i in range(250) for j in range(65)] * 10)
#
# for node in G1.nodes():
#     G1.nodes[node]["label"] = "blue"
#     G2.nodes[node]["label"] = "blue"
#
# G1_labels = nx.get_node_attributes(G1, "label")
# G2_labels = nx.get_node_attributes(G2, "label")
#
# t0 = time.time()
# m = VF2pp(G1, G2, G1_labels, G2_labels)
# print(f"VF2 elapsed time: {time.time() - t0}")
#
# assert m
from networkx.algorithms.isomorphism.vf2userfunc import *

g1edges = [
    ["a", "g"],
    ["a", "h"],
    ["a", "i"],
    ["b", "g"],
    ["b", "h"],
    ["b", "j"],
    ["c", "g"],
    ["c", "i"],
    ["c", "j"],
    ["d", "h"],
    ["d", "i"],
    ["d", "j"],
]

g2edges = [
    [1, 2],
    [2, 3],
    [3, 4],
    [4, 1],
    [5, 6],
    [6, 7],
    [7, 8],
    [8, 5],
    [1, 5],
    [2, 6],
    [3, 7],
    [4, 8],
]

g1 = nx.Graph()
g2 = nx.Graph()
g1.add_edges_from(g1edges)
g2.add_edges_from(g2edges)
g3 = g2.subgraph([1, 2, 3, 4])

for n1 in g1.nodes():
    g1.nodes[n1]["label"] = "red"
for n3 in g3.nodes():
    g3.nodes[n3]["label"] = "red"

l1, l3 = nx.get_node_attributes(g1, "label"), nx.get_node_attributes(g3, "label")

gm = GraphMatcher(g1, g3)
print(gm.subgraph_is_isomorphic())
print(VF2pp(g1, g3, l1, l3))
