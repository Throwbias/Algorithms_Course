"""
Edmonds-Karp max-flow algorithm.

Uses BFS to find shortest augmenting paths in the residual graph.
Returns:
- max_flow
- flow_matrix
- iterations
- bottlenecks
- augmenting_paths
"""

from collections import deque
from typing import Dict, Any, List, Optional, Tuple

from src.flow.network import FlowNetwork


def _bfs_find_augmenting_path(
    network: FlowNetwork, source: int, sink: int
) -> Tuple[Optional[List[Tuple[int, int]]], int]:
    """
    BFS over residual graph.
    Returns:
        path as list of (u, edge_index)
        bottleneck capacity
    """
    parent = [None] * network.num_vertices
    visited = [False] * network.num_vertices
    visited[source] = True

    queue = deque([source])

    while queue:
        u = queue.popleft()

        for edge_index, edge in enumerate(network.graph[u]):
            if edge.capacity > 0 and not visited[edge.to]:
                visited[edge.to] = True
                parent[edge.to] = (u, edge_index)

                if edge.to == sink:
                    path = []
                    bottleneck = float("inf")
                    current = sink

                    while current != source:
                        prev_u, prev_edge_index = parent[current]
                        prev_edge = network.graph[prev_u][prev_edge_index]
                        bottleneck = min(bottleneck, prev_edge.capacity)
                        path.append((prev_u, prev_edge_index))
                        current = prev_u

                    path.reverse()
                    return path, int(bottleneck)

                queue.append(edge.to)

    return None, 0


def edmonds_karp(network: FlowNetwork, source: int, sink: int) -> Dict[str, Any]:
    """
    Compute max flow using Edmonds-Karp.

    Args:
        network: FlowNetwork instance
        source: source vertex
        sink: sink vertex

    Returns:
        dict with:
            max_flow
            flow_matrix
            iterations
            bottlenecks
            augmenting_paths
            residual_updates
    """
    if source == sink:
        raise ValueError("source and sink must be different")

    network._validate_vertex(source)
    network._validate_vertex(sink)

    max_flow = 0
    iterations = 0
    bottlenecks: List[int] = []
    augmenting_paths: List[List[int]] = []
    residual_updates = 0

    while True:
        path, bottleneck = _bfs_find_augmenting_path(network, source, sink)
        if path is None:
            break

        iterations += 1
        bottlenecks.append(bottleneck)

        vertex_path = [source]
        current = source

        for u, edge_index in path:
            edge = network.graph[u][edge_index]
            if u != current:
                raise RuntimeError("augmenting path reconstruction error")
            vertex_path.append(edge.to)
            network.add_flow(u, edge_index, bottleneck)
            residual_updates += 2
            current = edge.to

        augmenting_paths.append(vertex_path)
        max_flow += bottleneck

    return {
        "max_flow": max_flow,
        "flow_matrix": network.get_flow_matrix(),
        "iterations": iterations,
        "bottlenecks": bottlenecks,
        "augmenting_paths": augmenting_paths,
        "residual_updates": residual_updates,
    }