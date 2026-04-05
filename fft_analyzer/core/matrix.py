"""
Core matrix algorithms for FFTAnalyzer.

Implements the minimum required checklist items:
- classical O(n^3) matrix multiplication
- LU decomposition with partial pivoting
- solving Ax=b via LU
- determinant via LU
- QR decomposition (classical Gram-Schmidt)
"""

from typing import List, Tuple


Matrix = List[List[float]]
Vector = List[float]


def _shape(A: Matrix) -> Tuple[int, int]:
    if not A or not A[0]:
        raise ValueError("matrix must be non-empty")
    rows = len(A)
    cols = len(A[0])
    if any(len(row) != cols for row in A):
        raise ValueError("matrix rows must all have same length")
    return rows, cols


def _identity(n: int) -> Matrix:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def _copy_matrix(A: Matrix) -> Matrix:
    return [row[:] for row in A]


def matrix_multiply(A: Matrix, B: Matrix) -> Matrix:
    """
    Classical O(n^3) matrix multiplication.
    """
    a_rows, a_cols = _shape(A)
    b_rows, b_cols = _shape(B)

    if a_cols != b_rows:
        raise ValueError("incompatible matrix dimensions for multiplication")

    C = [[0.0 for _ in range(b_cols)] for _ in range(a_rows)]

    for i in range(a_rows):
        for k in range(a_cols):
            for j in range(b_cols):
                C[i][j] += A[i][k] * B[k][j]

    return C


def lu_decomposition(A: Matrix) -> Tuple[Matrix, Matrix, Matrix, int]:
    """
    LU decomposition with partial pivoting.
    Returns P, L, U, swap_count such that P*A = L*U
    """
    n, m = _shape(A)
    if n != m:
        raise ValueError("LU decomposition requires a square matrix")

    U = _copy_matrix(A)
    L = _identity(n)
    P = _identity(n)
    swap_count = 0

    for k in range(n):
        pivot_row = max(range(k, n), key=lambda i: abs(U[i][k]))
        if abs(U[pivot_row][k]) < 1e-12:
            raise ValueError("matrix is singular or nearly singular")

        if pivot_row != k:
            U[k], U[pivot_row] = U[pivot_row], U[k]
            P[k], P[pivot_row] = P[pivot_row], P[k]

            for j in range(k):
                L[k][j], L[pivot_row][j] = L[pivot_row][j], L[k][j]

            swap_count += 1

        for i in range(k + 1, n):
            factor = U[i][k] / U[k][k]
            L[i][k] = factor
            for j in range(k, n):
                U[i][j] -= factor * U[k][j]

    return P, L, U, swap_count


def _permute_vector(P: Matrix, b: Vector) -> Vector:
    return [sum(P[i][j] * b[j] for j in range(len(b))) for i in range(len(P))]


def _forward_substitution(L: Matrix, b: Vector) -> Vector:
    n, m = _shape(L)
    if n != m or len(b) != n:
        raise ValueError("dimension mismatch in forward substitution")

    y = [0.0] * n
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))
    return y


def _backward_substitution(U: Matrix, y: Vector) -> Vector:
    n, m = _shape(U)
    if n != m or len(y) != n:
        raise ValueError("dimension mismatch in backward substitution")

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        if abs(U[i][i]) < 1e-12:
            raise ValueError("matrix is singular during back substitution")
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x


def solve_linear_system_lu(A: Matrix, b: Vector) -> Vector:
    """
    Solve Ax=b using LU decomposition with partial pivoting.
    """
    n, m = _shape(A)
    if n != m:
        raise ValueError("A must be square")
    if len(b) != n:
        raise ValueError("b length must match A dimensions")

    P, L, U, _ = lu_decomposition(A)
    pb = _permute_vector(P, b)
    y = _forward_substitution(L, pb)
    x = _backward_substitution(U, y)
    return x


def determinant_from_lu(A: Matrix) -> float:
    """
    Determinant computed from LU decomposition.
    """
    _, _, U, swap_count = lu_decomposition(A)
    det = 1.0
    for i in range(len(U)):
        det *= U[i][i]
    if swap_count % 2 == 1:
        det *= -1
    return det


def qr_decomposition(A: Matrix) -> Tuple[Matrix, Matrix]:
    """
    QR decomposition using classical Gram-Schmidt.
    Returns Q, R such that A = Q*R
    """
    m, n = _shape(A)
    A_cols = [[A[i][j] for i in range(m)] for j in range(n)]

    Q_cols = []
    R = [[0.0 for _ in range(n)] for _ in range(n)]

    for j in range(n):
        v = A_cols[j][:]

        for i in range(j):
            R[i][j] = sum(Q_cols[i][k] * A_cols[j][k] for k in range(m))
            for k in range(m):
                v[k] -= R[i][j] * Q_cols[i][k]

        norm_v = sum(vk * vk for vk in v) ** 0.5
        if norm_v < 1e-12:
            raise ValueError("matrix columns are linearly dependent or nearly so")

        R[j][j] = norm_v
        q = [vk / norm_v for vk in v]
        Q_cols.append(q)

    Q = [[Q_cols[j][i] for j in range(n)] for i in range(m)]
    return Q, R