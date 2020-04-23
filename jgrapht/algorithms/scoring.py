from .. import jgrapht
from .. import errors
from .. import iterator
from .. import util

def _scoring_alg(name, graph, *args):

    alg_method_name = 'jgrapht_scoring_exec_'
    if args:
        alg_method_name += 'custom_'
    alg_method_name += name

    try:
        alg_method = getattr(jgrapht, alg_method_name)
    except AttributeError:
        raise errors.UnsupportedOperationError("Algorithm not supported.")    

    err, scores_handle = alg_method(graph.handle, *args)
    if err: 
        errors.raise_status()

    return util.JGraphTLongDoubleMap(handle=scores_handle)

def scoring_alpha_centrality(graph, damping_factor=0.01, exogenous_factor=1.0, max_iterations=100, tolerance=0.0001):
    custom = [ damping_factor, exogenous_factor, max_iterations, tolerance ]
    return _scoring_alg('alpha_centrality', graph, *custom)

def scoring_betweenness_centrality(graph, incoming=False, normalize=False):
    custom = [ normalize ]
    return _scoring_alg('betweenness_centrality', graph, *custom)

def scoring_closeness_centrality(graph, incoming=False, normalize=True):
    custom = [ incoming, normalize ]
    return _scoring_alg('closeness_centrality', graph, *custom)

def scoring_harmonic_centrality(graph, incoming=False, normalize=True):
    custom = [ incoming, normalize ]
    return _scoring_alg('harmonic_centrality', graph, *custom)

def scoring_pagerank(graph, damping_factor=0.85, max_iterations=100, tolerance=0.0001):
    custom = [ damping_factor, max_iterations, tolerance ]
    return _scoring_alg('pagerank', graph, *custom)

