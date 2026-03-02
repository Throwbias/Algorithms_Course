import math

# -----------------------------
# Bitmask DP for TSP
# -----------------------------
def tsp_bitmask(distance_matrix):
    """
    Solve TSP using DP with bitmasking.

    Args:
        distance_matrix (list of lists): NxN distance matrix

    Returns:
        tuple: (min_cost, tour)
            min_cost: minimal total distance
            tour: list of city indices representing optimal tour (starts/ends at 0)
    """
    n = len(distance_matrix)
    if n == 0:
        return 0, []
    if n == 1:
        return 0, [0, 0]

    FULL_MASK = (1 << n) - 1

    # dp[mask][i] = min cost to visit all cities in mask ending at city i
    dp = [[math.inf] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]

    # starting city 0
    dp[1][0] = 0  # mask with only city 0 visited

    for mask in range(1, 1 << n):
        if not (mask & 1):
            continue  # enforce that city 0 is always included
        for u in range(n):
            if not (mask & (1 << u)):
                continue
            cur_cost = dp[mask][u]
            if cur_cost == math.inf:
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue  # v already visited
                next_mask = mask | (1 << v)
                new_cost = cur_cost + distance_matrix[u][v]
                if new_cost < dp[next_mask][v]:
                    dp[next_mask][v] = new_cost
                    parent[next_mask][v] = u

    # close the tour back to city 0
    min_cost = math.inf
    last_city = -1
    for i in range(1, n):
        cost = dp[FULL_MASK][i] + distance_matrix[i][0]
        if cost < min_cost:
            min_cost = cost
            last_city = i

    # reconstruct path ending at last_city
    tour = []
    mask = FULL_MASK
    city = last_city
    while city != -1:
        tour.append(city)
        prev_city = parent[mask][city]
        mask ^= (1 << city)
        city = prev_city

    tour.append(0)   # add start
    tour.reverse()   # now starts at 0

    # ✅ IMPORTANT: actually close the cycle in the returned tour
    tour.append(0)

    return min_cost, tour


# -----------------------------
# Standalone Test / Debug
# -----------------------------
if __name__ == "__main__":
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]

    cost, tour = tsp_bitmask(dist)
    print("Optimal tour cost:", cost)
    print("Optimal tour:", tour)