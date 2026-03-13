"""
Week 9 - Randomized Max-Cut Approximation

Algorithm:
- Assign each vertex independently to one of two sets with probability 1/2
- Evaluate cut value
- Repeat for multiple trials and keep the best cut found

Guarantee:
Expected cut value is at least 1/2 of optimal
"""

import random
from itertools import product


def cut_value(edges, left, right, weights=None):
    """Compute cut value for a partition."""
    total = 0
    for i, (u, v) in enumerate(edges):
        if (u in left and v in right) or (u in right and v in left):
            total += 1 if weights is None else weights[i]
    return total


def randomized_maxcut(vertices, edges, trials=100, seed=42, weights=None):
    """
    Randomized approximation for Max-Cut.

    Args:
        vertices: iterable of vertices
        edges: list of (u, v)
        trials: number of independent random trials
        seed: RNG seed
        weights: optional edge weights list

    Returns:
        dict with left, right, cut_value
    """
    rng = random.Random(seed)
    vertices = list(vertices)

    best_left, best_right = set(), set()
    best_cut = -1

    for _ in range(trials):
        left, right = set(), set()

        for v in vertices:
            if rng.random() < 0.5:
                left.add(v)
            else:
                right.add(v)

        value = cut_value(edges, left, right, weights)
        if value > best_cut:
            best_cut = value
            best_left, best_right = left, right

    return {
        "left": best_left,
        "right": best_right,
        "cut_value": best_cut
    }


def exact_maxcut(vertices, edges, weights=None):
    """
    Brute-force exact max-cut for small graphs.

    Args:
        vertices: iterable
        edges: list of (u, v)
        weights: optional edge weights

    Returns:
        dict with left, right, cut_value
    """
    vertices = list(vertices)
    n = len(vertices)

    best_value = -1
    best_left = set()
    best_right = set()

    for assignment in product([0, 1], repeat=n):
        left = {vertices[i] for i in range(n) if assignment[i] == 0}
        right = set(vertices) - left

        value = cut_value(edges, left, right, weights)
        if value > best_value:
            best_value = value
            best_left, best_right = left, right

    return {
        "left": best_left,
        "right": best_right,
        "cut_value": best_value
    }