"""
Simple demo runner for Week 9 approximation algorithms.
"""

import sys
import os

# Ensure project root is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.approximation.vertex_cover_2approx import vertex_cover_2approx
from src.approximation.set_cover_lpround import set_cover_lp_relaxation_rounding
from src.approximation.facility_location_greedy import greedy_facility_location
from src.approximation.tsp_metric_approx import tsp_metric_approx
from src.approximation.maxcut_randomized import randomized_maxcut


def demo_vertex_cover():
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)]
    result = vertex_cover_2approx(edges)
    print("\nVertex Cover 2-Approximation")
    print("-----------------------------")
    print("Edges:", edges)
    print("Approximate cover:", result)


def demo_set_cover():
    universe = {1, 2, 3, 4, 5}
    sets = [{1, 2}, {2, 3, 4}, {4, 5}, {1, 5}]
    result = set_cover_lp_relaxation_rounding(universe, sets)

    print("\nSet Cover Approximation")
    print("-----------------------")
    print("Universe:", universe)
    print("Sets:", sets)
    print("Selected sets:", result["selected_sets"])
    print("Total cost:", result["total_cost"])


def demo_facility_location():
    opening_costs = [10, 12, 8]
    assignment_costs = [
        [4, 6, 3],
        [5, 2, 4],
        [7, 3, 5],
        [6, 4, 2],
    ]

    result = greedy_facility_location(opening_costs, assignment_costs)

    print("\nFacility Location (Greedy)")
    print("---------------------------")
    print("Opening costs:", opening_costs)
    print("Assignments:", result["assignments"])
    print("Open facilities:", result["open_facilities"])
    print("Total cost:", result["total_cost"])


def demo_tsp():
    points = [(0, 0), (1, 0), (2, 1), (1, 2), (0, 1)]

    result = tsp_metric_approx(points)

    print("\nMetric TSP 2-Approximation")
    print("---------------------------")
    print("Points:", points)
    print("Tour:", result["tour"])
    print("Tour cost:", result["cost"])


def demo_maxcut():
    vertices = [0, 1, 2, 3, 4]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]

    result = randomized_maxcut(vertices, edges, trials=100)

    print("\nRandomized Max-Cut")
    print("------------------")
    print("Vertices:", vertices)
    print("Edges:", edges)
    print("Left partition:", result["left"])
    print("Right partition:", result["right"])
    print("Cut value:", result["cut_value"])


if __name__ == "__main__":
    demo_vertex_cover()
    demo_set_cover()
    demo_facility_location()
    demo_tsp()
    demo_maxcut()