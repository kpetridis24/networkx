import os
import struct

import networkx as nx
from networkx.algorithms.isomorphism.vf2pp import vf2pp_induced_subgraph_is_isomorphic


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


class TestGraphINDVF2pp:
    def test_both_graphs_empty(self):
        G = nx.Graph()
        H = nx.Graph()

        m = vf2pp_induced_subgraph_is_isomorphic(G, H)
        assert not m

    def test_first_graph_empty(self):
        G = nx.Graph()
        H = nx.Graph([(0, 1)])
        m = vf2pp_induced_subgraph_is_isomorphic(G, H)
        assert not m

    def test_second_graph_empty(self):
        G = nx.Graph([(0, 1)])
        H = nx.Graph()
        m = vf2pp_induced_subgraph_is_isomorphic(G, H)
        assert not m

    def test_first_graph_smaller(self):
        G = nx.path_graph(10)
        H = nx.path_graph(11)
        m = vf2pp_induced_subgraph_is_isomorphic(G, H)
        assert not m

    def test_wiki_graph(self):
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

        # Nodes 1,2,3,4 form the clockwise corners of a large square.
        # Nodes 5,6,7,8 form the clockwise corners of a small square
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
        m = vf2pp_induced_subgraph_is_isomorphic(g1, g2, node_labels=None)
        assert m

    def test_induced_iso_on_subgraph(self):
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

        g1 = nx.Graph()
        g2 = nx.Graph()
        g1.add_edges_from(g1edges)
        g2.add_edges_from([[1, 2], [2, 3], [3, 4]])
        m = vf2pp_induced_subgraph_is_isomorphic(g1, g2, node_labels=None)
        assert m

    def test_induced_DB_subgraph(self):
        # A is the subgraph
        # B is the full graph
        head, tail = os.path.split(__file__)
        subgraph = create_graph(os.path.join(head, "../si2_b06_m200.A99"))
        graph = create_graph(os.path.join(head, "../si2_b06_m200.B99"))
        assert vf2pp_induced_subgraph_is_isomorphic(graph, subgraph, node_labels=None)

    def test_multi_edge(self):
        # Simple test for multigraphs
        # Need something much more rigorous
        edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 8),
            (8, 9),
            (9, 10),
            (10, 11),
            (10, 11),
            (11, 12),
            (11, 12),
            (12, 13),
            (12, 13),
            (13, 14),
            (13, 14),
            (14, 15),
            (14, 15),
            (15, 16),
            (15, 16),
            (16, 17),
            (16, 17),
            (17, 18),
            (17, 18),
            (18, 19),
            (18, 19),
            (19, 0),
            (19, 0),
        ]
        nodes = list(range(20))
        import random

        g1 = nx.MultiGraph()
        g1.add_edges_from(edges)
        for _ in range(10):
            new_nodes = list(nodes)
            random.shuffle(new_nodes)
            d = dict(zip(nodes, new_nodes))
            g2 = nx.relabel_nodes(g1, d)
            assert vf2pp_induced_subgraph_is_isomorphic(g1, g2, node_labels=None)

    def test_self_loop_induced(self):
        # Simple test for graphs with selfloops
        edges0 = [
            (0, 1),
            (0, 2),
            (1, 2),
            (1, 3),
            (2, 4),
            (3, 1),
            (3, 2),
            (4, 2),
            (4, 5),
            (5, 4),
        ]
        edges = edges0 + [(2, 2)]
        nodes = list(range(6))
        import random

        g1 = nx.Graph()
        g1.add_edges_from(edges)
        for _ in range(100):
            new_nodes = list(nodes)
            random.shuffle(new_nodes)
            d = dict(zip(nodes, new_nodes))
            g2 = nx.relabel_nodes(g1, d)
            g2.remove_edges_from(nx.selfloop_edges(g2))
            assert not vf2pp_induced_subgraph_is_isomorphic(g2, g1, node_labels=None)

    def test_multiple(self):
        edges = [("A", "B"), ("B", "A"), ("B", "C")]
        g1, g2 = nx.Graph(), nx.Graph()
        g1.add_edges_from(edges)
        g2.add_edges_from(edges)
        g3 = nx.subgraph(g2, ["A", "B"])
        g2.remove_node("C")
        assert vf2pp_induced_subgraph_is_isomorphic(g1, g2, node_labels=None)
        assert vf2pp_induced_subgraph_is_isomorphic(g1, g3, node_labels=None)

    def test_non_comparable_nodes(self):
        node1 = object()
        node2 = object()
        node3 = object()

        # Graph
        G = nx.path_graph([node1, node2, node3])
        assert vf2pp_induced_subgraph_is_isomorphic(G, G, node_labels=None)
