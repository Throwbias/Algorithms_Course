from typing import List
import math
import cmath

Matrix = List[List[float]]


def _next_power_of_two(n: int) -> int:
    p = 1
    while p < n:
        p <<= 1
    return p


def _fft_1d(x):
    n = len(x)
    if n == 1:
        return [complex(x[0])]
    even = _fft_1d(x[0::2])
    odd = _fft_1d(x[1::2])
    out = [0j] * n
    for k in range(n // 2):
        w = cmath.exp(-2j * cmath.pi * k / n) * odd[k]
        out[k] = even[k] + w
        out[k + n // 2] = even[k] - w
    return out


def _ifft_1d(X):
    n = len(X)
    conj = [z.conjugate() for z in X]
    inv = _fft_1d(conj)
    return [z.conjugate() / n for z in inv]


def _fft2d(mat):
    rows = len(mat)
    cols = len(mat[0])
    row_fft = [_fft_1d([complex(v) for v in row]) for row in mat]
    out = [[0j] * cols for _ in range(rows)]
    for j in range(cols):
        col = [row_fft[i][j] for i in range(rows)]
        col_fft = _fft_1d(col)
        for i in range(rows):
            out[i][j] = col_fft[i]
    return out


def _ifft2d(mat):
    rows = len(mat)
    cols = len(mat[0])
    row_ifft = [_ifft_1d(row) for row in mat]
    out = [[0j] * cols for _ in range(rows)]
    for j in range(cols):
        col = [row_ifft[i][j] for i in range(rows)]
        col_ifft = _ifft_1d(col)
        for i in range(rows):
            out[i][j] = col_ifft[i]
    return out


def _pad_image(image: Matrix):
    r, c = len(image), len(image[0])
    pr, pc = _next_power_of_two(r), _next_power_of_two(c)
    out = [[0.0] * pc for _ in range(pr)]
    for i in range(r):
        for j in range(c):
            out[i][j] = image[i][j]
    return out, r, c


def gaussian_blur_fft(image: Matrix, sigma: float = 1.0) -> Matrix:
    padded, orig_r, orig_c = _pad_image(image)
    rows, cols = len(padded), len(padded[0])

    F = _fft2d(padded)

    for u in range(rows):
        for v in range(cols):
            du = min(u, rows - u)
            dv = min(v, cols - v)
            h = math.exp(-(du * du + dv * dv) / (2 * sigma * sigma))
            F[u][v] *= h

    blurred = _ifft2d(F)
    return [[blurred[i][j].real for j in range(orig_c)] for i in range(orig_r)]


def edge_detect_simple(image: Matrix) -> Matrix:
    rows, cols = len(image), len(image[0])
    out = [[0.0] * cols for _ in range(rows)]
    gx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    gy = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            sx = 0.0
            sy = 0.0
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    sx += image[i + di][j + dj] * gx[di + 1][dj + 1]
                    sy += image[i + di][j + dj] * gy[di + 1][dj + 1]
            out[i][j] = math.sqrt(sx * sx + sy * sy)
    return out