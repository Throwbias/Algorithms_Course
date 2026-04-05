from typing import List
from fft_analyzer.core.fft import fft_recursive


def magnitude_spectrum(signal: List[float]) -> List[float]:
    n = 1
    while n < len(signal):
        n <<= 1

    padded = signal + [0.0] * (n - len(signal))
    X = fft_recursive([complex(v) for v in padded])

    return [abs(v) for v in X[: n // 2]]


def peak_frequency(signal: List[float], sample_rate: int) -> float:
    spectrum = magnitude_spectrum(signal)
    peak_index = max(range(len(spectrum)), key=lambda i: spectrum[i])
    return peak_index * sample_rate / (2 * len(spectrum))