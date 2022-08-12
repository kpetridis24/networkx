import os
import struct

import networkx as nx
from networkx.algorithms.isomorphism.vf2pp import vf2pp_subgraph_is_isomorphic


# https://web.archive.org/web/20090303210205/http://amalfi.dis.unina.it/graph/db/
def create_graph(filename):
    """Creates a Graph instance from the filename."""

    # The file is assumed to be in the format from the VF2 graph database.
    # Each file is composed of 16-bit numbers (unsigned short int).
    # So we will want to read 2 bytes at a time.

    # We can read the number as follows:
    #   number = struct.unpack('<H', file.read(2))
    # This says, expect the data in little-endian encoding
    # as an unsigned short int and unpack 2 bytes from the file.

    fh = open(filename, mode="rb")

    # Grab the number of nodes.
    # Node numeration is 0-based, so the first node has index 0.
    nodes = struct.unpack("<H", fh.read(2))[0]

    graph = nx.Graph()
    for from_node in range(nodes):
        # Get the number of edges.
        edges = struct.unpack("<H", fh.read(2))[0]
        for edge in range(edges):
            # Get the terminal node.
            to_node = struct.unpack("<H", fh.read(2))[0]
            graph.add_edge(from_node, to_node)

    fh.close()
    return graph


def assign_labels(G1, G2, mapped_nodes=None, same=False):
    colors = [
        "white",
        "black",
        "green",
        "purple",
        "orange",
        "red",
        "blue",
        "pink",
        "yellow",
        "none",
        "ocean",
        "brown",
        "solarized",
    ]

    if same:
        for n1 in G1.nodes():
            G1.nodes[n1]["label"] = "blue"
        for n2 in G2.nodes():
            G2.nodes[n2]["label"] = "blue"
        return

    c = 0
    for node1, node2 in mapped_nodes:
        color = colors[c % len(colors)]
        G1.nodes[node1]["label"] = color
        G2.nodes[node2]["label"] = color
        c += 1


class TestGraphSUBVF2pp:
    def test_both_graphs_empty(self):
        G = nx.Graph()
        H = nx.Graph()

        m = vf2pp_subgraph_is_isomorphic(G, H)
        assert not m

    def test_first_graph_empty(self):
        G = nx.Graph()
        H = nx.Graph([(0, 1)])
        m = vf2pp_subgraph_is_isomorphic(G, H)
        assert not m

    def test_second_graph_empty(self):
        G = nx.Graph([(0, 1)])
        H = nx.Graph()
        m = vf2pp_subgraph_is_isomorphic(G, H)
        assert not m

    def test_first_graph_smaller(self):
        G = nx.path_graph(10)
        H = nx.path_graph(11)
        m = vf2pp_subgraph_is_isomorphic(G, H)
        assert not m

    def test_graph_same_labels(self):
        edges1 = [
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

        edges2 = [
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

        G1 = nx.Graph()
        G2 = nx.Graph()
        G1.add_edges_from(edges1)
        G2.add_edges_from(edges2)
        G3 = G2.subgraph([1, 2, 3, 4])

        assign_labels(G1, G3, same=True)
        m = vf2pp_subgraph_is_isomorphic(G1, G3, node_labels="label")
        assert m

    def test_graph_DB_same_labels(self):
        head, tail = os.path.split(__file__)
        subgraph = create_graph(os.path.join(head, "../si2_b06_m200.A99"))
        graph = create_graph(os.path.join(head, "../si2_b06_m200.B99"))

        assign_labels(graph, subgraph, same=True)
        m = vf2pp_subgraph_is_isomorphic(graph, subgraph, node_labels="label")
        assert m

    def test_custom_graph1_same_labels(self):
        G1 = nx.Graph()

        mapped = {1: "A", 2: "B", 3: "C", 4: "D", 5: "Z", 6: "E"}
        edges1 = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 6), (3, 4), (5, 1), (5, 2)]

        G1.add_edges_from(edges1)
        G2 = nx.relabel_nodes(G1, mapped)

        g2 = G2.subgraph([mapped[1], mapped[2], mapped[3]])
        assign_labels(G1, g2, same=True)
        m = vf2pp_subgraph_is_isomorphic(G1, g2, node_labels="label")
        assert m

        g3 = G2.subgraph([mapped[1], mapped[2], mapped[5]])
        assign_labels(G1, g3, same=True)
        m = vf2pp_subgraph_is_isomorphic(G1, g3, node_labels="label")
        assert m

        g4 = G1.subgraph([1, 3, 4])
        assign_labels(G2, g4, same=True)
        m = vf2pp_subgraph_is_isomorphic(G2, g4, node_labels="label")
        assert m

    def test_custom_graph2_same_labels(self):
        G1 = nx.Graph()

        mapped = {1: "A", 2: "C", 3: "D", 4: "E", 5: "G", 7: "B", 6: "F"}
        edges1 = [(1, 2), (1, 5), (5, 6), (2, 3), (2, 4), (3, 4), (4, 5), (2, 7)]

        G1.add_edges_from(edges1)
        G2 = nx.relabel_nodes(G1, mapped)
        assign_labels(G1, G2, same=True)

        g2 = G2.subgraph([mapped[1], mapped[3], mapped[4], mapped[5], mapped[6]])
        assign_labels(G1, g2, same=True)

        m = vf2pp_subgraph_is_isomorphic(G1, g2, node_labels="label")
        assert m

        g3 = G2.subgraph([mapped[1], mapped[6], mapped[2], mapped[3], mapped[4]])
        assign_labels(G1, g3, same=True)
        m = vf2pp_subgraph_is_isomorphic(G1, g3, node_labels="label")
        assert m

        G1.add_edges_from([(4, 6), (2, 5)])
        G1.remove_edge(4, 5)
        g1 = G1.subgraph([2, 4, 5, 6])
        assign_labels(g1, G2, same=True)

        m = vf2pp_subgraph_is_isomorphic(G2, g1, node_labels="label")
        assert m

    def test_custom_graph3_same_labels(self):
        G1 = nx.Graph()
        mapped = {1: 9, 2: 8, 3: 7, 4: 6, 5: 3, 8: 5, 9: 4, 7: 1, 6: 2}
        edges1 = [
            (1, 2),
            (1, 3),
            (2, 3),
            (3, 4),
            (4, 5),
            (4, 7),
            (4, 9),
            (5, 8),
            (8, 9),
            (5, 6),
            (6, 7),
            (5, 2),
        ]
        G1.add_edges_from(edges1)
        G2 = nx.relabel_nodes(G1, mapped)

        G2.add_edges_from(
            [(mapped[6], mapped[9]), (mapped[7], mapped[8]), (mapped[7], mapped[9])]
        )
        G1.add_edges_from([(6, 8), (6, 9)])

        g2 = G2.subgraph([mapped[4], mapped[7], mapped[8], mapped[9]])
        assign_labels(G1, g2, same=True)
        m = vf2pp_subgraph_is_isomorphic(G1, g2, node_labels="label")
        assert m

        g1 = G1.subgraph([6, 8, 9])
        assign_labels(g1, g2, same=True)
        m = vf2pp_subgraph_is_isomorphic(g2, g1, node_labels="label")
        assert m

        g1 = G1.subgraph([6, 8, 4, 5, 2, 3, 1])
        assign_labels(g1, G2, same=True)
        m = vf2pp_subgraph_is_isomorphic(g1, G2, node_labels="label")
        assert not m

        m = vf2pp_subgraph_is_isomorphic(G2, g1, node_labels="label")
        assert m

        g1 = G1.subgraph([4, 5, 8, 9])
        assign_labels(g1, G2, same=True)
        m = vf2pp_subgraph_is_isomorphic(G2, g1, node_labels="label")
        assert m

        G1.add_edges_from([(1, 5), (1, 4), (2, 4), (3, 5)])
        g1 = G1.subgraph([1, 2, 3, 4, 5])
        g2 = G1.subgraph([1, 2, 5])

        assign_labels(g1, g2, same=True)
        m = vf2pp_subgraph_is_isomorphic(g1, g2, node_labels="label")
        assert m

        g2 = G1.subgraph([3, 2, 4])
        assign_labels(g1, g2, same=True)
        m = vf2pp_subgraph_is_isomorphic(g1, g2, node_labels="label")
        assert m
