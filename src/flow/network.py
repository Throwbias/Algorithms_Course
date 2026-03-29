"""
Flow network core data structures.

Design goals:
- adjacency-list representation
- explicit forward/backward residual edges
- add_edge() automatically creates reverse edge
- helpers for residual inspection and validation
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class Edge:
    """
    Residual edge representation.

    Attributes:
        to: destination vertex
        capacity: capacity of this residual edge
        flow: current flow on the ORIGINAL forward edge.
              For reverse residual edges, flow is tracked through the paired edge.
        rev: index of reverse edge in graph[to]
        original_capacity: original capacity assigned when edge was created
        is_reverse: whether this edge is the automatically-created reverse edge
    """
    to: int
    capacity: int
    rev: int
    flow: int = 0
    original_capacity: int = 0
    is_reverse: bool = False

    @property
    def residual_capacity(self) -> int:
        return self.capacity


class FlowNetwork:
    """
    Directed flow network using adjacency lists and explicit residual edges.
    """

    def __init__(self, num_vertices: int):
        if num_vertices <= 0:
            raise ValueError("num_vertices must be positive")
        self.num_vertices = num_vertices
        self.graph: List[List[Edge]] = [[] for _ in range(num_vertices)]

    def add_edge(self, u: int, v: int, capacity: int) -> None:
        """
        Add directed edge u -> v with given capacity.
        Automatically adds reverse residual edge v -> u with capacity 0.
        """
        self._validate_vertex(u)
        self._validate_vertex(v)

        if capacity < 0:
            raise ValueError("capacity must be non-negative")

        forward_rev_index = len(self.graph[v])
        backward_rev_index = len(self.graph[u])

        forward = Edge(
            to=v,
            capacity=capacity,
            rev=forward_rev_index,
            flow=0,
            original_capacity=capacity,
            is_reverse=False,
        )
        backward = Edge(
            to=u,
            capacity=0,
            rev=backward_rev_index,
            flow=0,
            original_capacity=0,
            is_reverse=True,
        )

        self.graph[u].append(forward)
        self.graph[v].append(backward)

    def _validate_vertex(self, vertex: int) -> None:
        if not (0 <= vertex < self.num_vertices):
            raise IndexError(f"vertex {vertex} out of bounds")

    def get_reverse_edge(self, u: int, edge_index: int) -> Edge:
        edge = self.graph[u][edge_index]
        return self.graph[edge.to][edge.rev]

    def add_flow(self, u: int, edge_index: int, amount: int) -> None:
        """
        Push flow through edge graph[u][edge_index] by amount.
        Updates forward residual capacity and reverse residual capacity.
        Also keeps forward-edge flow consistent.
        """
        if amount < 0:
            raise ValueError("flow increment must be non-negative")

        edge = self.graph[u][edge_index]
        rev_edge = self.get_reverse_edge(u, edge_index)

        if amount > edge.capacity:
            raise ValueError("cannot push more than residual capacity")

        edge.capacity -= amount
        rev_edge.capacity += amount

        if not edge.is_reverse:
            edge.flow += amount
        else:
            rev_edge.flow -= amount

    def get_residual_graph(self) -> List[List[Dict[str, Any]]]:
        """
        Return a serializable view of the residual graph.
        """
        residual = []
        for u in range(self.num_vertices):
            row = []
            for edge in self.graph[u]:
                row.append(
                    {
                        "to": edge.to,
                        "residual_capacity": edge.capacity,
                        "flow": edge.flow,
                        "original_capacity": edge.original_capacity,
                        "is_reverse": edge.is_reverse,
                    }
                )
            residual.append(row)
        return residual

    def get_flow_matrix(self) -> List[List[int]]:
        """
        Return matrix flow[u][v] for original forward edges.
        """
        matrix = [[0 for _ in range(self.num_vertices)] for _ in range(self.num_vertices)]

        for u in range(self.num_vertices):
            for edge in self.graph[u]:
                if not edge.is_reverse and edge.original_capacity > 0:
                    matrix[u][edge.to] += edge.flow

        return matrix

    def edges(self):
        """
        Iterate over original directed edges only.
        Yields (u, edge).
        """
        for u in range(self.num_vertices):
            for edge in self.graph[u]:
                if not edge.is_reverse and edge.original_capacity > 0:
                    yield u, edge

    def validate_capacity_constraints(self) -> bool:
        """
        Check 0 <= flow <= original_capacity for all original edges.
        """
        for _, edge in self.edges():
            if edge.flow < 0 or edge.flow > edge.original_capacity:
                return False
        return True

    def validate_flow_conservation(self, source: int, sink: int) -> bool:
        """
        Check flow conservation at all vertices except source and sink.
        """
        self._validate_vertex(source)
        self._validate_vertex(sink)

        inflow = [0] * self.num_vertices
        outflow = [0] * self.num_vertices

        for u, edge in self.edges():
            outflow[u] += edge.flow
            inflow[edge.to] += edge.flow

        for v in range(self.num_vertices):
            if v == source or v == sink:
                continue
            if inflow[v] != outflow[v]:
                return False

        return True

    def total_flow_from_source(self, source: int) -> int:
        """
        Sum outgoing flow from source over original edges.
        """
        self._validate_vertex(source)
        total = 0
        for edge in self.graph[source]:
            if not edge.is_reverse and edge.original_capacity > 0:
                total += edge.flow
        return total

    def summary(self) -> Dict[str, Any]:
        """
        Helpful debug summary.
        """
        return {
            "num_vertices": self.num_vertices,
            "num_residual_edges": sum(len(adj) for adj in self.graph),
            "num_original_edges": sum(
                1 for u in range(self.num_vertices) for e in self.graph[u]
                if not e.is_reverse and e.original_capacity > 0
            ),
        }