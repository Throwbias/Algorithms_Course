"""
Space-Optimized 0/1 Knapsack
Reduces space complexity from O(nW) to O(W)
"""

from typing import List


def knapsack_space_optimized(
    weights: List[int],
    values: List[int],
    capacity: int
) -> int:
    """
    Time Complexity: O(n * W)
    Space Complexity: O(W)
    """

    dp = [0] * (capacity + 1)

    for i in range(len(weights)):
        weight = weights[i]
        value = values[i]

        # Iterate backwards to prevent overwriting needed states
        for w in range(capacity, weight - 1, -1):
            dp[w] = max(dp[w], dp[w - weight] + value)

    return dp[capacity]