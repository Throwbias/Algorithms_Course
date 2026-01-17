import pytest
from src.sorting.basic_sorts import bubble_sort, selection_sort, insertion_sort

SORT_FUNCTIONS = [bubble_sort, selection_sort, insertion_sort]

@pytest.mark.parametrize("sort_func", SORT_FUNCTIONS)
def test_empty_list(sort_func):
    assert sort_func([]) == []

@pytest.mark.parametrize("sort_func", SORT_FUNCTIONS)
def test_single_element(sort_func):
    assert sort_func([42]) == [42]

@pytest.mark.parametrize("sort_func", SORT_FUNCTIONS)
def test_already_sorted(sort_func):
    data = [1, 2, 3, 4, 5]
    result = sort_func(data)
    assert result == [1, 2, 3, 4, 5]
    assert data == [1, 2, 3, 4, 5]  # Original list not modified

@pytest.mark.parametrize("sort_func", SORT_FUNCTIONS)
def test_reverse_sorted(sort_func):
    data = [5, 4, 3, 2, 1]
    result = sort_func(data)
    assert result == [1, 2, 3, 4, 5]

@pytest.mark.parametrize("sort_func", SORT_FUNCTIONS)
def test_duplicates(sort_func):
    data = [3, 1, 2, 3, 1]
    result = sort_func(data)
    assert result == [1, 1, 2, 3, 3]

@pytest.mark.parametrize("sort_func", SORT_FUNCTIONS)
def test_random_large_list(sort_func):
    import random
    data = [random.randint(0, 1000) for _ in range(100)]
    result = sort_func(data)
    assert result == sorted(data)
