"""
Push-Relabel max-flow algorithm (FIFO variant).

Implements:
- preflow initialization from source
- height labels
- excess flow tracking
- push, relabel, discharge
- FIFO queue of active vertices

Returns:
- max_flow
- flow_matrix
- relabel_count
- push_count
- discharge_count
- heights
"""

from collections import deque
from typing import Dict, Any, List

from src.flow.network import FlowNetwork


def push_relabel(network: FlowNetwork, source: int, sink: int) -> Dict[str, Any]:
    """
    Compute max flow using FIFO Push-Relabel.

    Args:
        network: FlowNetwork instance
        source: source vertex
        sink: sink vertex

    Returns:
        dict with:
            max_flow
            flow_matrix
            relabel_count
            push_count
            discharge_count
            heights
    """
    if source == sink:
        raise ValueError("source and sink must be different")

    network._validate_vertex(source)
    network._validate_vertex(sink)

    n = network.num_vertices
    height = [0] * n
    excess = [0] * n
    active = [False] * n
    queue = deque()

    push_count = 0
    relabel_count = 0
    discharge_count = 0

    def enqueue(v: int) -> None:
        if v != source and v != sink and not active[v] and excess[v] > 0:
            active[v] = True
            queue.append(v)

    def push(u: int, edge_index: int) -> bool:
        nonlocal push_count

        edge = network.graph[u][edge_index]
        if edge.capacity <= 0:
            return False

        if height[u] != height[edge.to] + 1:
            return False

        send = min(excess[u], edge.capacity)
        if send <= 0:
            return False

        network.add_flow(u, edge_index, send)
        excess[u] -= send
        excess[edge.to] += send
        push_count += 1

        enqueue(edge.to)
        return True

    def relabel(u: int) -> None:
        nonlocal relabel_count

        min_height = float("inf")
        for edge in network.graph[u]:
            if edge.capacity > 0:
                min_height = min(min_height, height[edge.to])

        if min_height < float("inf"):
            height[u] = min_height + 1
            relabel_count += 1

    def discharge(u: int) -> None:
        nonlocal discharge_count

        discharge_count += 1
        while excess[u] > 0:
            pushed = False
            for edge_index, edge in enumerate(network.graph[u]):
                if push(u, edge_index):
                    pushed = True
                    if excess[u] == 0:
                        break

            if excess[u] > 0 and not pushed:
                relabel(u)

    # Initialize preflow
    height[source] = n

    for edge_index, edge in enumerate(network.graph[source]):
        if edge.capacity > 0:
            flow = edge.capacity
            network.add_flow(source, edge_index, flow)
            excess[edge.to] += flow
            excess[source] -= flow
            enqueue(edge.to)

    # Process active vertices in FIFO order
    while queue:
        u = queue.popleft()
        active[u] = False
        discharge(u)
        if excess[u] > 0:
            enqueue(u)

    max_flow = network.total_flow_from_source(source)

    return {
        "max_flow": max_flow,
        "flow_matrix": network.get_flow_matrix(),
        "relabel_count": relabel_count,
        "push_count": push_count,
        "discharge_count": discharge_count,
        "heights": height,
    }