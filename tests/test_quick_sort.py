import pytest
from src.sorting.quick_sort import quick_sort

@pytest.mark.parametrize(
    "input_list, expected",
    [
        ([], []),
        ([1], [1]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        ([2, 3, 2, 1, 4, 3], [1, 2, 2, 3, 3, 4]),
        ([5, 1, 4, 2, 8, 0, 3, 7, 6, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ]
)
def test_quick_sort(input_list, expected):
    result = quick_sort(input_list)
    assert result == expected
    # ensure non-destructive
    assert input_list != result or input_list == expected
