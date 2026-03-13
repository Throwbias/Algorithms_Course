from src.approximation.tsp_metric_approx import tsp_metric_approx, exact_tsp


def test_tsp_metric_returns_valid_tour():
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    result = tsp_metric_approx(points)
    tour = result["tour"]

    assert tour[0] == tour[-1]
    assert len(set(tour[:-1])) == len(points)


def test_tsp_metric_approx_ratio_small_instance():
    points = [(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)]

    approx = tsp_metric_approx(points)
    optimal = exact_tsp(points)

    assert approx["cost"] <= 2 * optimal["cost"] + 1e-9