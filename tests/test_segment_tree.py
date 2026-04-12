from advds.trees.segment_tree import SegmentTree


def test_segment_tree_basic():
    arr = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(arr)

    # full range
    assert st.query(0, 5) == sum(arr)

    # sub range
    assert st.query(1, 3) == 15  # 3 + 5 + 7

    # point update (if you still support it)
    # NOTE: if your lazy version removed update(), you can comment this out
    try:
        st.update(1, 10)
        assert st.query(1, 3) == 22  # 10 + 5 + 7
    except AttributeError:
        pass


def test_segment_tree_single_element():
    arr = [42]
    st = SegmentTree(arr)

    assert st.query(0, 0) == 42

    try:
        st.update(0, 100)
        assert st.query(0, 0) == 100
    except AttributeError:
        pass


def test_segment_tree_lazy():
    arr = [1, 2, 3, 4, 5]
    st = SegmentTree(arr)

    st.range_update(1, 3, 10)  # add 10 to indices 1..3

    # expected array: [1, 12, 13, 14, 5]
    assert st.query(0, 4) == 45
    assert st.query(1, 3) == 39


def test_segment_tree_lazy_multiple_updates():
    arr = [0, 0, 0, 0, 0]
    st = SegmentTree(arr)

    st.range_update(0, 4, 5)
    st.range_update(1, 3, 3)

    # expected array: [5, 8, 8, 8, 5]
    assert st.query(0, 4) == 34
    assert st.query(1, 3) == 24


def test_segment_tree_lazy_edge_cases():
    arr = [1, 1, 1, 1, 1]
    st = SegmentTree(arr)

    # update single element range
    st.range_update(2, 2, 10)
    assert st.query(2, 2) == 11

    # query outside update
    assert st.query(0, 1) == 2