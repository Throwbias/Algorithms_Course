# src/utils/graph_generator.py

import random
from src.graphs.graph import Graph

def generate_sparse_graph(n):
    """Generate a sparse undirected, unweighted/weighted graph with n nodes."""
    g = Graph(directed=False)
    for i in range(n):
        g.add_node(i)
    for _ in range(n):  # ~1 edge per node
        u, v = random.sample(range(n), 2)
        g.add_edge(u, v, random.randint(1, 10))
    return g

def generate_dense_graph(n):
    """Generate a dense undirected, weighted graph with n nodes."""
    g = Graph(directed=False)
    for i in range(n):
        g.add_node(i)
    for u in range(n):
        for v in range(u + 1, n):  # avoids duplicate edges and self-loops
            g.add_edge(u, v, random.randint(1, 10))
    return g
