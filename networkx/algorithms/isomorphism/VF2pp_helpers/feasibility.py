import networkx as nx


def feasibility(node1, node2, graph_params, state_params):
    """Given a candidate pair of nodes u and v from G1 and G2 respectively, checks if it's feasible to extend the
    mapping, i.e. if u and v can be matched.

    Notes
    -----
    This function performs all the necessary checking by applying both consistency and cutting rules.

    Parameters
    ----------
    node1, node2: Graph node
        The candidate pair of nodes being checked for matching

    graph_params: namedtuple
        Contains all the Graph-related parameters:

        G1,G2: NetworkX Graph or MultiGraph instances.
            The two graphs to check for isomorphism or monomorphism

        G1_labels,G2_labels: dict
            The label of every node in G1 and G2 respectively

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

    Returns
    -------
    True if all checks are successful, False otherwise.
    """
    G1, G2 = graph_params.G1, graph_params.G2
    if G1.number_of_edges(node1, node1) != G2.number_of_edges(node2, node2):
        return False

    if cut_PT(node1, node2, graph_params, state_params):
        return False

    if isinstance(G1, nx.MultiGraph):
        if not consistent_PT(node1, node2, graph_params, state_params):
            return False

    return True


def cut_PT(u, v, graph_params, state_params):
    """Implements the cutting rules for the ISO problem.

    Parameters
    ----------
    u, v: Graph node
        The two candidate nodes being examined.

    graph_params: namedtuple
        Contains all the Graph-related parameters:

        G1,G2: NetworkX Graph or MultiGraph instances.
            The two graphs to check for isomorphism or monomorphism

        G1_labels,G2_labels: dict
            The label of every node in G1 and G2 respectively

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

    Returns
    -------
    True if we should prune this branch, i.e. the node pair failed the cutting checks. False otherwise.
    """
    G1, G2, G1_labels, G2_labels = graph_params
    _, _, T1, T1_out, T2, T2_out = state_params

    u_neighbors_labels = {n1: G1_labels[n1] for n1 in G1[u]}
    u_labels_neighbors = nx.utils.groups(u_neighbors_labels)

    v_neighbors_labels = {n2: G2_labels[n2] for n2 in G2[v]}
    v_labels_neighbors = nx.utils.groups(v_neighbors_labels)

    # if the neighbors of u, do not have the same labels as those of v, NOT feasible.
    if set(u_labels_neighbors.keys()) != set(v_labels_neighbors.keys()):
        return True

    for label, G1_nbh in u_labels_neighbors.items():
        G2_nbh = v_labels_neighbors[label]

        if isinstance(G1, nx.MultiGraph):
            # Check for every neighbor in the neighborhood, if u-nbr1 has same edges as v-nbr2
            u_nbrs_edges = sorted(
                (n for n in G1_nbh), key=lambda x: G1.number_of_edges(u, x)
            )
            v_nbrs_edges = sorted(
                (n for n in G2_nbh), key=lambda x: G2.number_of_edges(v, x)
            )
            for u_nbr, v_nbr in zip(u_nbrs_edges, v_nbrs_edges):
                if G1.number_of_edges(u, u_nbr) != G2.number_of_edges(v, v_nbr):
                    return True

        if len(T1.intersection(G1_nbh)) != len(T2.intersection(G2_nbh)) or len(
            T1_out.intersection(G1_nbh)
        ) != len(T2_out.intersection(G2_nbh)):
            return True

    return False


def consistent_PT(u, v, graph_params, state_params):
    """Checks the consistency of extending the mapping using the current node pair.

    Parameters
    ----------
    u, v: Graph node
        The two candidate nodes being examined.

    graph_params: namedtuple
        Contains all the Graph-related parameters:

        G1,G2: NetworkX Graph or MultiGraph instances.
            The two graphs to check for isomorphism or monomorphism

        G1_labels,G2_labels: dict
            The label of every node in G1 and G2 respectively

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

    Returns
    -------
    True if the pair passes all the consistency checks successfully. False otherwise.
    """
    G1, G2 = graph_params.G1, graph_params.G2
    mapping, reverse_mapping = state_params.mapping, state_params.reverse_mapping

    for neighbor in G1[u]:
        if neighbor in mapping:
            if G1.number_of_edges(u, neighbor) != G2.number_of_edges(
                v, mapping[neighbor]
            ):
                return False

    for neighbor in G2[v]:
        if neighbor in reverse_mapping:
            if G1.number_of_edges(u, reverse_mapping[neighbor]) != G2.number_of_edges(
                v, neighbor
            ):
                return False
    return True
