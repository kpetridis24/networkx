import time

import networkx as nx
from networkx.algorithms.isomorphism.vf2pp_Di import vf2pp_mapping_Di

# Graph initialization
# G1 = nx.gnp_random_graph(50, 0.6, seed=42)
# G2 = nx.gnp_random_graph(50, 0.6, seed=42)
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
# c = 0
# for node in G1.nodes():
#     # if c == 400:
#     #     break
#     # if c % 3 == 0:
#     #     G1.nodes[node]["label"] = -1
#     #     G2.nodes[node]["label"] = -1
#     G1.nodes[node]["color"] = "blue"
#     G2.nodes[node]["color"] = "blue"
#     c += 1
#
# # VF2++
# t0 = time.time()
# m = nx.vf2pp_is_isomorphic(G1, G2, node_labels="color", default_label=-1)
# print(f"VF2++ elapsed time: {time.time() - t0}")

# assert m

# t0 = time.time()
# nx.is_isomorphic(G1, G2)
# print(f"VF2 elapsed time: {time.time() - t0}")

# G1 = nx.MultiGraph([(i, j) for i in range(250) for j in range(65)] * 10)
# G2 = nx.MultiGraph([(i, j) for i in range(250) for j in range(65)] * 10)
#
# for node in G1.nodes():
#     G1.nodes[node]["label"] = "blue"
#     G2.nodes[node]["label"] = "blue"

G1 = nx.DiGraph()
G1.add_edges_from([(0, 1), (3, 0), (0, 2), (1, 3), (2, 1), (1, 4), (4, 2)])

# G2 = nx.relabel_nodes(G1, mapping={0: "a", 1: "b", 2: "c", 3: "d", 4: "e"})
# # G1.add_edges_from([(1, 0), (2, 1), (1, 6), (0, 5), (3, 0), (4, 3), (3, 2), (2, 7), (7, 6), (4, 7), (5, 6), (4, 5)])
# # G2 = nx.relabel_nodes(G1, mapping={0: "h", 1: "i", 2: "k", 3: "l", 4: "m", 5: "g", 6: "h", 7: "z"})
# # G1.add_edges_from([(0, 1), (1, 2), (3, 0), (0, 2), (2, 3), (4, 3), (4, 2), (5, 2), (5, 7), (5, 6), (8, 7), (7, 9)])
# # G2 = nx.relabel_nodes(G1, mapping={0: "e", 1: "f", 2: "g", 3: "h", 4: "i", 5: "j", 6: "k", 7: "l", 8: "m", 9: "x"})
#
# print(nx.is_isomorphic(G1, G2))
# m = vf2pp_mapping_Di(G1, G2, node_labels=None)
# print(m)
