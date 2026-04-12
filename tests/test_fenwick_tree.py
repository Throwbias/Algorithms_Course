from advds.trees.fenwick_tree import FenwickTree


def test_fenwick_tree_build_from_array():
    arr = [1, 2, 3, 4, 5]
    ft = FenwickTree(arr)

    assert ft.prefix_sum(0) == 1
    assert ft.prefix_sum(2) == 6
    assert ft.prefix_sum(4) == 15


def test_fenwick_tree_range_sum():
    arr = [1, 2, 3, 4, 5]
    ft = FenwickTree(arr)

    assert ft.range_sum(0, 4) == 15
    assert ft.range_sum(1, 3) == 9
    assert ft.range_sum(2, 2) == 3


def test_fenwick_tree_updates():
    arr = [1, 2, 3, 4, 5]
    ft = FenwickTree(arr)

    ft.update(2, 10)  # add 10 to index 2
    assert ft.prefix_sum(4) == 25
    assert ft.range_sum(2, 2) == 13
    assert ft.range_sum(1, 3) == 19


def test_fenwick_tree_from_size():
    ft = FenwickTree(5)

    ft.update(0, 5)
    ft.update(3, 7)

    assert ft.prefix_sum(0) == 5
    assert ft.prefix_sum(3) == 12
    assert ft.range_sum(1, 3) == 7