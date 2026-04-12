from advds.trees.persistent_tree import PersistentSegmentTree


def test_persistent_tree_initial_query():
    arr = [1, 2, 3, 4, 5]
    pst = PersistentSegmentTree(arr)

    assert pst.query(0, 0, 4) == 15
    assert pst.query(0, 1, 3) == 9


def test_persistent_tree_single_update_creates_new_version():
    arr = [1, 2, 3, 4, 5]
    pst = PersistentSegmentTree(arr)

    v1 = pst.update(0, 2, 10)  # change index 2 from 3 to 10

    assert pst.query(0, 0, 4) == 15
    assert pst.query(v1, 0, 4) == 22

    # old version unchanged
    assert pst.query(0, 2, 2) == 3
    assert pst.query(v1, 2, 2) == 10


def test_persistent_tree_multiple_versions():
    arr = [1, 2, 3, 4]
    pst = PersistentSegmentTree(arr)

    v1 = pst.update(0, 0, 10)   # [10,2,3,4]
    v2 = pst.update(v1, 3, 20)  # [10,2,3,20]

    assert pst.query(0, 0, 3) == 10
    assert pst.query(v1, 0, 3) == 19
    assert pst.query(v2, 0, 3) == 35

    # verify earlier versions remain intact
    assert pst.query(0, 0, 0) == 1
    assert pst.query(v1, 0, 0) == 10
    assert pst.query(v2, 3, 3) == 20


def test_persistent_tree_subrange_queries():
    arr = [5, 1, 7, 3, 2]
    pst = PersistentSegmentTree(arr)

    v1 = pst.update(0, 1, 10)  # [5,10,7,3,2]

    assert pst.query(0, 1, 3) == 11
    assert pst.query(v1, 1, 3) == 20