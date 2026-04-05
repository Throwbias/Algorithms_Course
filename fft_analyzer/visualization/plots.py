import matplotlib
matplotlib.use("Agg")  # ✅ FIX: non-GUI backend (required for tests)

import matplotlib.pyplot as plt
from typing import List
import os

from fft_analyzer.signal.analysis import magnitude_spectrum


def _ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def plot_signal(signal: List[float], output_path: str, title: str = "Signal") -> None:
    _ensure_parent_dir(output_path)

    plt.figure(figsize=(10, 4))
    plt.plot(signal)
    plt.title(title)
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_spectrum(signal: List[float], output_path: str, title: str = "Magnitude Spectrum") -> None:
    _ensure_parent_dir(output_path)

    spectrum = magnitude_spectrum(signal)

    plt.figure(figsize=(10, 4))
    plt.plot(spectrum)
    plt.title(title)
    plt.xlabel("Frequency Bin")
    plt.ylabel("Magnitude")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_spectrogram_like(
    signal: List[float],
    output_path: str,
    window_size: int = 64,
    hop_size: int = 32,
    title: str = "Spectrogram",
) -> None:
    _ensure_parent_dir(output_path)

    if window_size <= 0 or hop_size <= 0:
        raise ValueError("window_size and hop_size must be positive")
    if len(signal) < window_size:
        raise ValueError("signal must be at least as long as window_size")

    frames = []
    for start in range(0, len(signal) - window_size + 1, hop_size):
        window = signal[start:start + window_size]
        frames.append(magnitude_spectrum(window))

    plt.figure(figsize=(10, 4))
    plt.imshow(frames, aspect="auto", origin="lower")
    plt.title(title)
    plt.xlabel("Frequency Bin")
    plt.ylabel("Frame")
    plt.colorbar(label="Magnitude")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_matrix_heatmap(matrix: List[List[float]], output_path: str, title: str = "Matrix Heatmap") -> None:
    _ensure_parent_dir(output_path)

    plt.figure(figsize=(6, 5))
    plt.imshow(matrix, aspect="auto")
    plt.title(title)
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()