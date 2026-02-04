# tests/test_bfs.py
import pytest
from src.graphs.graph import Graph
from src.graphs.bfs import bfs

def test_bfs_simple_graph():
    g = Graph(directed=False, weighted=True)
    g.add_edge("A", "B", 1)
    g.add_edge("A", "C", 1)
    g.add_edge("B", "D", 1)

    order = bfs(g, "A")
    assert order == ["A", "B", "C", "D"] or order == ["A", "C", "B", "D"]

def test_bfs_disconnected_graph():
    g = Graph(directed=False, weighted=True)
    g.add_edge("A", "B", 1)
    g.add_node("C")  # disconnected node

    order = bfs(g, "A")
    assert "A" in order
    assert "B" in order
    assert "C" not in order  # C is disconnected

def test_bfs_start_not_in_graph():
    g = Graph()
    g.add_edge("X", "Y")
    order = bfs(g, "Z")
    assert order == []  # start node not in graph
