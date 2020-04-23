from .. import jgrapht
from .. import errors
from .. import iterator
from .. import util

def _coloring_alg(name, graph, *args):
    alg_method_name = 'jgrapht_coloring_exec_'
    alg_method_name += name

    try:
        alg_method = getattr(jgrapht, alg_method_name)
    except AttributeError:
        raise errors.UnsupportedOperationError("Algorithm not supported.")    

    err, num_colors, color_map_handle = alg_method(graph.handle, *args)
    if err: 
        errors.raise_status()

    return (num_colors, util.JGraphTLongLongMap(handle=color_map_handle))


def coloring_greedy(graph):
    return _coloring_alg('greedy', graph)

def coloring_greedy_smallestdegreelast(graph):
    return _coloring_alg('greedy_smallestdegreelast', graph)

def coloring_greedy_largestdegreefirst(graph):
    return _coloring_alg('greedy_largestdegreefirst', graph)

def coloring_greedy_random(graph, seed=None):
    if seed is None: 
        return _coloring_alg('greedy_random', graph)
    else:
        return _coloring_alg('greedy_random_with_seed', graph, seed)

def coloring_greedy_dsatur(graph):
    return _coloring_alg('greedy_dsatur', graph)

def coloring_color_refinement(graph):
    return _coloring_alg('color_refinement', graph)

def coloring_backtracking_brown(graph):
    return _coloring_alg('backtracking_brown', graph)    

