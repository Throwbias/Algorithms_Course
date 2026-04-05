from fft_analyzer.core.fft import (
    fft_recursive,
    ifft_recursive,
    circular_convolution,
    linear_convolution,
)


def approx_equal(a, b, tol=1e-6):
    return abs(a - b) < tol


def test_fft_ifft_round_trip():
    x = [0, 1, 2, 3]
    X = fft_recursive([complex(v) for v in x])
    x_back = ifft_recursive(X)

    for original, recovered in zip(x, x_back):
        assert approx_equal(original, recovered.real)


def test_fft_known_small_case():
    x = [1, 0, 0, 0]
    X = fft_recursive([complex(v) for v in x])

    for value in X:
        assert approx_equal(value.real, 1.0)
        assert approx_equal(value.imag, 0.0)


def test_circular_convolution_small():
    x = [1, 2, 0, 0]
    y = [1, 1, 0, 0]
    result = circular_convolution(x, y)

    expected = [1, 3, 2, 0]
    for a, b in zip(result, expected):
        assert approx_equal(a.real, b)


def test_linear_convolution_small():
    x = [1, 2, 3]
    y = [4, 5]
    result = linear_convolution(x, y)

    expected = [4, 13, 22, 15]
    for a, b in zip(result, expected):
        assert approx_equal(a, b)


def test_fft_requires_power_of_two():
    try:
        fft_recursive([1, 2, 3])
        assert False, "Expected ValueError for non-power-of-two input"
    except ValueError:
        assert True