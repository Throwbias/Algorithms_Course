from src.strings.suffix_array import (
    build_suffix_array,
    build_lcp_array,
    suffix_array_search,
)


def test_build_suffix_array_banana():
    text = "banana"
    sa = build_suffix_array(text)
    assert sa == [5, 3, 1, 0, 4, 2]


def test_build_lcp_array_banana():
    text = "banana"
    sa = build_suffix_array(text)
    lcp = build_lcp_array(text, sa)
    assert lcp == [0, 1, 3, 0, 0, 2]


def test_suffix_array_search_single_match():
    text = "abracadabra"
    sa = build_suffix_array(text)
    matches = suffix_array_search(text, "cad", sa)
    assert matches == [4]


def test_suffix_array_search_multiple_matches():
    text = "banana"
    sa = build_suffix_array(text)
    matches = suffix_array_search(text, "ana", sa)
    assert matches == [1, 3]


def test_suffix_array_search_no_match():
    text = "banana"
    sa = build_suffix_array(text)
    matches = suffix_array_search(text, "xyz", sa)
    assert matches == []


def test_suffix_array_search_empty_pattern():
    text = "banana"
    sa = build_suffix_array(text)
    matches = suffix_array_search(text, "", sa)
    assert matches == [0, 1, 2, 3, 4, 5, 6]


def test_suffix_array_empty_text():
    text = ""
    sa = build_suffix_array(text)
    lcp = build_lcp_array(text, sa)
    assert sa == []
    assert lcp == []