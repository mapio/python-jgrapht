from collections.abc import Set

from .. import backend
from ..types import (
    Graph,
    GraphType,
)

import ctypes
from . import _refcount
from ._wrappers import _HandleWrapper, _JGraphTRefIterator


class _JGraphTRefGraph(_HandleWrapper, Graph):
    """The ref graph implementation."""

    def __init__(
        self,
        handle,
        vertex_supplier_fptr_wrapper,
        edge_supplier_fptr_wrapper,
        hash_lookup_fptr_wrapper,
        equals_lookup_fptr_wrapper,
        **kwargs
    ):
        super().__init__(handle=handle, **kwargs)

        # read attributes from backend
        directed = backend.jgrapht_xx_graph_is_directed(self._handle)
        allowing_self_loops = backend.jgrapht_xx_graph_is_allowing_selfloops(
            self._handle
        )
        allowing_multiple_edges = backend.jgrapht_xx_graph_is_allowing_multipleedges(
            self._handle
        )
        allowing_cycles = backend.jgrapht_xx_graph_is_allowing_cycles(self._handle)
        weighted = backend.jgrapht_xx_graph_is_weighted(self._handle)
        modifiable = backend.jgrapht_xx_graph_is_modifiable(self._handle)

        self._type = GraphType(
            directed=directed,
            allowing_self_loops=allowing_self_loops,
            allowing_multiple_edges=allowing_multiple_edges,
            allowing_cycles=allowing_cycles,
            weighted=weighted,
            modifiable=modifiable,
        )
        self._vertex_set = None
        self._edge_set = None

        # keep ctypes callbacks from being garbage collected
        self._vertex_supplier_fptr_wrapper = vertex_supplier_fptr_wrapper
        self._edge_supplier_fptr_wrapper = edge_supplier_fptr_wrapper
        self._hash_lookup_fptr_wrapper = hash_lookup_fptr_wrapper
        self._equals_lookup_fptr_wrapper = equals_lookup_fptr_wrapper

    @property
    def type(self):
        return self._type

    def add_vertex(self, vertex=None):
        if vertex is not None:
            if backend.jgrapht_rr_graph_add_given_vertex(self._handle, id(vertex)):
                _refcount._inc_ref(vertex)
        else:
            v_ptr = backend.jgrapht_rr_graph_add_vertex(self._handle)
            vertex = _refcount._swig_ptr_to_obj(v_ptr)
            _refcount._inc_ref(vertex)
        return vertex

    def remove_vertex(self, v):
        removed = backend.jgrapht_rr_graph_remove_vertex(self._handle, id(v))
        if removed:
            _refcount._dec_ref(v)

    def contains_vertex(self, v):
        return backend.jgrapht_rr_graph_contains_vertex(self._handle, id(v))

    def add_edge(self, u, v, weight=None, edge=None):
        if edge is not None:
            e_ptr = id(edge)
            if backend.jgrapht_rr_graph_add_given_edge(
                self._handle, id(u), id(v), e_ptr
            ):
                _refcount._inc_ref(edge)
                if weight is not None:
                    backend.jgrapht_rr_graph_set_edge_weight(
                        self._handle, e_ptr, weight
                    )
        else:
            e_ptr = backend.jgrapht_rr_graph_add_edge(self._handle, id(u), id(v))
            edge = _refcount._swig_ptr_to_obj(e_ptr)
            _refcount._inc_ref(edge)
            if weight is not None:
                backend.jgrapht_rr_graph_set_edge_weight(self._handle, e_ptr, weight)
        return edge

    def remove_edge(self, e):
        if e is None:
            raise ValueError("Edge cannot be None")
        if backend.jgrapht_rr_graph_remove_edge(self._handle, id(e)):
            _refcount._dec_ref(e)
            return True
        else:
            return False

    def contains_edge(self, e):
        return backend.jgrapht_rr_graph_contains_edge(self._handle, id(e))

    def contains_edge_between(self, u, v):
        return backend.jgrapht_rr_graph_contains_edge_between(
            self._handle, id(u), id(v)
        )

    def degree_of(self, v):
        return backend.jgrapht_rr_graph_degree_of(self._handle, id(v))

    def indegree_of(self, v):
        return backend.jgrapht_rr_graph_indegree_of(self._handle, id(v))

    def outdegree_of(self, v):
        return backend.jgrapht_rr_graph_outdegree_of(self._handle, id(v))

    def edge_source(self, e):
        v_ptr = backend.jgrapht_rr_graph_edge_source(self._handle, id(e))
        return _refcount._swig_ptr_to_obj(v_ptr)

    def edge_target(self, e):
        v_ptr = backend.jgrapht_rr_graph_edge_target(self._handle, id(e))
        return _refcount._swig_ptr_to_obj(v_ptr)

    def get_edge_weight(self, e):
        return backend.jgrapht_rr_graph_get_edge_weight(self._handle, id(e))

    def set_edge_weight(self, e, weight):
        backend.jgrapht_rr_graph_set_edge_weight(self._handle, id(e), weight)

    @property
    def number_of_vertices(self):
        return backend.jgrapht_xx_graph_vertices_count(self._handle)

    @property
    def vertices(self):
        if self._vertex_set is None:
            self._vertex_set = self._VertexSet(self._handle)
        return self._vertex_set

    @property
    def number_of_edges(self):
        return backend.jgrapht_xx_graph_edges_count(self._handle)

    @property
    def edges(self):
        if self._edge_set is None:
            self._edge_set = self._EdgeSet(self._handle)
        return self._edge_set

    def edges_between(self, u, v):
        it = backend.jgrapht_rr_graph_create_between_eit(self._handle, id(u), id(v))
        return _JGraphTRefIterator(it)

    def edges_of(self, v):
        it = backend.jgrapht_rr_graph_vertex_create_eit(self._handle, id(v))
        return _JGraphTRefIterator(it)

    def inedges_of(self, v):
        it = backend.jgrapht_rr_graph_vertex_create_in_eit(self._handle, id(v))
        return _JGraphTRefIterator(it)

    def outedges_of(self, v):
        it = backend.jgrapht_rr_graph_vertex_create_out_eit(self._handle, id(v))
        return _JGraphTRefIterator(it)

    def __repr__(self):
        return "_JGraphTRefGraph(%r)" % self._handle

    class _VertexSet(Set):
        """Wrapper around the vertices of a JGraphT graph"""

        def __init__(self, handle=None):
            self._handle = handle

        def __iter__(self):
            res = backend.jgrapht_xx_graph_create_all_vit(self._handle)
            return _JGraphTRefIterator(res)

        def __len__(self):
            return backend.jgrapht_xx_graph_vertices_count(self._handle)

        def __contains__(self, v):
            return backend.jgrapht_rr_graph_contains_vertex(self._handle, id(v))

        def __repr__(self):
            return "_JGraphTRefGraph-VertexSet(%r)" % self._handle

        def __str__(self):
            return "{" + ", ".join(str(x) for x in self) + "}"

        @classmethod
        def _from_iterable(cls, it):
            return set(it)

    class _EdgeSet(Set):
        """Wrapper around the edges of a JGraphT graph"""

        def __init__(self, handle=None):
            self._handle = handle

        def __iter__(self):
            res = backend.jgrapht_xx_graph_create_all_eit(self._handle)
            return _JGraphTRefIterator(res)

        def __len__(self):
            return backend.jgrapht_xx_graph_edges_count(self._handle)

        def __contains__(self, e):
            return backend.jgrapht_rr_graph_contains_edge(self._handle, id(e))

        def __repr__(self):
            return "_JGraphTRefGraph-EdgeSet(%r)" % self._handle

        def __str__(self):
            return "{" + ", ".join(str(x) for x in self) + "}"

        @classmethod
        def _from_iterable(cls, it):
            return set(it)

    def __del__(self):
        # Cleanup reference counts
        for e in self.edges:
            _refcount._dec_ref(e)
        for v in self.vertices:
            _refcount._dec_ref(v)
        super().__del__()


def _fallback_vertex_supplier():
    return object()


def _fallback_edge_supplier():
    return object()


def _hash_lookup(o):
    """TODO"""
    return 0


def _equals_lookup(o):
    """TODO"""
    return 0


def _create_ref_graph(
    directed=True,
    allowing_self_loops=False,
    allowing_multiple_edges=False,
    weighted=True,
    vertex_supplier=None,
    edge_supplier=None,
):
    """Create a graph with any reference as vertices/edges.

    :param directed: if True the graph will be directed, otherwise undirected
    :param allowing_self_loops: if True the graph will allow the addition of self-loops
    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :returns: a graph
    :rtype: :class:`~jgrapht.types.Graph`
    """

    if vertex_supplier is None:
        vertex_supplier = _fallback_vertex_supplier
    vertex_supplier_type = ctypes.CFUNCTYPE(ctypes.py_object)
    vertex_supplier_fptr_wrapper = _refcount._CallbackWrapper(
        vertex_supplier, vertex_supplier_type
    )

    if edge_supplier is None:
        edge_supplier = _fallback_edge_supplier
    edge_supplier_type = ctypes.CFUNCTYPE(ctypes.py_object)
    edge_supplier_fptr_wrapper = _refcount._CallbackWrapper(
        edge_supplier, edge_supplier_type
    )

    hash_lookup_fptr_wrapper = _refcount._CallbackWrapper(
        _hash_lookup, ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)
    )

    equals_lookup_fptr_wrapper = _refcount._CallbackWrapper(
        _equals_lookup, ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)
    )

    handle = backend.jgrapht_rr_graph_create(
        directed,
        allowing_self_loops,
        allowing_multiple_edges,
        weighted,
        vertex_supplier_fptr_wrapper.fptr,
        edge_supplier_fptr_wrapper.fptr,
        hash_lookup_fptr_wrapper.fptr,
        equals_lookup_fptr_wrapper.fptr,
    )

    return _JGraphTRefGraph(
        handle,
        vertex_supplier_fptr_wrapper=vertex_supplier_fptr_wrapper,
        edge_supplier_fptr_wrapper=edge_supplier_fptr_wrapper,
        hash_lookup_fptr_wrapper=hash_lookup_fptr_wrapper,
        equals_lookup_fptr_wrapper=equals_lookup_fptr_wrapper,
    )
