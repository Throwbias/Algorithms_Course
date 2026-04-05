from fft_analyzer.core.numerical import (
    absolute_error,
    relative_error,
    l1_norm,
    l2_norm,
    inf_norm,
    condition_number_estimate,
    is_ill_conditioned,
)


def test_errors():
    assert absolute_error(10.0, 9.5) == 0.5
    assert relative_error(10.0, 9.5) == 0.05


def test_vector_norms():
    x = [3.0, -4.0]
    assert l1_norm(x) == 7.0
    assert abs(l2_norm(x) - 5.0) < 1e-6
    assert inf_norm(x) == 4.0


def test_condition_number_identity():
    A = [[1.0, 0.0], [0.0, 1.0]]
    cond = condition_number_estimate(A)
    assert abs(cond - 1.0) < 1e-6
    assert is_ill_conditioned(A) is False


def test_condition_number_detects_bad_matrix():
    A = [[1.0, 1.0], [1.0, 1.000001]]
    assert is_ill_conditioned(A, threshold=100) is True