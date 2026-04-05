from fft_analyzer.applications.audio_processor import AudioProcessor
from fft_analyzer.applications.image_processor import ImageProcessor
from fft_analyzer.applications.data_analyzer import DataAnalyzer
from fft_analyzer.signal.generators import multi_tone


def test_audio_processor_summary():
    signal = multi_tone([50, 120], sample_rate=1000, duration=1.0)
    processor = AudioProcessor(signal, 1000)
    summary = processor.summary()

    assert summary["sample_rate"] == 1000
    assert summary["length"] == 1000
    assert summary["spectrum_size"] > 0


def test_image_processor_shapes():
    image = [
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 10.0, 10.0, 0.0],
        [0.0, 10.0, 10.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
    ]
    processor = ImageProcessor(image)

    blurred = processor.blur()
    edges = processor.edges()
    recon = processor.reconstruct(quality=10.0)

    assert len(blurred) == 4
    assert len(edges) == 4
    assert len(recon) == 4
    assert processor.summary()["rows"] == 4


def test_data_analyzer_smoothing_length():
    series = [1, 2, 3, 4, 5, 6]
    analyzer = DataAnalyzer(series, sample_rate=10)

    smoothed = analyzer.smooth(window_size=3)
    assert len(smoothed) == len(series)

    auto = analyzer.autocorrelation()
    assert len(auto) == len(series)