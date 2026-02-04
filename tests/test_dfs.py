# tests/test_dfs.py
import pytest
from src.graphs.graph import Graph
from src.graphs.dfs import dfs_recursive, dfs_iterative

def test_dfs_simple_graph():
    g = Graph(directed=False, weighted=True)
    g.add_edge("A", "B", 1)
    g.add_edge("A", "C", 1)
    g.add_edge("B", "D", 1)

    order_recursive = dfs_recursive(g, "A")
    order_iterative = dfs_iterative(g, "A")
    for order in [order_recursive, order_iterative]:
        assert "A" in order
        assert "B" in order
        assert "C" in order
        assert "D" in order

def test_dfs_disconnected_graph():
    g = Graph(directed=False, weighted=True)
    g.add_edge("A", "B", 1)
    g.add_node("C")  # disconnected node

    order_recursive = dfs_recursive(g, "A")
    order_iterative = dfs_iterative(g, "A")
    for order in [order_recursive, order_iterative]:
        assert "A" in order
        assert "B" in order
        assert "C" not in order  # C is disconnected

def test_dfs_start_not_in_graph():
    g = Graph()
    g.add_edge("X", "Y")
    order_recursive = dfs_recursive(g, "Z")
    order_iterative = dfs_iterative(g, "Z")
    assert order_recursive == []
    assert order_iterative == []
