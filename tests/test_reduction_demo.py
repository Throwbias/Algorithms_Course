from src.complexity.reduction_demo import ThreeSATInstance, reduce_3sat_to_vertex_cover


def test_reduction_target_k():
    instance = ThreeSATInstance(
        num_vars=3,
        clauses=[
            [1, -2, 3],
            [-1, 2, -3],
        ]
    )
    vc_instance, _ = reduce_3sat_to_vertex_cover(instance)
    assert vc_instance.k == 3 + 2 * 2


def test_reduction_creates_variable_nodes():
    instance = ThreeSATInstance(
        num_vars=2,
        clauses=[[1, -2, 1]]
    )
    vc_instance, _ = reduce_3sat_to_vertex_cover(instance)
    assert "x1" in vc_instance.vertices
    assert "~x1" in vc_instance.vertices
    assert "x2" in vc_instance.vertices
    assert "~x2" in vc_instance.vertices