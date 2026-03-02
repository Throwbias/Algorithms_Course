"""
Floyd–Warshall Algorithm - All-Pairs Shortest Paths
"""

import math

def floyd_warshall(graph):
    """
    Compute all-pairs shortest paths using Floyd–Warshall algorithm.

    Args:
        graph (list of lists): adjacency matrix where graph[i][j] is the weight
                               from i to j, or math.inf if no edge.

    Returns:
        tuple:
            dist: 2D list of shortest distances
            next_node: 2D list for path reconstruction
    """
    n = len(graph)
    dist = [row[:] for row in graph]  # copy of graph
    next_node = [[None if graph[i][j] == math.inf else j for j in range(n)] for i in range(n)]

    # Main algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    return dist, next_node


def reconstruct_path(u, v, next_node):
    """
    Reconstruct the path from u to v using next_node table.

    Args:
        u (int): start vertex
        v (int): end vertex
        next_node (2D list): predecessor/next table from floyd_warshall

    Returns:
        list: sequence of vertices from u to v (inclusive)
    """
    if next_node[u][v] is None:
        return []  # no path

    path = [u]
    while u != v:
        u = next_node[u][v]
        path.append(u)
    return path


# -----------------------------
# Standalone Demo / Test
# -----------------------------
if __name__ == "__main__":
    inf = math.inf
    graph = [
        [0, 3, inf, 7],
        [8, 0, 2, inf],
        [5, inf, 0, 1],
        [2, inf, inf, 0]
    ]

    dist, next_node = floyd_warshall(graph)
    print("Distance Matrix:")
    for row in dist:
        print(row)

    print("\nExample Path: 0 -> 2")
    path = reconstruct_path(0, 2, next_node)
    print(path)