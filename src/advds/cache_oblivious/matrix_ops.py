def naive_transpose(matrix):
    if not matrix or not matrix[0]:
        return []

    rows = len(matrix)
    cols = len(matrix[0])
    return [[matrix[r][c] for r in range(rows)] for c in range(cols)]


def cache_oblivious_transpose(matrix):
    if not matrix or not matrix[0]:
        return []

    rows = len(matrix)
    cols = len(matrix[0])
    result = [[0 for _ in range(rows)] for _ in range(cols)]

    def transpose_rec(r0, r1, c0, c1):
        if r0 >= r1 or c0 >= c1:
            return

        if (r1 - r0) <= 2 and (c1 - c0) <= 2:
            for i in range(r0, r1):
                for j in range(c0, c1):
                    result[j][i] = matrix[i][j]
            return

        if (r1 - r0) >= (c1 - c0):
            rm = (r0 + r1) // 2
            transpose_rec(r0, rm, c0, c1)
            transpose_rec(rm, r1, c0, c1)
        else:
            cm = (c0 + c1) // 2
            transpose_rec(r0, r1, c0, cm)
            transpose_rec(r0, r1, cm, c1)

    transpose_rec(0, rows, 0, cols)
    return result


def naive_multiply(a, b):
    if not a or not b or not a[0] or not b[0]:
        return []

    a_rows = len(a)
    a_cols = len(a[0])
    b_rows = len(b)
    b_cols = len(b[0])

    if a_cols != b_rows:
        raise ValueError("Incompatible matrix dimensions for multiplication")

    result = [[0 for _ in range(b_cols)] for _ in range(a_rows)]

    for i in range(a_rows):
        for k in range(a_cols):
            for j in range(b_cols):
                result[i][j] += a[i][k] * b[k][j]

    return result


def cache_oblivious_multiply(a, b):
    if not a or not b or not a[0] or not b[0]:
        return []

    a_rows = len(a)
    a_cols = len(a[0])
    b_rows = len(b)
    b_cols = len(b[0])

    if a_cols != b_rows:
        raise ValueError("Incompatible matrix dimensions for multiplication")

    if not _is_power_of_two(a_rows) or not _is_power_of_two(a_cols) or not _is_power_of_two(b_cols):
        return naive_multiply(a, b)

    result = [[0 for _ in range(b_cols)] for _ in range(a_rows)]
    _multiply_rec(a, b, result, 0, 0, 0, 0, 0, 0, a_rows)
    return result


def _multiply_rec(a, b, c, ar, ac, br, bc, cr, cc, size):
    if size == 1:
        c[cr][cc] += a[ar][ac] * b[br][bc]
        return

    half = size // 2

    # C11 = A11*B11 + A12*B21
    _multiply_rec(a, b, c, ar, ac, br, bc, cr, cc, half)
    _multiply_rec(a, b, c, ar, ac + half, br + half, bc, cr, cc, half)

    # C12 = A11*B12 + A12*B22
    _multiply_rec(a, b, c, ar, ac, br, bc + half, cr, cc + half, half)
    _multiply_rec(a, b, c, ar, ac + half, br + half, bc + half, cr, cc + half, half)

    # C21 = A21*B11 + A22*B21
    _multiply_rec(a, b, c, ar + half, ac, br, bc, cr + half, cc, half)
    _multiply_rec(a, b, c, ar + half, ac + half, br + half, bc, cr + half, cc, half)

    # C22 = A21*B12 + A22*B22
    _multiply_rec(a, b, c, ar + half, ac, br, bc + half, cr + half, cc + half, half)
    _multiply_rec(a, b, c, ar + half, ac + half, br + half, bc + half, cr + half, cc + half, half)


def _is_power_of_two(x):
    return x > 0 and (x & (x - 1)) == 0