from . import jgrapht
from . import status
from . import errors
from . import iterator

class GraphType: 
    """Graph Type"""
    def __init__(self, directed, allowing_self_loops, allowing_multiple_edges, weighted):
        self._directed = directed
        self._allowing_self_loops = allowing_self_loops
        self._allowing_multiple_edges = allowing_multiple_edges
        self._weighed = weighted

    @property
    def directed(self):
        return self._directed

    @property
    def undirected(self):
        return not self._directed    

    @property
    def allowing_self_loops(self):
        return self._allowing_self_loops

    @property
    def allowing_multiple_edges(self):
        return self._allowing_multiple_edges

    @property
    def weighted(self):
        return self._weighted

    def __repr__(self):
        return { 'directed':self._directed, 
                 'allowing_self_loops':self._allowing_self_loops, 
                 'allowing_multiple_edges':self._allowing_multiple_edges, 
                 'weighted': self._weighted }

    def __str__(self):
        return 'GraphType(directed={}, allowing-self-loops={}, allowing-multiple-edges={}, weighted={})' \
            .format(self._directed, self._allowing_self_loops, self._allowing_multiple_edges, self._weighed)


class Graph:
    """The main graph class"""
    def __init__(self, directed=True, allowing_self_loops=True, allowing_multiple_edges=True, weighted=True):
        status, handle = jgrapht.jgrapht_graph_create(directed, allowing_self_loops, allowing_multiple_edges, weighted)
        errors.raise_status()
        self._handle = handle
        self._graph_type = GraphType(directed, allowing_self_loops, allowing_multiple_edges, weighted)

    def __del__(self):
        if jgrapht.jgrapht_is_thread_attached():
            err = jgrapht.jgrapht_destroy(self._handle)
            if err:
                errors.raise_status() 

    @property
    def graph_type(self):
        return self._graph_type;

    @property
    def handle(self):
        return self._handle;

    def add_vertex(self):
        err, v = jgrapht.jgrapht_graph_add_vertex(self._handle)
        if err:
            errors.raise_status()
        return v

    def remove_vertex(self, vertex):
        err = jgrapht.jgrapht_graph_remove_vertex(self._handle, vertex)
        if err:
            errors.raise_status()

    def contains_vertex(self, vertex):
        err, res = jgrapht.jgrapht_graph_contains_vertex(self._handle, vertex)
        if err:
            errors.raise_status()
        return res 

    def vertices_count(self):
        err, res = jgrapht.jgrapht_graph_vertices_count(self._handle)
        if err:
            errors.raise_status()        
        return res 

    def add_edge(self, source, target):
        err, res = jgrapht.jgrapht_graph_add_edge(self._handle, source, target)
        if err:
            errors.raise_status()
        return res 

    def remove_edge(self, edge): 
        err, res = jgrapht.jgrapht_graph_remove_edge(self._handle, edge)
        if err:
            errors.raise_status()

    def contains_edge(self, edge):
        err, res = jgrapht.jgrapht_graph_contains_edge(self._handle, edge)
        if err:
            errors.raise_status()
        return res

    def contains_edge_between(self, source, target): 
        err, res = jgrapht.jgrapht_graph_contains_edge_between(self._handle, source, target)
        if err:
            errors.raise_status()
        return res

    def edges_count(self):
        err, res = jgrapht.jgrapht_graph_edges_count(self._handle)
        if err:
            errors.raise_status()
        return res     

    def degree_of(self, vertex):
        err, res = jgrapht.jgrapht_graph_degree_of(self._handle, vertex)
        if err:
            errors.raise_status()
        return res     

    def indegree_of(self, vertex):
        err, res = jgrapht.jgrapht_graph_indegree_of(self._handle, vertex)
        if err:
            errors.raise_status()
        return res

    def outdegree_of(self, vertex):
        err, res = jgrapht.jgrapht_graph_outdegree_of(self._handle, vertex)
        if err:
            errors.raise_status()
        return res

    def edge_source(self, edge):
        err, res = jgrapht.jgrapht_graph_edge_source(self._handle, edge)
        if err:
            errors.raise_status()
        return res

    def edge_target(self, edge):
        err, res = jgrapht.jgrapht_graph_edge_target(self._handle, edge)
        if err:
            errors.raise_status()
        return res

    def get_edge_weight(self, edge): 
        err, res = jgrapht.jgrapht_graph_get_edge_weight(self._handle, edge)
        if err:
            errors.raise_status()
        return res

    def set_edge_weight(self, edge, weight):
        err = jgrapht.jgrapht_graph_set_edge_weight(self._handle, edge, weight)
        if err:
            errors.raise_status()

    def vertices(self): 
        err, res = jgrapht.jgrapht_graph_create_all_vit(self._handle)
        if err:
            errors.raise_status()
        return iterator.LongValueIterator(res)

    def edges(self): 
        err, res = jgrapht.jgrapht_graph_create_all_eit(self._handle)
        if err:
            errors.raise_status()
        return iterator.LongValueIterator(res)

    def edges_between(self, source, target):
        err, res = jgrapht.jgrapht_graph_create_between_eit(self._handle)
        if err:
            errors.raise_status()
        return iterator.LongValueIterator(res)

    def edges_of(self, vertex):
        err, res = jgrapht.jgrapht_graph_vertex_create_eit(self._handle, vertex)
        if err:
            errors.raise_status()
        return iterator.LongValueIterator(res)

    def inedges_of(self, vertex):
        err, res = jgrapht.jgrapht_graph_vertex_create_in_eit(self._handle, vertex)
        if err:
            errors.raise_status()
        return iterator.LongValueIterator(res)    

    def outedges_of(self, vertex):
        err, res = jgrapht.jgrapht_graph_vertex_create_out_eit(self._handle, vertex)
        if err:
            errors.raise_status()
        return iterator.LongValueIterator(res)
            