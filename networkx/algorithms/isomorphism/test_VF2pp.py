import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.algorithms.isomorphism.VF2pp.feasibility import check_feasibility
from networkx.algorithms.isomorphism.VF2pp.state import State
from networkx.algorithms.isomorphism.VF2pp.candidates import find_candidates


def main():
    G = nx.gnp_random_graph(50, 0.5, seed=19)
    colors = ["blue", "red", "green", "orange", "grey", "yellow", "purple", "black", "white"]

    for i in range(len(G.nodes)):
        G.nodes[i]["label"] = colors[random.randrange(len(colors))]

    G1_labels = {n: G.nodes[n]["label"] for n in G.nodes()}
    G2_labels = G1_labels

    # pos = graphviz_layout(G, prog='dot')
    # nx.draw(G, pos, with_labels=True, arrows=False)
    # plt.show()

    m = {node: node for node in G.nodes() if node < G.number_of_nodes() // 4}
    s = State(G1=G, G2=G, u=0, node_order=None, mapping=m, reverse_mapping=m)

    # cnt = 0
    # feasible = -1
    # for n in G.nodes():
    #     if check_feasibility(node1=0, node2=n, G1=G, G2=G, G1_labels=G1_labels, G2_labels=G2_labels, state=s):
    #         feasible = n
    #         cnt += 1
    #
    # print("Number of feasible nodes: ", cnt)
    # print("feasible node: ", feasible)

    print(find_candidates(G, G, G1_labels, G2_labels, 49, s))


main()
