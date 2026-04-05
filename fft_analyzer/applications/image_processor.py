from typing import List, Dict, Any

from fft_analyzer.image.filters import gaussian_blur_fft, edge_detect_simple
from fft_analyzer.image.compression import compress_image, reconstruct_image

Matrix = List[List[float]]


class ImageProcessor:
    """
    Minimal image processing workflow using grayscale 2D arrays.
    """

    def __init__(self, image: Matrix):
        self.image = image

    def blur(self, sigma: float = 1.0) -> Matrix:
        return gaussian_blur_fft(self.image, sigma=sigma)

    def edges(self) -> Matrix:
        return edge_detect_simple(self.image)

    def compress(self, quality: float = 10.0) -> Matrix:
        return compress_image(self.image, quality=quality)

    def reconstruct(self, quality: float = 10.0) -> Matrix:
        compressed = self.compress(quality=quality)
        return reconstruct_image(compressed, quality=quality)

    def summary(self) -> Dict[str, Any]:
        return {
            "rows": len(self.image),
            "cols": len(self.image[0]) if self.image else 0,
        }