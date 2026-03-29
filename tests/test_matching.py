from src.flow.applications.matching import bipartite_matching


def test_bipartite_matching_perfect_matching():
    left = ["L1", "L2", "L3"]
    right = ["R1", "R2", "R3"]
    edges = [
        ("L1", "R1"),
        ("L1", "R2"),
        ("L2", "R2"),
        ("L2", "R3"),
        ("L3", "R1"),
        ("L3", "R3"),
    ]

    result = bipartite_matching(left, right, edges, solver="ek")

    assert result["matching_size"] == 3
    assert len(result["matching_pairs"]) == 3

    matched_left = {u for u, _ in result["matching_pairs"]}
    matched_right = {v for _, v in result["matching_pairs"]}

    assert len(matched_left) == 3
    assert len(matched_right) == 3


def test_bipartite_matching_nonperfect_matching():
    left = ["A", "B", "C"]
    right = ["X", "Y"]
    edges = [
        ("A", "X"),
        ("B", "X"),
        ("C", "Y"),
    ]

    result = bipartite_matching(left, right, edges, solver="ek")

    assert result["matching_size"] == 2
    assert len(result["matching_pairs"]) == 2


def test_bipartite_matching_matches_push_relabel():
    left = ["L1", "L2", "L3"]
    right = ["R1", "R2", "R3"]
    edges = [
        ("L1", "R1"),
        ("L1", "R2"),
        ("L2", "R2"),
        ("L2", "R3"),
        ("L3", "R1"),
    ]

    result_ek = bipartite_matching(left, right, edges, solver="ek")
    result_pr = bipartite_matching(left, right, edges, solver="pr")

    assert result_ek["matching_size"] == result_pr["matching_size"]


def test_bipartite_matching_rejects_bad_input():
    left = ["L1", "L2"]
    right = ["R1", "R2"]
    edges = [("L1", "R1"), ("BAD", "R2")]

    try:
        bipartite_matching(left, right, edges, solver="ek")
        assert False, "Expected ValueError for invalid edge"
    except ValueError:
        assert True