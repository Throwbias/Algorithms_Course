from src.graphs.graph import Graph
from src.graphs.dijkstra import dijkstra


def test_dijkstra_simple_graph():
    g = Graph(directed=True, weighted=True)
    g.add_edge("A", "B", 1)
    g.add_edge("A", "C", 4)
    g.add_edge("B", "C", 2)
    g.add_edge("B", "D", 5)
    g.add_edge("C", "D", 1)

    distances, predecessors = dijkstra(g, "A")

    assert distances["A"] == 0
    assert distances["B"] == 1
    assert distances["C"] == 3
    assert distances["D"] == 4

    assert predecessors["B"] == "A"
    assert predecessors["C"] == "B"
    assert predecessors["D"] == "C"


def test_dijkstra_disconnected_graph():
    g = Graph(directed=True, weighted=True)
    g.add_edge(1, 2, 3)
    g.add_node(3)

    distances, _ = dijkstra(g, 1)

    assert distances[1] == 0
    assert distances[2] == 3
    assert distances[3] == float("inf")


def test_dijkstra_invalid_source():
    g = Graph(directed=True, weighted=True)
    g.add_edge("X", "Y", 1)

    distances, _ = dijkstra(g, "Z")

    assert all(v == float("inf") for v in distances.values())
