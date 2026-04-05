from fft_analyzer.core.matrix import (
    matrix_multiply,
    solve_linear_system_lu,
    determinant_from_lu,
    qr_decomposition,
)


def approx_equal(a, b, tol=1e-6):
    return abs(a - b) < tol


def test_matrix_multiply():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    C = matrix_multiply(A, B)
    assert C == [[19.0, 22.0], [43.0, 50.0]]


def test_solve_linear_system_lu():
    A = [[2.0, 1.0], [5.0, 7.0]]
    b = [11.0, 13.0]
    x = solve_linear_system_lu(A, b)
    assert approx_equal(x[0], 64 / 9)
    assert approx_equal(x[1], -29 / 9)


def test_determinant_from_lu():
    A = [[1.0, 2.0], [3.0, 4.0]]
    det = determinant_from_lu(A)
    assert approx_equal(det, -2.0)


def test_qr_decomposition_reconstructs_matrix():
    A = [[1.0, 1.0], [1.0, -1.0]]
    Q, R = qr_decomposition(A)
    reconstructed = matrix_multiply(Q, R)

    for i in range(2):
        for j in range(2):
            assert approx_equal(reconstructed[i][j], A[i][j], tol=1e-5)