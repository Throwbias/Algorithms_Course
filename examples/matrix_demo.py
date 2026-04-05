import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fft_analyzer.core.matrix import (
    matrix_multiply,
    solve_linear_system_lu,
    determinant_from_lu,
)
from fft_analyzer.core.numerical import condition_number_estimate

A = [[2.0, 1.0], [5.0, 7.0]]
B = [[1.0, 2.0], [3.0, 4.0]]
b = [11.0, 13.0]

print("A * B =", matrix_multiply(A, B))
print("solve Ax=b =", solve_linear_system_lu(A, b))
print("det(A) =", determinant_from_lu(A))
print("cond(B) =", condition_number_estimate(B))