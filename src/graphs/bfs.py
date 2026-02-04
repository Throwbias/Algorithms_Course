# src/graphs/bfs.py

from collections import deque

def bfs(graph, start):
    """
    Breadth-First Search
    Returns the traversal order starting from `start`.
    """
    if start not in graph.nodes:
        return []

    visited = set()
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            order.append(node)
            for neighbor_info in graph.get_neighbors(node):
                neighbor = neighbor_info[0] if isinstance(neighbor_info, tuple) else neighbor_info
                if neighbor not in visited:
                    queue.append(neighbor)

    return order
