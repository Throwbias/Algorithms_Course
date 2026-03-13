from src.approximation.vertex_cover_2approx import (
    vertex_cover_2approx,
    exact_min_vertex_cover,
    is_vertex_cover,
)


def test_vertex_cover_returns_valid_cover():
    edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
    cover = vertex_cover_2approx(edges)
    assert is_vertex_cover(edges, cover)


def test_vertex_cover_ratio_bound_small_instance():
    edges = [(0, 1), (1, 2), (2, 3)]
    approx_cover = vertex_cover_2approx(edges)
    optimal_cover = exact_min_vertex_cover(edges)

    assert len(approx_cover) <= 2 * len(optimal_cover)