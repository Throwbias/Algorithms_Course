from typing import List, Dict, Any

from fft_analyzer.signal.analysis import peak_frequency
from fft_analyzer.core.fft import linear_convolution


class DataAnalyzer:
    """
    Minimal time-series analytics wrapper.
    """

    def __init__(self, series: List[float], sample_rate: int = 1):
        self.series = series
        self.sample_rate = sample_rate

    def detect_periodicity(self) -> float:
        """
        Returns dominant frequency estimate.
        """
        return peak_frequency(self.series, self.sample_rate)

    def smooth(self, window_size: int = 3) -> List[float]:
        if window_size <= 0:
            raise ValueError("window_size must be positive")

        kernel = [1.0 / window_size] * window_size
        smoothed = linear_convolution(self.series, kernel)

        start = (window_size - 1) // 2
        end = start + len(self.series)
        return smoothed[start:end]

    def autocorrelation(self) -> List[float]:
        n = len(self.series)
        result = []
        for lag in range(n):
            value = 0.0
            for i in range(n - lag):
                value += self.series[i] * self.series[i + lag]
            result.append(value)
        return result

    def summary(self) -> Dict[str, Any]:
        return {
            "length": len(self.series),
            "dominant_frequency": self.detect_periodicity(),
        }