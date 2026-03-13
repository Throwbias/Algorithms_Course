from src.complexity.subset_sum_backtracking import subset_sum_backtracking, subset_sum_greedy


def test_subset_sum_backtracking_finds_solution():
    nums = [3, 34, 4, 12, 5, 2]
    target = 9
    result = subset_sum_backtracking(nums, target)
    assert result is not None
    assert sum(result) == target


def test_subset_sum_backtracking_returns_none_when_impossible():
    nums = [5, 10, 20]
    target = 3
    result = subset_sum_backtracking(nums, target)
    assert result is None


def test_subset_sum_greedy_never_exceeds_target():
    nums = [8, 7, 6, 5]
    target = 15
    result = subset_sum_greedy(nums, target)
    assert sum(result) <= target