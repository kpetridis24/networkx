"""
***************
VF2++ Algorithm
***************

An implementation of the VF2++ algorithm for Graph Isomorphism testing.

The simplest interface to use this module is to call:
`vf2pp_is_isomorphic`: to check whether two graphs are isomorphic.
`vf2pp_mapping`: to obtain the node mapping between two graphs, in case they are isomorphic.
`vf2pp_all_mappings`: to generate all possible mappings between two graphs, if isomorphic.

"""
import collections

import networkx as nx
from networkx.algorithms.isomorphism.vf2pp_helpers.candidates import _find_candidates
from networkx.algorithms.isomorphism.vf2pp_helpers.feasibility import _feasibility
from networkx.algorithms.isomorphism.vf2pp_helpers.node_ordering import _matching_order
from networkx.algorithms.isomorphism.vf2pp_helpers.state import (
    _restore_state,
    _update_state,
)

__all__ = [
    "vf2pp_mapping",
    "vf2pp_is_isomorphic",
    "vf2pp_subgraph_is_isomorphic",
    "vf2pp_induced_subgraph_is_isomorphic",
]


def vf2pp_mapping(G1, G2, node_labels=None, default_label=None, PT="iso"):
    """Return an isomorphic mapping between `G1` and `G2` if it exists.

    Parameters
    ----------
    G1,G2: NetworkX Graph or MultiGraph instances.
        The two graphs to check for isomorphism or monomorphism.

    node_labels: Label name
        The label name of all nodes

    default_label: Label name
        Let the user pick a default label value

    Returns
    -------
    Node mapping, if the two graphs are isomorphic. None otherwise.
    """
    try:
        mapping = next(vf2pp_all_mappings(G1, G2, node_labels, default_label, PT))
        return mapping
    except StopIteration:
        return None


def vf2pp_is_isomorphic(G1, G2, node_labels=None, default_label=None):
    """Examines whether G1 and G2 are isomorphic.

    Parameters
    ----------
    G1,G2: NetworkX Graph or MultiGraph instances.
        The two graphs to check for isomorphism or monomorphism.

    node_labels: Label name
        The label name of all nodes

    default_label: Label name
        Let the user pick a default label value

    Returns
    -------
    True if the two graphs are isomorphic. False otherwise.
    """
    return True and not (
        not vf2pp_mapping(G1, G2, node_labels, default_label, PT="iso")
    )


def vf2pp_subgraph_is_isomorphic(G1, G2, node_labels=None, default_label=None):
    """Checks if there exists a Subgraph in G1, that is isomorphic to G2.

    Parameters
    ----------
    G1,G2: NetworkX Graph or MultiGraph instances.
        The two graphs to check for isomorphism or monomorphism.

    node_labels: Label name
        The label name of all nodes

    default_label: Label name
        Let the user pick a default label value

    Returns
    -------
    True if the two graphs are isomorphic. False otherwise.
    """
    return True and not (
        not vf2pp_mapping(G1, G2, node_labels, default_label, PT="sub")
    )


def vf2pp_induced_subgraph_is_isomorphic(G1, G2, node_labels=None, default_label=None):
    """Checks if there exists a Subgraph in G1, that is isomorphic to G2.

    Parameters
    ----------
    G1,G2: NetworkX Graph or MultiGraph instances.
        The two graphs to check for isomorphism or monomorphism.

    node_labels: Label name
        The label name of all nodes

    default_label: Label name
        Let the user pick a default label value

    Returns
    -------
    True if the two graphs are isomorphic. False otherwise.
    """
    return True and not (
        not vf2pp_mapping(G1, G2, node_labels, default_label, PT="ind")
    )


def vf2pp_all_mappings(G1, G2, node_labels=None, default_label=None, PT="iso"):
    """Yields all the possible mappings between G1 and G2.

    Parameters
    ----------
    G1,G2: NetworkX Graph or MultiGraph instances.
        The two graphs to check for isomorphism.

    node_labels: string or None
        The node attribute name within G that indicates node labels.
        If None, then no node labels are used to compute isomorphisms.

    default_label: string
        The default label for nodes that have no label attribute value.
    """
    G1_labels, G2_labels = {}, {}
    if not G1 and not G2:
        return False
    if not _precheck(G1, G2, G1_labels, G2_labels, node_labels, default_label, PT):
        return False

    graph_params, state_params, node_order, stack = _initialize_VF2pp(
        G1, G2, G1_labels, G2_labels, PT
    )
    matching_node = 1
    mapping = state_params.mapping

    while stack:
        current_node, candidate_nodes = stack[-1]

        try:
            candidate = next(candidate_nodes)
        except StopIteration:
            stack.pop()
            matching_node -= 1
            if stack:
                _restore_state(stack, graph_params, state_params)
            continue

        if _feasibility(current_node, candidate, graph_params, state_params, PT):
            if len(mapping) == G2.number_of_nodes() - 1:
                mapping.update({current_node: candidate})
                yield mapping
                mapping.pop(current_node)
                continue

            _update_state(
                current_node,
                candidate,
                matching_node,
                node_order,
                stack,
                graph_params,
                state_params,
                PT,
            )
            matching_node += 1


def _precheck(
    G1, G2, G1_labels, G2_labels, node_labels=None, default_label=-1, PT="iso"
):
    """Checks if all the pre-requisites are satisfied before calling the isomorphism solver.

    Notes
    -----
    Before trying to create the mapping between the nodes of the two graphs, we must check if:
    1. The two graphs have equal number of nodes
    2. The degree sequences in the two graphs are identical
    3. The two graphs have the same label distribution. For example, if G1 has orange nodes but G2 doesn't, there's no
    point in proceeding to create a mapping.

    Parameters
    ----------
    G1,G2: NetworkX Graph or MultiGraph instances.
        The two graphs to check for isomorphism or monomorphism.

    G1_labels,G2_labels: dict
        The label of every node in G1 and G2 respectively.

        node_labels: Label name
        The label name of all nodes

    default_label: Label name
        Let the user pick a default label value
    """
    if PT == "iso":
        if G1.order() != G2.order():
            return False
        if sorted(d for n, d in G1.degree()) != sorted(d for n, d in G2.degree()):
            return False
    else:
        if G1.order() < G2.order() or not G2:
            return False

    G1_labels.update(G1.nodes(data=node_labels, default=default_label))
    G2_labels.update(G2.nodes(data=node_labels, default=default_label))

    G1_nodes_per_label = {
        label: len(nodes) for label, nodes in nx.utils.groups(G1_labels).items()
    }

    if PT == "iso":
        if any(
            label not in G1_nodes_per_label or G1_nodes_per_label[label] != len(nodes)
            for label, nodes in nx.utils.groups(G2_labels).items()
        ):
            return False
    else:
        if any(
            label not in G1_nodes_per_label
            for label, nodes in nx.utils.groups(G2_labels).items()
        ):
            return False

    return True


def _initialize_VF2pp(G1, G2, G1_labels, G2_labels, PT):
    """Initializes all the necessary parameters for VF2++

    Parameters
    ----------
    G1,G2: NetworkX Graph or MultiGraph instances.
        The two graphs to check for isomorphism or monomorphism

    G1_labels,G2_labels: dict
        The label of every node in G1 and G2 respectively

    Returns
    -------
    graph_params: namedtuple
        Contains all the Graph-related parameters:

        G1,G2
        G1_labels,G2_labels: dict

    state_params: namedtuple
        Contains all the State-related parameters:

        mapping: dict
            The mapping as extended so far. Maps nodes of G1 to nodes of G2

        reverse_mapping: dict
            The reverse mapping as extended so far. Maps nodes from G2 to nodes of G1. It's basically "mapping" reversed

        T1, T2: set
            Ti contains uncovered neighbors of covered nodes from Gi, i.e. nodes that are not in the mapping, but are
            neighbors of nodes that are.

        T1_out, T2_out: set
            Ti_out contains all the nodes from Gi, that are neither in the mapping nor in Ti
    """
    GraphParameters = collections.namedtuple(
        "GraphParameters",
        [
            "G1",
            "G2",
            "G1_labels",
            "G2_labels",
            "nodes_of_G1Labels",
            "nodes_of_G2Labels",
            "G2_nodes_of_degree",
        ],
    )
    StateParameters = collections.namedtuple(
        "StateParameters",
        ["mapping", "reverse_mapping", "T1", "T1_out", "T2", "T2_out"],
    )

    graph_params = GraphParameters(
        G1,
        G2,
        G1_labels,
        G2_labels,
        nx.utils.groups(G1_labels),
        nx.utils.groups(G2_labels),
        nx.utils.groups({node: degree for node, degree in G2.degree()}),
    )

    state_params = StateParameters(
        dict(), dict(), set(), set(G1.nodes()), set(), set(G2.nodes())
    )

    node_order = _matching_order(graph_params)

    starting_node = node_order[0]
    candidates = _find_candidates(starting_node, graph_params, state_params, PT)
    stack = [(starting_node, iter(candidates))]

    return graph_params, state_params, node_order, stack
