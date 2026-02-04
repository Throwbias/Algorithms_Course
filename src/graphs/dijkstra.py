# src/graphs/dijkstra.py

import heapq

def dijkstra(graph, start):
    if start not in graph.nodes:
        return {}, {}

    distances = {node: float("inf") for node in graph.nodes}
    previous = {node: None for node in graph.nodes}
    distances[start] = 0

    heap = [(0, start)]

    while heap:
        current_dist, u = heapq.heappop(heap)
        if current_dist > distances[u]:
            continue

        for v, weight in graph.get_neighbors(u):
            alt = current_dist + weight
            if alt < distances[v]:
                distances[v] = alt
                previous[v] = u
                heapq.heappush(heap, (alt, v))

    return distances, previous
