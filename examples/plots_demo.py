import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fft_analyzer.signal.generators import multi_tone
from fft_analyzer.visualization.plots import (
    plot_signal,
    plot_spectrum,
    plot_spectrogram_like,
    plot_matrix_heatmap,
)

signal = multi_tone([20, 60], sample_rate=256, duration=2.0)

plot_signal(signal, "examples/output_signal.png", title="Demo Signal")
plot_spectrum(signal, "examples/output_spectrum.png", title="Demo Spectrum")
plot_spectrogram_like(signal, "examples/output_spectrogram.png", window_size=64, hop_size=32)
plot_matrix_heatmap([[1, 2], [3, 4]], "examples/output_heatmap.png", title="Demo Heatmap")

print("Saved demo plots to examples/")