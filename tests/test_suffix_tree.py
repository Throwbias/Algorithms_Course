from src.strings.suffix_tree import CompressedSuffixTree


def test_suffix_tree_search_single_match():
    tree = CompressedSuffixTree("abracadabra")
    assert tree.search("cad") == [4]


def test_suffix_tree_search_multiple_matches():
    tree = CompressedSuffixTree("banana")
    assert tree.search("ana") == [1, 3]


def test_suffix_tree_search_no_match():
    tree = CompressedSuffixTree("banana")
    assert tree.search("xyz") == []


def test_suffix_tree_empty_pattern():
    tree = CompressedSuffixTree("abc")
    assert tree.search("") == [0, 1, 2, 3]


def test_longest_repeated_substring():
    tree = CompressedSuffixTree("banana")
    assert tree.longest_repeated_substring() == "ana"


def test_count_distinct_substrings():
    tree = CompressedSuffixTree("aba")
    # distinct substrings: a, b, ab, ba, aba
    assert tree.count_distinct_substrings() == 5