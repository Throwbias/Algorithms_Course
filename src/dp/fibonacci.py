"""
fibonacci.py

Demonstrates the transition from naive recursion to optimized dynamic programming
using memoization and tabulation.
"""

# -----------------------------
# Naive Recursive Fibonacci
# -----------------------------
def fib_recursive(n, counter=None):
    """
    Naive recursive Fibonacci implementation.

    Time Complexity: O(2^n)
    """
    if counter is not None:
        counter["calls"] += 1

    if n <= 1:
        return n

    return fib_recursive(n - 1, counter) + fib_recursive(n - 2, counter)


# -----------------------------
# Top-Down DP (Memoization)
# -----------------------------
def fib_memoized(n, memo=None, counter=None):
    """
    Top-down dynamic programming Fibonacci implementation using memoization.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if counter is not None:
        counter["calls"] += 1

    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n <= 1:
        memo[n] = n
    else:
        memo[n] = fib_memoized(n - 1, memo, counter) + fib_memoized(n - 2, memo, counter)

    return memo[n]


# -----------------------------
# Bottom-Up DP (Tabulation)
# -----------------------------
def fib_tabulated(n):
    """
    Bottom-up dynamic programming Fibonacci implementation.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


# -----------------------------
# Standalone Test / Debug
# -----------------------------
if __name__ == "__main__":
    n_values = [10, 20, 30, 35]
    print("Fibonacci Results:\n")

    for n in n_values:
        # Naive recursive
        counter_naive = {"calls": 0}
        res_naive = fib_recursive(n, counter_naive)
        print(f"n={n} | Naive={res_naive} | calls={counter_naive['calls']}")

        # Memoized
        counter_memo = {"calls": 0}
        res_memo = fib_memoized(n, memo={}, counter=counter_memo)
        print(f"n={n} | Memoized={res_memo} | calls={counter_memo['calls']}")

        # Tabulated
        res_tab = fib_tabulated(n)
        print(f"n={n} | Tabulated={res_tab}")

    print("\nDone.")
