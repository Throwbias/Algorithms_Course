"""
Matrix Chain Multiplication (MCM) - Interval DP
"""

# -----------------------------
# Recursive Memoized Solution
# -----------------------------
def mcm_recursive(p, i=None, j=None, memo=None, split=None):
    """
    Recursive memoized solution for Matrix Chain Multiplication.
    
    Args:
        p (list): Matrix dimensions, length n+1, where Ai has dimensions p[i-1] x p[i]
        i (int): Start index (1-based)
        j (int): End index (1-based)
        memo (dict): Memoization dictionary
        split (dict): Stores k for optimal parenthesization
    Returns:
        int: Minimum multiplication cost
    """
    n = len(p) - 1
    if i is None: i = 1
    if j is None: j = n
    if memo is None: memo = {}
    if split is None: split = {}

    if i == j:
        return 0

    if (i, j) in memo:
        return memo[(i, j)]

    min_cost = float('inf')
    best_k = None
    for k in range(i, j):
        cost = (mcm_recursive(p, i, k, memo, split) +
                mcm_recursive(p, k+1, j, memo, split) +
                p[i-1]*p[k]*p[j])
        if cost < min_cost:
            min_cost = cost
            best_k = k

    memo[(i, j)] = min_cost
    split[(i, j)] = best_k
    return min_cost


# -----------------------------
# Bottom-Up DP Solution
# -----------------------------
def mcm_tabulated(p):
    """
    Bottom-up DP solution for MCM.
    
    Args:
        p (list): Matrix dimensions
    Returns:
        tuple: (minimum multiplication cost, dp table, split table)
    """
    n = len(p) - 1
    dp = [[0]*(n+1) for _ in range(n+1)]
    split = [[0]*(n+1) for _ in range(n+1)]

    for l in range(2, n+1):  # chain length
        for i in range(1, n-l+2):
            j = i + l - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + p[i-1]*p[k]*p[j]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k
    return dp[1][n], dp, split  # return correct min cost


# -----------------------------
# Parenthesization Reconstruction
# -----------------------------
def print_optimal_parens(split, i, j):
    """
    Recursively reconstruct the optimal parenthesization.
    Works with both 2D list (DP) and dict (recursive memo).
    """
    if i == j:
        return f"A{i}"
    if isinstance(split, dict):
        k = split[(i, j)]
    else:
        k = split[i][j]
    left = print_optimal_parens(split, i, k)
    right = print_optimal_parens(split, k+1, j)
    return f"({left} x {right})"


# -----------------------------
# Standalone Test / Demo
# -----------------------------
if __name__ == "__main__":
    p = [5, 10, 3, 12, 5, 50, 6]  # example dimensions
    print("Matrix Chain Multiplication Demo\n")

    # Recursive memoized
    memo = {}
    split_memo = {}
    min_cost_rec = mcm_recursive(p, memo=memo, split=split_memo)
    print(f"Recursive Memoized Min Cost: {min_cost_rec}")
    print(f"Optimal Parenthesization (recursive): {print_optimal_parens(split_memo, 1, len(p)-1)}")

    # Bottom-up DP
    min_cost_dp, dp_table, split_table = mcm_tabulated(p)
    print(f"Bottom-Up DP Min Cost: {min_cost_dp}")
    print(f"Optimal Parenthesization (DP): {print_optimal_parens(split_table, 1, len(p)-1)}")