"""
Week 9 - Vertex Cover 2-Approximation

Implements the classical 2-approximation algorithm for Vertex Cover:
1. Pick any uncovered edge (u, v)
2. Add both u and v to the cover
3. Remove all edges incident to u or v
4. Repeat until no edges remain

Guarantee:
|C| <= 2 * OPT
"""

from itertools import combinations


def normalize_edges(edges):
    """Return a cleaned set of undirected edges with no self-loops."""
    cleaned = set()
    for u, v in edges:
        if u != v:
            cleaned.add(tuple(sorted((u, v))))
    return cleaned


def vertex_cover_2approx(edges):
    """
    Compute a 2-approximation to the minimum vertex cover problem.

    Args:
        edges: iterable of (u, v) tuples representing undirected edges

    Returns:
        set: selected vertices in the cover
    """
    remaining_edges = normalize_edges(edges)
    cover = set()

    while remaining_edges:
        u, v = next(iter(remaining_edges))
        cover.add(u)
        cover.add(v)

        remaining_edges = {
            (a, b)
            for (a, b) in remaining_edges
            if u not in (a, b) and v not in (a, b)
        }

    return cover


def is_vertex_cover(edges, cover):
    """Check whether cover is a valid vertex cover."""
    return all(u in cover or v in cover for u, v in normalize_edges(edges))


def exact_min_vertex_cover(edges):
    """
    Brute-force exact minimum vertex cover for small graphs.

    Args:
        edges: iterable of undirected edges

    Returns:
        set: minimum vertex cover
    """
    edges = list(normalize_edges(edges))
    vertices = sorted(set(v for edge in edges for v in edge))

    for r in range(len(vertices) + 1):
        for subset in combinations(vertices, r):
            subset = set(subset)
            if is_vertex_cover(edges, subset):
                return subset

    return set()