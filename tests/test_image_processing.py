from fft_analyzer.image.filters import gaussian_blur_fft, edge_detect_simple
from fft_analyzer.image.compression import dct_2d, idct_2d, compress_image, reconstruct_image


def approx_equal(a, b, tol=1e-5):
    return abs(a - b) < tol


def test_dct_idct_round_trip():
    image = [
        [10.0, 20.0],
        [30.0, 40.0],
    ]
    coeffs = dct_2d(image)
    recon = idct_2d(coeffs)

    for i in range(2):
        for j in range(2):
            assert approx_equal(image[i][j], recon[i][j], tol=1e-4)


def test_compress_reconstruct_shape():
    image = [
        [10.0, 20.0],
        [30.0, 40.0],
    ]
    comp = compress_image(image, quality=10.0)
    recon = reconstruct_image(comp, quality=10.0)
    assert len(recon) == 2
    assert len(recon[0]) == 2


def test_gaussian_blur_fft_shape():
    image = [
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 10.0, 10.0, 0.0],
        [0.0, 10.0, 10.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
    ]
    blurred = gaussian_blur_fft(image, sigma=1.0)
    assert len(blurred) == 4
    assert len(blurred[0]) == 4


def test_edge_detect_simple_shape():
    image = [
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 10.0, 10.0, 0.0],
        [0.0, 10.0, 10.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
    ]
    edges = edge_detect_simple(image)
    assert len(edges) == 4
    assert len(edges[0]) == 4