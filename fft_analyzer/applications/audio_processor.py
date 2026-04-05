from typing import List, Dict, Any

from fft_analyzer.signal.filters import low_pass_filter, high_pass_filter
from fft_analyzer.signal.analysis import magnitude_spectrum, peak_frequency


class AudioProcessor:
    """
    Minimal functional audio workflow using in-memory signals.
    """

    def __init__(self, signal: List[float], sample_rate: int):
        self.signal = signal
        self.sample_rate = sample_rate

    def apply_low_pass(self, cutoff_ratio: float) -> List[float]:
        return low_pass_filter(self.signal, cutoff_ratio)

    def apply_high_pass(self, cutoff_ratio: float) -> List[float]:
        return high_pass_filter(self.signal, cutoff_ratio)

    def spectrum(self, signal: List[float] = None) -> List[float]:
        if signal is None:
            signal = self.signal
        return magnitude_spectrum(signal)

    def summary(self, signal: List[float] = None) -> Dict[str, Any]:
        if signal is None:
            signal = self.signal
        return {
            "sample_rate": self.sample_rate,
            "length": len(signal),
            "peak_frequency": peak_frequency(signal, self.sample_rate),
            "spectrum_size": len(magnitude_spectrum(signal)),
        }