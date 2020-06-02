from .. import backend as _backend

from .._internals._collections import _JGraphTIntegerSet

from .._internals._pg import is_property_graph
from .._internals._pg_collections import _PropertyGraphEdgeSet


def _matching_alg(name, graph, *args, no_custom_prefix=False):

    alg_method_name = "jgrapht_matching_exec_"
    if args and not no_custom_prefix:
        alg_method_name += "custom_"
    alg_method_name += name

    try:
        alg_method = getattr(_backend, alg_method_name)
    except AttributeError:
        raise NotImplementedError("Algorithm not supported.")

    weight, m_handle = alg_method(graph.handle, *args)

    if is_property_graph(graph):
        return weight, _PropertyGraphEdgeSet(m_handle, graph)
    else:    
        return weight, _JGraphTIntegerSet(m_handle)


def greedy_max_cardinality(graph, sort=False):
    custom = [sort]
    return _matching_alg("greedy_general_max_card", graph, *custom)


def edmonds_max_cardinality(graph, dense=False):
    if dense:
        return _matching_alg("edmonds_general_max_card_dense", graph)
    else:
        return _matching_alg("edmonds_general_max_card_sparse", graph)


def greedy_max_weight(graph, normalize_edge_costs=False, tolerance=1e-9):
    custom = [normalize_edge_costs, tolerance]
    return _matching_alg("greedy_general_max_weight", graph, *custom)


def pathgrowing_max_weight(graph):
    return _matching_alg("pathgrowing_max_weight", graph)


def blossom5_max_weight(graph, perfect=True):
    if perfect:
        return _matching_alg("blossom5_general_perfect_max_weight", graph)
    else:
        return _matching_alg("blossom5_general_max_weight", graph)


def blossom5_min_weight(graph, perfect=True):
    if perfect:
        return _matching_alg("blossom5_general_perfect_min_weight", graph)
    else:
        return _matching_alg("blossom5_general_min_weight", graph)


def bipartite_max_cardinality(graph):
    return _matching_alg("bipartite_max_card", graph)


def bipartite_max_weight(graph):
    return _matching_alg("bipartite_max_weight", graph)


def bipartite_perfect_min_weight(graph, partition_a, partition_b):
    custom = [partition_a.handle, partition_b.handle]
    return _matching_alg(
        "bipartite_perfect_min_weight", graph, *custom, no_custom_prefix=True
    )
