# src/graphs/dfs.py

def dfs_recursive(graph, start, visited=None, order=None):
    """
    Recursive Depth-First Search
    """
    if start not in graph.nodes:
        return []

    if visited is None:
        visited = set()
    if order is None:
        order = []

    visited.add(start)
    order.append(start)

    for neighbor_info in graph.get_neighbors(start):
        neighbor = neighbor_info[0] if isinstance(neighbor_info, tuple) else neighbor_info
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited, order)

    return order


def dfs_iterative(graph, start):
    """
    Iterative Depth-First Search using a stack
    """
    if start not in graph.nodes:
        return []

    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            # reverse to maintain the same order as recursive DFS
            for neighbor_info in reversed(graph.get_neighbors(node)):
                neighbor = neighbor_info[0] if isinstance(neighbor_info, tuple) else neighbor_info
                if neighbor not in visited:
                    stack.append(neighbor)

    return order
