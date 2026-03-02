from src.sorting.deterministic_quick_sort import deterministic_quick_sort


def test_deterministic_quick_sort_basic():
    assert deterministic_quick_sort([]) == []
    assert deterministic_quick_sort([1]) == [1]
    assert deterministic_quick_sort([2, 1]) == [1, 2]
    assert deterministic_quick_sort([3, 1, 2]) == [1, 2, 3]


def test_deterministic_quick_sort_duplicates():
    data = [5, 3, 3, 2, 2, 1]
    assert deterministic_quick_sort(data) == sorted(data)


def test_deterministic_quick_sort_does_not_mutate():
    data = [3, 2, 1]
    out = deterministic_quick_sort(data)
    assert data == [3, 2, 1]
    assert out == [1, 2, 3]