# tests/test_bitmask_tsp.py

import sys
import os
import pytest

# -----------------------------
# Add src folder to Python path
# -----------------------------
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from src.dp_advanced.bitmask_traveling_salesman import tsp_bitmask  

# -----------------------------
# Test cases for TSP
# -----------------------------
@pytest.mark.parametrize(
    "dist_matrix, expected_cost, expected_tour",
    [
        # 4 cities example
        (
            [
                [0, 10, 15, 20],
                [10, 0, 35, 25],
                [15, 35, 0, 30],
                [20, 25, 30, 0]
            ],
            80,
            [0, 1, 3, 2, 0]  # one optimal tour (rotations/reflections are okay)
        ),
        # 3 cities simple
        (
            [
                [0, 1, 5],
                [1, 0, 2],
                [5, 2, 0]
            ],
            8,
            [0, 1, 2, 0]
        ),
        # 5 cities example
        (
            [
                [0, 2, 9, 10, 7],
                [2, 0, 6, 4, 3],
                [9, 6, 0, 8, 5],
                [10, 4, 8, 0, 6],
                [7, 3, 5, 6, 0]
            ],
            26,  # cost according to your algorithm
            [0, 1, 3, 2, 4, 0]
        ),
    ]
)
def test_tsp_bitmask(dist_matrix, expected_cost, expected_tour):
    cost, tour = tsp_bitmask(dist_matrix)
    # Check cost
    assert cost == expected_cost
    # Check tour starts and ends at 0
    assert tour[0] == 0 and tour[-1] == 0