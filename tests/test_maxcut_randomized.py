from src.approximation.maxcut_randomized import randomized_maxcut, exact_maxcut


def test_randomized_maxcut_returns_valid_partition():
    vertices = [0, 1, 2, 3]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]

    result = randomized_maxcut(vertices, edges, trials=50, seed=1)

    assert result["left"].isdisjoint(result["right"])
    assert result["left"].union(result["right"]) == set(vertices)
    assert result["cut_value"] >= 0


def test_randomized_maxcut_not_better_than_optimum():
    vertices = [0, 1, 2, 3]
    edges = [(0, 1), (0, 2), (1, 3), (2, 3)]

    approx = randomized_maxcut(vertices, edges, trials=100, seed=2)
    optimal = exact_maxcut(vertices, edges)

    assert approx["cut_value"] <= optimal["cut_value"]