import os

from fft_analyzer.visualization.plots import (
    plot_signal,
    plot_spectrum,
    plot_spectrogram_like,
    plot_matrix_heatmap,
)
from fft_analyzer.signal.generators import sine_wave


def test_plot_signal_creates_file():
    output = "tests/_artifacts/test_signal.png"
    plot_signal([0, 1, 0, -1], output)
    assert os.path.exists(output)


def test_plot_spectrum_creates_file():
    output = "tests/_artifacts/test_spectrum.png"
    signal = sine_wave(freq=10, sample_rate=128, duration=1.0)
    plot_spectrum(signal, output)
    assert os.path.exists(output)


def test_plot_spectrogram_like_creates_file():
    output = "tests/_artifacts/test_spectrogram.png"
    signal = sine_wave(freq=10, sample_rate=128, duration=2.0)
    plot_spectrogram_like(signal, output, window_size=64, hop_size=32)
    assert os.path.exists(output)


def test_plot_matrix_heatmap_creates_file():
    output = "tests/_artifacts/test_heatmap.png"
    matrix = [[1, 2], [3, 4]]
    plot_matrix_heatmap(matrix, output)
    assert os.path.exists(output)