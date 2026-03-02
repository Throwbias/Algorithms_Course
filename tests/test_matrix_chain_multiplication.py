"""
Pytest for Matrix Chain Multiplication (MCM)
Tests both recursive memoized and bottom-up DP implementations
"""

import pytest
from src.dp_advanced.matrix_chain_multiplication import (
    mcm_recursive,
    mcm_tabulated,
    print_optimal_parens
)


# ---------- Test Data ----------
test_cases = [
    # format: (matrix dimensions p[], expected min cost)
    ([5, 10, 3, 12, 5, 50, 6], 2010),
    ([2, 3, 4, 5], 64),
    ([1, 2, 3, 4, 3], 30),
    ([10, 20, 30], 6000)
]

# ---------- Recursive Memoized Tests ----------
@pytest.mark.parametrize("p, expected_cost", test_cases)
def test_mcm_recursive(p, expected_cost):
    memo = {}
    split_memo = {}
    min_cost = mcm_recursive(p, memo=memo, split=split_memo)
    assert min_cost == expected_cost
    # Optional: check parenthesization string is non-empty
    parens = print_optimal_parens(split_memo, 1, len(p)-1)
    assert isinstance(parens, str) and len(parens) > 0

# ---------- Bottom-Up DP Tests ----------
@pytest.mark.parametrize("p, expected_cost", test_cases)
def test_mcm_tabulated(p, expected_cost):
    min_cost, dp_table, split_table = mcm_tabulated(p)
    assert min_cost == expected_cost
    # Optional: check parenthesization string is non-empty
    parens = print_optimal_parens(split_table, 1, len(p)-1)
    assert isinstance(parens, str) and len(parens) > 0