from src.strings.kmp import compute_lps, kmp_search, kmp_search_all


def test_compute_lps_basic():
    pattern = "ababaca"
    assert compute_lps(pattern) == [0, 0, 1, 2, 3, 0, 1]


def test_kmp_first_match():
    text = "abxabcabcaby"
    pattern = "abcaby"
    assert kmp_search(text, pattern) == 6


def test_kmp_all_matches():
    text = "aaaaa"
    pattern = "aa"
    assert kmp_search_all(text, pattern) == [0, 1, 2, 3]


def test_kmp_pattern_longer_than_text():
    assert kmp_search("abc", "abcdef") == -1
    assert kmp_search_all("abc", "abcdef") == []


def test_kmp_empty_pattern():
    assert kmp_search("abc", "") == 0
    assert kmp_search_all("abc", "") == [0, 1, 2, 3]


def test_kmp_no_match():
    assert kmp_search("abcdefgh", "xyz") == -1
    assert kmp_search_all("abcdefgh", "xyz") == []