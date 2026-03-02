# tests/test_space_optimized_knapsack.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from dp_advanced.space_optimized_knapsack import knapsack_space_optimized


def test_basic_case():
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7

    assert knapsack_space_optimized(weights, values, capacity) == 9


def test_zero_capacity():
    assert knapsack_space_optimized([1, 2, 3], [10, 20, 30], 0) == 0


def test_single_item():
    assert knapsack_space_optimized([5], [10], 5) == 10