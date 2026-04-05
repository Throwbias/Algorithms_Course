import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fft_analyzer.signal.generators import sine_wave, multi_tone
from fft_analyzer.signal.filters import low_pass_filter
from fft_analyzer.signal.analysis import peak_frequency

signal = multi_tone([50, 200], sample_rate=1000, duration=1.0)

print("Original peak:", peak_frequency(signal, 1000))

filtered = low_pass_filter(signal, cutoff_ratio=0.1)

print("Filtered peak:", peak_frequency(filtered, 1000))