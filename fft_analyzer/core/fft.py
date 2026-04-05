"""
Core FFT algorithms for FFTAnalyzer.

Implements the required minimum:
- recursive Cooley-Tukey FFT
- inverse FFT
- circular convolution via FFT
- linear convolution via zero padding

Assumes power-of-two lengths for fft_recursive / ifft_recursive.
"""

from typing import List
import cmath


def _is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def _next_power_of_two(n: int) -> int:
    power = 1
    while power < n:
        power <<= 1
    return power


def fft_recursive(x: List[complex]) -> List[complex]:
    """
    Recursive Cooley-Tukey FFT.
    Input length must be a power of two.
    """
    n = len(x)
    if n == 0:
        return []
    if not _is_power_of_two(n):
        raise ValueError("fft_recursive input length must be a power of two")
    if n == 1:
        return [complex(x[0])]

    even = fft_recursive(x[0::2])
    odd = fft_recursive(x[1::2])

    result = [0j] * n
    for k in range(n // 2):
        twiddle = cmath.exp(-2j * cmath.pi * k / n) * odd[k]
        result[k] = even[k] + twiddle
        result[k + n // 2] = even[k] - twiddle

    return result


def ifft_recursive(X: List[complex]) -> List[complex]:
    """
    Inverse FFT using conjugation trick.
    Input length must be a power of two.
    """
    n = len(X)
    if n == 0:
        return []
    if not _is_power_of_two(n):
        raise ValueError("ifft_recursive input length must be a power of two")

    conjugated = [z.conjugate() for z in X]
    transformed = fft_recursive(conjugated)
    return [z.conjugate() / n for z in transformed]


def circular_convolution(x: List[float], y: List[float]) -> List[complex]:
    """
    Circular convolution of equal-length signals using FFT.
    Length must be equal and power of two.
    """
    if len(x) != len(y):
        raise ValueError("circular convolution inputs must have equal length")
    if not _is_power_of_two(len(x)):
        raise ValueError("circular convolution length must be a power of two")

    X = fft_recursive([complex(v) for v in x])
    Y = fft_recursive([complex(v) for v in y])
    Z = [X[k] * Y[k] for k in range(len(X))]
    return ifft_recursive(Z)


def linear_convolution(x: List[float], y: List[float]) -> List[float]:
    """
    Linear convolution via zero padding + FFT.
    """
    if not x or not y:
        return []

    out_len = len(x) + len(y) - 1
    fft_len = _next_power_of_two(out_len)

    x_pad = [complex(v) for v in x] + [0j] * (fft_len - len(x))
    y_pad = [complex(v) for v in y] + [0j] * (fft_len - len(y))

    X = fft_recursive(x_pad)
    Y = fft_recursive(y_pad)
    Z = [X[k] * Y[k] for k in range(fft_len)]
    conv = ifft_recursive(Z)

    return [conv[i].real for i in range(out_len)]