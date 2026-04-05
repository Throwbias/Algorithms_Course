from fft_analyzer.signal.generators import sine_wave
from fft_analyzer.signal.analysis import peak_frequency
from fft_analyzer.signal.filters import low_pass_filter


def test_sine_wave_frequency_detection():
    signal = sine_wave(freq=50, sample_rate=1000, duration=1.0)
    peak = peak_frequency(signal, sample_rate=1000)
    assert abs(peak - 50) < 2


def test_low_pass_filter_reduces_high_freq():
    signal = sine_wave(200, 1000, 1.0)
    filtered = low_pass_filter(signal, cutoff_ratio=0.05)

    assert sum(abs(x) for x in filtered) < sum(abs(x) for x in signal)