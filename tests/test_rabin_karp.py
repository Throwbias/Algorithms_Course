from src.strings.rabin_karp import rolling_hash, rabin_karp_search, rabin_karp_search_all


def test_rolling_hash_deterministic():
    assert rolling_hash("hello") == rolling_hash("hello")
    assert rolling_hash("hello") != rolling_hash("world")


def test_rabin_karp_first_match():
    text = "abxabcabcaby"
    pattern = "abcaby"
    assert rabin_karp_search(text, pattern) == 6


def test_rabin_karp_all_matches():
    text = "aaaaa"
    pattern = "aa"
    assert rabin_karp_search_all(text, pattern) == [0, 1, 2, 3]


def test_rabin_karp_pattern_longer_than_text():
    assert rabin_karp_search("abc", "abcdef") == -1
    assert rabin_karp_search_all("abc", "abcdef") == []


def test_rabin_karp_empty_pattern():
    assert rabin_karp_search("abc", "") == 0
    assert rabin_karp_search_all("abc", "") == [0, 1, 2, 3]


def test_rabin_karp_no_match():
    assert rabin_karp_search("abcdefgh", "xyz") == -1
    assert rabin_karp_search_all("abcdefgh", "xyz") == []


def test_rabin_karp_handles_collisions_by_verification():
    text = "abracadabra"
    pattern = "cad"
    # Small modulus increases collision chances, but verification should keep result correct
    assert rabin_karp_search(text, pattern, modulus=5) == 4