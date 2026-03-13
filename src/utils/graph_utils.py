"""
Utility functions for generating graphs and metric point sets.
"""

import random
import math


def generate_random_graph(num_vertices, edge_probability=0.3, seed=42):
    """
    Generate an undirected random graph.

    Returns:
        vertices, edges
    """
    rng = random.Random(seed)
    vertices = list(range(num_vertices))
    edges = []

    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if rng.random() < edge_probability:
                edges.append((i, j))

    return vertices, edges


def generate_metric_points(num_points, seed=42, width=100, height=100):
    """Generate random 2D points for metric TSP."""
    rng = random.Random(seed)
    return [(rng.uniform(0, width), rng.uniform(0, height)) for _ in range(num_points)]


def generate_set_cover_instance(universe_size=8, num_sets=6, seed=42):
    """
    Generate a random set cover instance that is likely coverable.
    """
    rng = random.Random(seed)
    universe = set(range(universe_size))
    sets = []

    # Ensure every element appears at least once
    element_to_set = {e: set() for e in universe}
    for _ in range(num_sets):
        subset_size = rng.randint(1, max(2, universe_size // 2))
        subset = set(rng.sample(list(universe), subset_size))
        sets.append(subset)
        for e in subset:
            element_to_set[e].add(len(sets) - 1)

    # Repair uncovered elements if needed
    for e in universe:
        if not element_to_set[e]:
            idx = rng.randrange(num_sets)
            sets[idx].add(e)

    costs = [rng.randint(1, 5) for _ in range(num_sets)]
    return universe, sets, costs


def generate_facility_location_instance(num_facilities=4, num_clients=6, seed=42):
    """
    Generate a small random facility location instance.
    """
    rng = random.Random(seed)

    opening_costs = [rng.randint(5, 20) for _ in range(num_facilities)]
    assignment_costs = [
        [rng.randint(1, 15) for _ in range(num_facilities)]
        for _ in range(num_clients)
    ]

    return opening_costs, assignment_costs