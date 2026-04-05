"""
Numerical stability utilities for FFTAnalyzer.
"""

from typing import List
from math import sqrt

Matrix = List[List[float]]
Vector = List[float]


def absolute_error(true_value: float, approx_value: float) -> float:
    return abs(true_value - approx_value)


def relative_error(true_value: float, approx_value: float) -> float:
    if true_value == 0:
        return abs(approx_value)
    return abs(true_value - approx_value) / abs(true_value)


def l1_norm(x: Vector) -> float:
    return sum(abs(v) for v in x)


def l2_norm(x: Vector) -> float:
    return sqrt(sum(v * v for v in x))


def inf_norm(x: Vector) -> float:
    return max(abs(v) for v in x) if x else 0.0


def _matrix_inf_norm(A: Matrix) -> float:
    return max(sum(abs(v) for v in row) for row in A) if A else 0.0


def _identity(n: int) -> Matrix:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def _copy_matrix(A: Matrix) -> Matrix:
    return [row[:] for row in A]


def _shape(A: Matrix):
    if not A or not A[0]:
        raise ValueError("matrix must be non-empty")
    rows = len(A)
    cols = len(A[0])
    if any(len(row) != cols for row in A):
        raise ValueError("matrix rows must all have same length")
    return rows, cols


def _gauss_jordan_inverse(A: Matrix) -> Matrix:
    n, m = _shape(A)
    if n != m:
        raise ValueError("matrix must be square")

    aug = [A[i][:] + _identity(n)[i] for i in range(n)]

    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-12:
            raise ValueError("matrix is singular or nearly singular")

        aug[col], aug[pivot] = aug[pivot], aug[col]

        pivot_val = aug[col][col]
        for j in range(2 * n):
            aug[col][j] /= pivot_val

        for i in range(n):
            if i == col:
                continue
            factor = aug[i][col]
            for j in range(2 * n):
                aug[i][j] -= factor * aug[col][j]

    return [row[n:] for row in aug]


def condition_number_estimate(A: Matrix) -> float:
    """
    Infinity-norm condition number estimate: ||A||_inf * ||A^-1||_inf
    """
    A_inv = _gauss_jordan_inverse(A)
    return _matrix_inf_norm(A) * _matrix_inf_norm(A_inv)


def is_ill_conditioned(A: Matrix, threshold: float = 1e3) -> bool:
    return condition_number_estimate(A) > threshold