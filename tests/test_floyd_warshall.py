import math
import pytest
from src.dp_advanced.floyd_warshall import floyd_warshall, reconstruct_path

inf = math.inf

# -----------------------------
# Test Graphs
# -----------------------------
@pytest.fixture
def small_graph():
    """
    Returns a small adjacency matrix graph
    """
    # Graph: 4 vertices, some weights
    return [
        [0, 3, inf, 7],
        [8, 0, 2, inf],
        [5, inf, 0, 1],
        [2, inf, inf, 0]
    ]

@pytest.fixture
def negative_edge_graph():
    """
    Graph with negative edge weights (no negative cycles)
    """
    return [
        [0, 1, float('inf'), float('inf')],
        [float('inf'), 0, -1, float('inf')],
        [float('inf'), float('inf'), 0, -1],
        [float('inf'), float('inf'), float('inf'), 0]
    ]


# -----------------------------
# Tests
# -----------------------------
def test_distances_small_graph(small_graph):
    dist, _ = floyd_warshall(small_graph)
    expected = [
        [0, 3, 5, 6],
        [5, 0, 2, 3],
        [3, 6, 0, 1],
        [2, 5, 7, 0]
    ]
    for i in range(len(dist)):
        for j in range(len(dist)):
            assert dist[i][j] == expected[i][j]

def test_path_reconstruction_small_graph(small_graph):
    _, next_node = floyd_warshall(small_graph)
    path = reconstruct_path(0, 2, next_node)
    # Expected path: 0 -> 1 -> 2
    assert path == [0, 1, 2]

def test_negative_edges(negative_edge_graph):
    dist, next_node = floyd_warshall(negative_edge_graph)
    # Check some distances
    # 0 -> 1 -> 2 -> 3
    assert dist[0][2] == 0      # 0 -> 1 -> 2
    assert dist[0][3] == -1     # 0 -> 1 -> 2 -> 3
    # Reconstruct path
    path = reconstruct_path(0, 3, next_node)
    assert path == [0, 1, 2, 3]