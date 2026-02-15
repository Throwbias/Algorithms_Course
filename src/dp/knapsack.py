"""
knapsack.py

0/1 Knapsack Problem implemented with:
- Naive recursion
- Top-down DP (memoization)
- Bottom-up DP (tabulation)
"""

# -----------------------------
# Naive Recursive Knapsack
# -----------------------------
def knapsack_recursive(weights, values, capacity, n=None, counter=None):
    """
    Naive recursive 0/1 Knapsack.

    Time Complexity: O(2^n)
    """
    if counter is not None:
        counter["calls"] += 1

    if n is None:
        n = len(weights)

    if n == 0 or capacity == 0:
        return 0

    if weights[n - 1] > capacity:
        return knapsack_recursive(weights, values, capacity, n - 1, counter)
    else:
        include = values[n - 1] + knapsack_recursive(weights, values, capacity - weights[n - 1], n - 1, counter)
        exclude = knapsack_recursive(weights, values, capacity, n - 1, counter)
        return max(include, exclude)


# -----------------------------
# Top-Down DP (Memoization)
# -----------------------------
def knapsack_memoized(weights, values, capacity, n=None, memo=None, counter=None):
    """
    Top-down DP with memoization.

    Time Complexity: O(n*capacity)
    Space Complexity: O(n*capacity)
    """
    if counter is not None:
        counter["calls"] += 1

    if n is None:
        n = len(weights)
    if memo is None:
        memo = {}

    key = (n, capacity)
    if key in memo:
        return memo[key]

    if n == 0 or capacity == 0:
        memo[key] = 0
    elif weights[n - 1] > capacity:
        memo[key] = knapsack_memoized(weights, values, capacity, n - 1, memo, counter)
    else:
        include = values[n - 1] + knapsack_memoized(weights, values, capacity - weights[n - 1], n - 1, memo, counter)
        exclude = knapsack_memoized(weights, values, capacity, n - 1, memo, counter)
        memo[key] = max(include, exclude)

    return memo[key]


# -----------------------------
# Bottom-Up DP (Tabulation)
# -----------------------------
def knapsack_tabulated(weights, values, capacity):
    """
    Bottom-up DP implementation.

    Time Complexity: O(n*capacity)
    Space Complexity: O(n*capacity)
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] > w:
                dp[i][w] = dp[i - 1][w]
            else:
                dp[i][w] = max(dp[i - 1][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])

    return dp[n][capacity], dp  # return DP table for reconstruction


# -----------------------------
# Helper: Reconstruct chosen items
# -----------------------------
def trace_solution(weights, values, capacity, dp_table):
    """
    Reconstructs which items were chosen from the DP table.
    Returns a list of indices.
    """
    solution = []
    i = len(weights)
    w = capacity

    while i > 0 and w > 0:
        if dp_table[i][w] != dp_table[i - 1][w]:
            solution.append(i - 1)  # item i-1 included
            w -= weights[i - 1]
        i -= 1

    solution.reverse()
    return solution


# -----------------------------
# Standalone Test / Debug
# -----------------------------
if __name__ == "__main__":
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5

    print("Knapsack Results:\n")

    # Naive recursive
    counter_naive = {"calls": 0}
    val_naive = knapsack_recursive(weights, values, capacity, counter=counter_naive)
    print(f"Naive Recursive Value: {val_naive} | Calls: {counter_naive['calls']}")

    # Memoized
    counter_memo = {"calls": 0}
    val_memo = knapsack_memoized(weights, values, capacity, memo={}, counter=counter_memo)
    print(f"Memoized Value: {val_memo} | Calls: {counter_memo['calls']}")

    # Tabulated
    val_tab, table = knapsack_tabulated(weights, values, capacity)
    solution = trace_solution(weights, values, capacity, table)
    print(f"Tabulated Value: {val_tab} | Selected items indices: {solution}")

    print("\nDone.")
