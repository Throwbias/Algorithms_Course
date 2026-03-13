"""
Subset Sum Problem
Exact solution using backtracking (exponential complexity)
and a greedy heuristic for comparison.
"""

def subset_sum_backtracking(nums, target, index=0, current=None):
    if current is None:
        current = []

    if target == 0:
        return current

    if index >= len(nums) or target < 0:
        return None

    # Include current number
    result = subset_sum_backtracking(
        nums, target - nums[index], index + 1, current + [nums[index]]
    )
    if result is not None:
        return result

    # Exclude current number
    return subset_sum_backtracking(nums, target, index + 1, current)


def subset_sum_greedy(nums, target):
    """
    Greedy approximation: take largest numbers first
    """
    nums = sorted(nums, reverse=True)
    subset = []
    total = 0

    for n in nums:
        if total + n <= target:
            subset.append(n)
            total += n

    if total == target:
        return subset
    return subset  # approximate result