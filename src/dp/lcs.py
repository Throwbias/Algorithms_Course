"""
lcs.py

Longest Common Subsequence implemented with:
- Naive recursion
- Top-down DP (memoization)
- Bottom-up DP (tabulation)
"""

# -----------------------------
# Naive Recursive LCS
# -----------------------------
def lcs_recursive(X, Y, m=None, n=None, counter=None):
    """
    Naive recursive LCS.

    Time Complexity: O(2^(m+n))
    """
    if counter is not None:
        counter["calls"] += 1

    if m is None:
        m = len(X)
    if n is None:
        n = len(Y)

    if m == 0 or n == 0:
        return 0

    if X[m - 1] == Y[n - 1]:
        return 1 + lcs_recursive(X, Y, m - 1, n - 1, counter)
    else:
        return max(
            lcs_recursive(X, Y, m - 1, n, counter),
            lcs_recursive(X, Y, m, n - 1, counter)
        )


# -----------------------------
# Top-Down DP (Memoization)
# -----------------------------
def lcs_memoized(X, Y, m=None, n=None, memo=None, counter=None):
    """
    Top-down DP with memoization.

    Time Complexity: O(m*n)
    Space Complexity: O(m*n)
    """
    if counter is not None:
        counter["calls"] += 1

    if m is None:
        m = len(X)
    if n is None:
        n = len(Y)
    if memo is None:
        memo = {}

    key = (m, n)
    if key in memo:
        return memo[key]

    if m == 0 or n == 0:
        memo[key] = 0
    elif X[m - 1] == Y[n - 1]:
        memo[key] = 1 + lcs_memoized(X, Y, m - 1, n - 1, memo, counter)
    else:
        memo[key] = max(
            lcs_memoized(X, Y, m - 1, n, memo, counter),
            lcs_memoized(X, Y, m, n - 1, memo, counter)
        )

    return memo[key]


# -----------------------------
# Bottom-Up DP (Tabulation)
# -----------------------------
def lcs_tabulated(X, Y):
    """
    Bottom-up DP implementation.

    Time Complexity: O(m*n)
    Space Complexity: O(m*n)
    Returns: length of LCS and DP table for reconstruction
    """
    m = len(X)
    n = len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n], dp


# -----------------------------
# Helper: Reconstruct LCS Sequence
# -----------------------------
def trace_lcs(X, Y, dp):
    """
    Reconstructs the actual LCS sequence from the DP table.
    """
    i, j = len(X), len(Y)
    lcs_seq = []

    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            lcs_seq.append(X[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    lcs_seq.reverse()
    return "".join(lcs_seq)


# -----------------------------
# Standalone Test / Debug
# -----------------------------
if __name__ == "__main__":
    X = "AGGTAB"
    Y = "GXTXAYB"

    print("LCS Results:\n")

    # Naive recursive
    counter_naive = {"calls": 0}
    val_naive = lcs_recursive(X, Y, counter=counter_naive)
    print(f"Naive Recursive Length: {val_naive} | Calls: {counter_naive['calls']}")

    # Memoized
    counter_memo = {"calls": 0}
    val_memo = lcs_memoized(X, Y, memo={}, counter=counter_memo)
    print(f"Memoized Length: {val_memo} | Calls: {counter_memo['calls']}")

    # Tabulated
    val_tab, table = lcs_tabulated(X, Y)
    seq = trace_lcs(X, Y, table)
    print(f"Tabulated Length: {val_tab} | Sequence: {seq}")

    print("\nDone.")
