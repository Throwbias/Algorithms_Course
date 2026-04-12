from advds.cache_oblivious.matrix_ops import (
    naive_transpose,
    cache_oblivious_transpose,
    naive_multiply,
    cache_oblivious_multiply,
)


def test_transpose_square_matrix():
    matrix = [
        [1, 2],
        [3, 4],
    ]

    expected = [
        [1, 3],
        [2, 4],
    ]

    assert naive_transpose(matrix) == expected
    assert cache_oblivious_transpose(matrix) == expected


def test_transpose_rectangular_matrix():
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
    ]

    expected = [
        [1, 4],
        [2, 5],
        [3, 6],
    ]

    assert naive_transpose(matrix) == expected
    assert cache_oblivious_transpose(matrix) == expected


def test_multiply_2x2():
    a = [
        [1, 2],
        [3, 4],
    ]
    b = [
        [5, 6],
        [7, 8],
    ]

    expected = [
        [19, 22],
        [43, 50],
    ]

    assert naive_multiply(a, b) == expected
    assert cache_oblivious_multiply(a, b) == expected


def test_multiply_4x4():
    a = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]
    b = [
        [16, 15, 14, 13],
        [12, 11, 10, 9],
        [8, 7, 6, 5],
        [4, 3, 2, 1],
    ]

    assert cache_oblivious_multiply(a, b) == naive_multiply(a, b)


def test_multiply_fallback_non_power_of_two():
    a = [
        [1, 2, 3],
        [4, 5, 6],
    ]
    b = [
        [7, 8],
        [9, 10],
        [11, 12],
    ]

    expected = naive_multiply(a, b)
    assert cache_oblivious_multiply(a, b) == expected


def test_invalid_multiply_dimensions():
    a = [[1, 2]]
    b = [[1, 2]]

    try:
        naive_multiply(a, b)
        assert False, "Expected ValueError"
    except ValueError:
        assert True

    try:
        cache_oblivious_multiply(a, b)
        assert False, "Expected ValueError"
    except ValueError:
        assert True