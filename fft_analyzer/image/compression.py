from typing import List
import math

Matrix = List[List[float]]


def dct_2d(block: Matrix) -> Matrix:
    n = len(block)
    m = len(block[0])
    out = [[0.0] * m for _ in range(n)]

    for u in range(n):
        for v in range(m):
            alpha_u = math.sqrt(1 / n) if u == 0 else math.sqrt(2 / n)
            alpha_v = math.sqrt(1 / m) if v == 0 else math.sqrt(2 / m)
            s = 0.0
            for x in range(n):
                for y in range(m):
                    s += (
                        block[x][y]
                        * math.cos((2 * x + 1) * u * math.pi / (2 * n))
                        * math.cos((2 * y + 1) * v * math.pi / (2 * m))
                    )
            out[u][v] = alpha_u * alpha_v * s
    return out


def idct_2d(coeffs: Matrix) -> Matrix:
    n = len(coeffs)
    m = len(coeffs[0])
    out = [[0.0] * m for _ in range(n)]

    for x in range(n):
        for y in range(m):
            s = 0.0
            for u in range(n):
                for v in range(m):
                    alpha_u = math.sqrt(1 / n) if u == 0 else math.sqrt(2 / n)
                    alpha_v = math.sqrt(1 / m) if v == 0 else math.sqrt(2 / m)
                    s += (
                        alpha_u
                        * alpha_v
                        * coeffs[u][v]
                        * math.cos((2 * x + 1) * u * math.pi / (2 * n))
                        * math.cos((2 * y + 1) * v * math.pi / (2 * m))
                    )
            out[x][y] = s
    return out


def compress_image(image: Matrix, quality: float = 10.0) -> Matrix:
    coeffs = dct_2d(image)
    return [[round(v / quality) for v in row] for row in coeffs]


def reconstruct_image(compressed: Matrix, quality: float = 10.0) -> Matrix:
    dequantized = [[v * quality for v in row] for row in compressed]
    return idct_2d(dequantized)