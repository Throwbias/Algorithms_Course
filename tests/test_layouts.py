from advds.cache_oblivious.layouts import (
    build_balanced_bst,
    inorder_values,
    level_order_layout,
    veb_layout,
    path_to_value,
    path_memory_cost,
    compare_locality,
)


def test_build_balanced_bst_inorder():
    values = [1, 2, 3, 4, 5, 6, 7]
    root = build_balanced_bst(values)

    assert inorder_values(root) == values


def test_level_order_layout_contains_all_values():
    values = [1, 2, 3, 4, 5, 6, 7]
    root = build_balanced_bst(values)

    layout = level_order_layout(root)
    assert sorted(layout) == values
    assert len(layout) == len(values)


def test_veb_layout_contains_all_values():
    values = [1, 2, 3, 4, 5, 6, 7]
    root = build_balanced_bst(values)

    layout = veb_layout(root)
    assert sorted(layout) == values
    assert len(layout) == len(values)


def test_path_to_value():
    values = [1, 2, 3, 4, 5, 6, 7]
    root = build_balanced_bst(values)

    assert path_to_value(root, 1) == [4, 2, 1]
    assert path_to_value(root, 7) == [4, 6, 7]
    assert path_to_value(root, 4) == [4]


def test_path_memory_cost_nonnegative():
    layout = [4, 2, 1, 3, 6, 5, 7]
    path = [4, 2, 1]

    cost = path_memory_cost(layout, path)
    assert cost >= 0


def test_compare_locality_runs():
    values = list(range(1, 16))
    root = build_balanced_bst(values)

    result = compare_locality(root, [1, 4, 8, 12, 15])

    assert "level_order_layout" in result
    assert "veb_layout" in result
    assert "average_level_order_cost" in result
    assert "average_veb_cost" in result

    assert sorted(result["level_order_layout"]) == values
    assert sorted(result["veb_layout"]) == values