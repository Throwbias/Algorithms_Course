"""
Bipartite matching via max-flow.

Reduction:
- source -> each left node with capacity 1
- left node -> right node with capacity 1 if edge exists
- each right node -> sink with capacity 1

Then:
max flow value = maximum bipartite matching size
"""

from typing import List, Tuple, Dict, Any

from src.flow.network import FlowNetwork
from src.flow.edmonds_karp import edmonds_karp


def bipartite_matching(
    left_partition: List[str],
    right_partition: List[str],
    edges: List[Tuple[str, str]],
    solver: str = "ek",
) -> Dict[str, Any]:
    """
    Solve bipartite matching using max-flow.

    Args:
        left_partition: list of left-side node labels
        right_partition: list of right-side node labels
        edges: list of (left_node, right_node) edges
        solver: "ek" for Edmonds-Karp, "pr" for Push-Relabel

    Returns:
        dict with:
            matching_size
            matching_pairs
            flow_result
    """
    if len(set(left_partition)) != len(left_partition):
        raise ValueError("left_partition contains duplicate node labels")

    if len(set(right_partition)) != len(right_partition):
        raise ValueError("right_partition contains duplicate node labels")

    left_set = set(left_partition)
    right_set = set(right_partition)

    for u, v in edges:
        if u not in left_set:
            raise ValueError(f"Left node {u} not in left_partition")
        if v not in right_set:
            raise ValueError(f"Right node {v} not in right_partition")

    # Node indexing:
    # 0 = source
    # 1..L = left nodes
    # L+1 .. L+R = right nodes
    # last = sink
    source = 0
    left_offset = 1
    right_offset = 1 + len(left_partition)
    sink = 1 + len(left_partition) + len(right_partition)

    total_nodes = sink + 1
    network = FlowNetwork(total_nodes)

    left_index = {node: left_offset + i for i, node in enumerate(left_partition)}
    right_index = {node: right_offset + i for i, node in enumerate(right_partition)}

    # Source to left partition
    for node in left_partition:
        network.add_edge(source, left_index[node], 1)

    # Left to right partition edges
    for u, v in edges:
        network.add_edge(left_index[u], right_index[v], 1)

    # Right partition to sink
    for node in right_partition:
        network.add_edge(right_index[node], sink, 1)

    if solver == "ek":
        flow_result = edmonds_karp(network, source, sink)
    elif solver == "pr":
        from src.flow.push_relabel import push_relabel
        flow_result = push_relabel(network, source, sink)
    else:
        raise ValueError("solver must be 'ek' or 'pr'")

    matching_pairs = []

    # Recover matching from used left->right edges with flow = 1
    for u_label in left_partition:
        u_idx = left_index[u_label]
        for edge in network.graph[u_idx]:
            if edge.is_reverse:
                continue
            if edge.original_capacity != 1:
                continue
            if edge.to < right_offset or edge.to >= sink:
                continue
            if edge.flow == 1:
                v_label = right_partition[edge.to - right_offset]
                matching_pairs.append((u_label, v_label))

    return {
        "matching_size": len(matching_pairs),
        "matching_pairs": matching_pairs,
        "flow_result": flow_result,
    }