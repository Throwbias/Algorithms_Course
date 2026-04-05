import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fft_analyzer.image.filters import gaussian_blur_fft, edge_detect_simple
from fft_analyzer.image.compression import compress_image, reconstruct_image

image = [
    [0.0, 0.0, 0.0, 0.0],
    [0.0, 10.0, 10.0, 0.0],
    [0.0, 10.0, 10.0, 0.0],
    [0.0, 0.0, 0.0, 0.0],
]

print("Blurred:")
for row in gaussian_blur_fft(image, sigma=1.0):
    print(row)

print("\nEdges:")
for row in edge_detect_simple(image):
    print(row)

compressed = compress_image(image, quality=10.0)
print("\nCompressed:")
for row in compressed:
    print(row)

print("\nReconstructed:")
for row in reconstruct_image(compressed, quality=10.0):
    print(row)