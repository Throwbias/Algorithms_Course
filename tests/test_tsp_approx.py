from src.complexity.traveling_salesman_approx import tsp_nearest_neighbor


def test_tsp_nearest_neighbor_returns_cycle():
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    path = tsp_nearest_neighbor(points)

    assert path[0] == 0
    assert path[-1] == 0
    assert len(path) == len(points) + 1
    assert set(path[:-1]) == {0, 1, 2, 3}