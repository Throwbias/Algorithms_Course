import pytest
from src.randomized.randomized_selection import randomized_selection, QuickSelectStats


def test_randomized_selection_min_median_max():
    data = [9, 1, 7, 3, 2, 8, 5]
    assert randomized_selection(data, 0, seed=1) == min(data)
    assert randomized_selection(data, len(data) // 2, seed=1) == sorted(data)[len(data) // 2]
    assert randomized_selection(data, len(data) - 1, seed=1) == max(data)


def test_randomized_selection_does_not_mutate():
    data = [3, 1, 2]
    out = randomized_selection(data, 1, seed=42)
    assert data == [3, 1, 2]
    assert out == 2


def test_randomized_selection_stats():
    data = [10, 7, 8, 9, 1, 5]
    s = QuickSelectStats()
    out = randomized_selection(data, 2, seed=123, stats=s)
    assert out == sorted(data)[2]
    assert s.partitions >= 1
    assert s.comparisons >= 1
    assert s.max_depth >= 1


def test_randomized_selection_k_out_of_bounds():
    with pytest.raises(ValueError):
        randomized_selection([1, 2, 3], -1)
    with pytest.raises(ValueError):
        randomized_selection([1, 2, 3], 3)