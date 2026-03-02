from src.randomized.randomized_quicksort import randomized_quicksort, QuickSortStats


def test_randomized_quicksort_empty_and_single():
    assert randomized_quicksort([]) == []
    assert randomized_quicksort([1]) == [1]


def test_randomized_quicksort_basic():
    assert randomized_quicksort([2, 1]) == [1, 2]
    assert randomized_quicksort([3, 1, 2]) == [1, 2, 3]


def test_randomized_quicksort_duplicates():
    data = [5, 3, 3, 2, 2, 1]
    assert randomized_quicksort(data) == sorted(data)


def test_randomized_quicksort_does_not_mutate_input():
    data = [3, 2, 1]
    out = randomized_quicksort(data, seed=42)
    assert data == [3, 2, 1]
    assert out == [1, 2, 3]


def test_randomized_quicksort_reproducible_with_seed():
    data = [7, 1, 9, 2, 5, 3]
    out1 = randomized_quicksort(data, seed=123)
    out2 = randomized_quicksort(data, seed=123)
    assert out1 == out2 == sorted(data)


def test_stats_counts():
    data = [4, 1, 3, 2]
    s = QuickSortStats()
    out = randomized_quicksort(data, seed=1, stats=s)
    assert out == sorted(data)
    assert s.partitions >= 1
    assert s.comparisons >= 1