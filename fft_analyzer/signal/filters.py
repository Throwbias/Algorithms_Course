from typing import List
from fft_analyzer.core.fft import fft_recursive, ifft_recursive
import cmath


def _pad_to_power_of_two(signal: List[float]):
    n = 1
    while n < len(signal):
        n <<= 1
    return signal + [0.0] * (n - len(signal))


def low_pass_filter(signal: List[float], cutoff_ratio: float) -> List[float]:
    """
    cutoff_ratio: 0.0–0.5 (fraction of Nyquist)
    """
    padded = _pad_to_power_of_two(signal)
    n = len(padded)

    X = fft_recursive([complex(v) for v in padded])

    cutoff = int(cutoff_ratio * n)

    for i in range(n):
        if i > cutoff and i < n - cutoff:
            X[i] = 0

    filtered = ifft_recursive(X)
    return [filtered[i].real for i in range(len(signal))]


def high_pass_filter(signal: List[float], cutoff_ratio: float) -> List[float]:
    padded = _pad_to_power_of_two(signal)
    n = len(padded)

    X = fft_recursive([complex(v) for v in padded])

    cutoff = int(cutoff_ratio * n)

    for i in range(n):
        if i <= cutoff or i >= n - cutoff:
            X[i] = 0

    filtered = ifft_recursive(X)
    return [filtered[i].real for i in range(len(signal))]