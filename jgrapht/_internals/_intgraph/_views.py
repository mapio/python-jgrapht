from ... import backend
from ...types import GraphEvent, ListenableGraph
from ._int_graphs import _JGraphTIntegerGraph
from ._long_graphs import _JGraphTLongGraph
from .._callbacks import _create_wrapped_callback

import ctypes
import copy


class _UnweightedIntegerGraphView(_JGraphTIntegerGraph):
    def __init__(self, graph):
        res = backend.jgrapht_xx_graph_as_unweighted(graph.handle)

        super().__init__(res)

        self._type = graph.type.as_unweighted()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type

    def __repr__(self):
        return "_UnweightedIntegerGraphView(%r)" % self._handle


class _UnweightedLongGraphView(_JGraphTLongGraph):
    def __init__(self, graph):
        res = backend.jgrapht_xx_graph_as_unweighted(graph.handle)

        super().__init__(res)

        self._type = graph.type.as_unweighted()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type

    def __repr__(self):
        return "_UnweightedLongGraphView(%r)" % self._handle


class _UndirectedIntegerGraphView(_JGraphTIntegerGraph):
    def __init__(self, graph):
        res = backend.jgrapht_xx_graph_as_undirected(graph.handle)

        super().__init__(res)

        self._type = graph.type.as_undirected()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type

    def __repr__(self):
        return "_UndirectedIntegerGraphView(%r)" % self._handle


class _UndirectedLongGraphView(_JGraphTLongGraph):
    def __init__(self, graph):
        res = backend.jgrapht_xx_graph_as_undirected(graph.handle)

        super().__init__(res)

        self._type = graph.type.as_undirected()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type

    def __repr__(self):
        return "_UndirectedLongGraphView(%r)" % self._handle


class _UnmodifiableIntegerGraphView(_JGraphTIntegerGraph):
    def __init__(self, graph):
        res = backend.jgrapht_xx_graph_as_unmodifiable(graph.handle)

        super().__init__(res)

        self._type = graph.type.as_unmodifiable()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type

    def __repr__(self):
        return "_UnmodifiableIntegerGraphView(%r)" % self._handle


class _UnmodifiableLongGraphView(_JGraphTLongGraph):
    def __init__(self, graph):
        res = backend.jgrapht_xx_graph_as_unmodifiable(graph.handle)

        super().__init__(res)

        self._type = graph.type.as_unmodifiable()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type

    def __repr__(self):
        return "_UnmodifiableLongGraphView(%r)" % self._handle


class _EdgeReversedIntegerGraphView(_JGraphTIntegerGraph):
    def __init__(self, graph):
        res = backend.jgrapht_xx_graph_as_edgereversed(graph.handle)

        super().__init__(res)

        self._type = copy.copy(graph.type)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type

    def __repr__(self):
        return "_EdgeReversedIntegerGraphView(%r)" % self._handle


class _EdgeReversedLongGraphView(_JGraphTLongGraph):
    def __init__(self, graph):
        res = backend.jgrapht_xx_graph_as_edgereversed(graph.handle)

        super().__init__(res)

        self._type = copy.copy(graph.type)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type

    def __repr__(self):
        return "_EdgeReversedLongGraphView(%r)" % self._handle


class _MaskedIntegerSubgraphView(_JGraphTIntegerGraph):
    def __init__(self, graph, vertex_mask_cb, edge_mask_cb):

        # Create callbacks and keep a reference
        self._vertex_mask_cb_fptr, self._vertex_mask_cb = _create_wrapped_callback(
            vertex_mask_cb, ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
        )
        self._edge_mask_cb_fptr, self._edge_mask_cb = _create_wrapped_callback(
            edge_mask_cb, ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
        )
        res = backend.jgrapht_ii_graph_as_masked_subgraph(
            graph.handle, self._vertex_mask_cb_fptr, self._edge_mask_cb_fptr
        )

        super().__init__(res)

        self._type = graph.type.as_unmodifiable()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type

    def __repr__(self):
        return "_MaskedIntegerSubgraphView(%r)" % self._handle


class _MaskedLongSubgraphView(_JGraphTLongGraph):
    def __init__(self, graph, vertex_mask_cb, edge_mask_cb):

        # Create callbacks and keep a reference
        self._vertex_mask_cb_fptr, self._vertex_mask_cb = _create_wrapped_callback(
            vertex_mask_cb, ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_longlong)
        )
        self._edge_mask_cb_fptr, self._edge_mask_cb = _create_wrapped_callback(
            edge_mask_cb, ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_longlong)
        )
        res = backend.jgrapht_ll_graph_as_masked_subgraph(
            graph.handle, self._vertex_mask_cb_fptr, self._edge_mask_cb_fptr
        )

        super().__init__(res)

        self._type = graph.type.as_unmodifiable()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type

    def __repr__(self):
        return "_MaskedLongSubgraphView(%r)" % self._handle


class _IntegerWeightedView(_JGraphTIntegerGraph):
    def __init__(self, graph, edge_weight_cb, cache_weights, write_weights_through):

        # Create callbacks and keep a reference
        self._edge_weight_cb_fptr, self._edge_weight_cb = _create_wrapped_callback(
            edge_weight_cb, ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_int)
        )
        res = backend.jgrapht_ii_graph_as_weighted(
            graph.handle,
            self._edge_weight_cb_fptr,
            cache_weights,
            write_weights_through,
        )

        super().__init__(res)

        self._type = graph.type.as_weighted()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type

    def __repr__(self):
        return "_IntegerWeightedView(%r)" % self._handle


class _LongWeightedView(_JGraphTLongGraph):
    def __init__(self, graph, edge_weight_cb, cache_weights, write_weights_through):

        # Create callbacks and keep a reference
        self._edge_weight_cb_fptr, self._edge_weight_cb = _create_wrapped_callback(
            edge_weight_cb, ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_longlong)
        )
        res = backend.jgrapht_ll_graph_as_weighted(
            graph.handle,
            self._edge_weight_cb_fptr,
            cache_weights,
            write_weights_through,
        )

        super().__init__(res)

        self._type = graph.type.as_weighted()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type

    def __repr__(self):
        return "_LongWeightedView(%r)" % self._handle


class _IntegerGraphUnion(_JGraphTIntegerGraph):
    def __init__(self, graph1, graph2, edge_weight_combiner_cb=None):

        # Create callbacks and keep a reference
        (
            self._edge_weight_combiner_cb_fptr,
            self._edge_weight_combiner_cb,
        ) = _create_wrapped_callback(
            edge_weight_combiner_cb,
            ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_double),
        )

        # create graph union at the backend
        res = backend.jgrapht_ii_graph_as_graph_union(
            graph1.handle, graph2.handle, self._edge_weight_combiner_cb_fptr
        )

        super().__init__(res)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph1 = graph1
        self._graph2 = graph2


class _LongGraphUnion(_JGraphTLongGraph):
    def __init__(self, graph1, graph2, edge_weight_combiner_cb=None):

        # Create callbacks and keep a reference
        (
            self._edge_weight_combiner_cb_fptr,
            self._edge_weight_combiner_cb,
        ) = _create_wrapped_callback(
            edge_weight_combiner_cb,
            ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_double),
        )

        # create graph union at the backend
        res = backend.jgrapht_ll_graph_as_graph_union(
            graph1.handle, graph2.handle, self._edge_weight_combiner_cb_fptr
        )

        super().__init__(res)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph1 = graph1
        self._graph2 = graph2


class _IntegerListenableView(_JGraphTIntegerGraph, ListenableGraph):
    def __init__(self, graph):
        res = backend.jgrapht_xx_listenable_as_listenable(graph.handle)
        super().__init__(res)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # list of user-added listeners
        self._listeners = {}
        self._next_id = 0

    def add_listener(self, listener_cb):
        def actual_cb(element, event_type):
            # convert integer event type to enum
            listener_cb(element, GraphEvent(event_type))

        cb_fptr, cb = _create_wrapped_callback(
            actual_cb, ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int)
        )

        listener_handle = backend.jgrapht_ii_listenable_create_graph_listener(cb_fptr)
        backend.jgrapht_ii_listenable_add_graph_listener(self.handle, listener_handle)

        # create listener identifier
        listener_id = self._next_id
        self._next_id += 1

        # register and make sure to keep the actual callback around to
        # avoid garbage collection
        self._listeners[listener_id] = (listener_handle, cb)

        return listener_id

    def remove_listener(self, listener_id):
        listener_handle, cb = self._listeners.pop(listener_id)

        backend.jgrapht_ii_listenable_remove_graph_listener(self.handle, listener_handle)
        backend.jgrapht_handles_destroy(listener_handle)

    def __repr__(self):
        return "_IntegerListenableView(%r)" % self._handle


class _LongListenableView(_JGraphTLongGraph, ListenableGraph):
    def __init__(self, graph):
        res = backend.jgrapht_xx_listenable_as_listenable(graph.handle)
        super().__init__(res)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # list of user-added listeners
        self._listeners = {}
        self._next_id = 0

    def add_listener(self, listener_cb):
        def actual_cb(element, event_type):
            # convert integer event type to enum
            listener_cb(element, GraphEvent(event_type))

        cb_fptr, cb = _create_wrapped_callback(
            actual_cb, ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_int)
        )

        listener_handle = backend.jgrapht_ll_listenable_create_graph_listener(cb_fptr)
        backend.jgrapht_ll_listenable_add_graph_listener(self.handle, listener_handle)

        # create listener identifier
        listener_id = self._next_id
        self._next_id += 1

        # register and make sure to keep the actual callback around to
        # avoid garbage collection
        self._listeners[listener_id] = (listener_handle, cb)

        return listener_id

    def remove_listener(self, listener_id):
        listener_handle, cb = self._listeners.pop(listener_id)

        backend.jgrapht_ll_listenable_remove_graph_listener(self.handle, listener_handle)
        backend.jgrapht_handles_destroy(listener_handle)

    def __repr__(self):
        return "_LongListenableView(%r)" % self._handle
