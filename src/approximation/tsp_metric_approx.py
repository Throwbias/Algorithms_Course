"""
Week 9 - Metric TSP 2-Approximation

Implements:
1. Build complete graph from Euclidean points
2. Compute MST with Prim's algorithm
3. Preorder DFS traversal of MST
4. Shortcut repeated vertices implicitly by visiting preorder once
5. Return to start

Guarantee:
For metric TSP, cost <= 2 * OPT
"""

import math
from itertools import permutations
from collections import defaultdict


def euclidean_distance(p1, p2):
    return math.dist(p1, p2)


def build_complete_graph(points):
    """Build complete weighted graph from 2D points."""
    n = len(points)
    graph = defaultdict(dict)
    for i in range(n):
        for j in range(i + 1, n):
            d = euclidean_distance(points[i], points[j])
            graph[i][j] = d
            graph[j][i] = d
    return graph


def prim_mst(graph):
    """Compute MST using Prim's algorithm."""
    vertices = list(graph.keys())
    if not vertices:
        return {}

    start = vertices[0]
    visited = {start}
    mst = defaultdict(list)

    while len(visited) < len(vertices):
        best_edge = None
        best_weight = float("inf")

        for u in visited:
            for v, w in graph[u].items():
                if v not in visited and w < best_weight:
                    best_edge = (u, v)
                    best_weight = w

        if best_edge is None:
            break

        u, v = best_edge
        mst[u].append(v)
        mst[v].append(u)
        visited.add(v)

    return mst


def preorder_traversal(tree, start=0):
    """Return preorder DFS traversal of tree."""
    visited = set()
    order = []

    def dfs(u):
        visited.add(u)
        order.append(u)
        for v in sorted(tree[u]):
            if v not in visited:
                dfs(v)

    dfs(start)
    return order


def tsp_tour_cost(tour, graph):
    """Compute total cost of a cyclic tour."""
    total = 0
    for i in range(len(tour) - 1):
        total += graph[tour[i]][tour[i + 1]]
    return total


def tsp_metric_approx(points):
    """
    2-approximation for metric TSP using MST preorder walk.

    Args:
        points: list of (x, y) tuples

    Returns:
        dict with tour and cost
    """
    if len(points) < 2:
        return {"tour": [0], "cost": 0.0}

    graph = build_complete_graph(points)
    mst = prim_mst(graph)
    preorder = preorder_traversal(mst, start=0)
    tour = preorder + [preorder[0]]
    cost = tsp_tour_cost(tour, graph)

    return {"tour": tour, "cost": cost}


def exact_tsp(points):
    """
    Brute-force exact TSP solver for small point sets.

    Args:
        points: list of (x, y) tuples

    Returns:
        dict with optimal tour and cost
    """
    n = len(points)
    if n < 2:
        return {"tour": [0], "cost": 0.0}

    graph = build_complete_graph(points)
    best_tour = None
    best_cost = float("inf")

    for perm in permutations(range(1, n)):
        tour = [0] + list(perm) + [0]
        cost = tsp_tour_cost(tour, graph)
        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    return {"tour": best_tour, "cost": best_cost}