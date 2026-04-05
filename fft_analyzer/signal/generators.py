import math
import random
from typing import List


def sine_wave(freq: float, sample_rate: int, duration: float) -> List[float]:
    n = int(sample_rate * duration)
    return [math.sin(2 * math.pi * freq * t / sample_rate) for t in range(n)]


def multi_tone(freqs: List[float], sample_rate: int, duration: float) -> List[float]:
    n = int(sample_rate * duration)
    signal = [0.0] * n
    for f in freqs:
        for t in range(n):
            signal[t] += math.sin(2 * math.pi * f * t / sample_rate)
    return signal


def white_noise(sample_rate: int, duration: float) -> List[float]:
    n = int(sample_rate * duration)
    return [random.uniform(-1.0, 1.0) for _ in range(n)]