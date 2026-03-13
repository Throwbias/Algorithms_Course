import math

def distance(a, b):
    return math.dist(a, b)


def tsp_nearest_neighbor(points):
    n = len(points)
    visited = [False] * n
    path = [0]
    visited[0] = True

    for _ in range(n - 1):
        last = path[-1]
        nearest = None
        best_dist = float("inf")

        for i in range(n):
            if not visited[i]:
                d = distance(points[last], points[i])
                if d < best_dist:
                    best_dist = d
                    nearest = i

        path.append(nearest)
        visited[nearest] = True

    path.append(0)
    return path