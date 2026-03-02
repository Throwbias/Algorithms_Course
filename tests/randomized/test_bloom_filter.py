from src.randomized.bloom_filter import BloomFilter


def test_bloom_basic_add_check():
    bf = BloomFilter(m_bits=10_000, k_hashes=7)
    items = ["apple", "banana", "carrot", "donut"]

    for x in items:
        bf.add(x)

    for x in items:
        assert bf.check(x) is True

    # This *could* be a false positive, but with 10k bits and 4 items, extremely unlikely.
    assert bf.check("not-in-set-xyz") is False


def test_bloom_theoretical_fp_rate_decreases_with_more_bits():
    bf_small = BloomFilter(m_bits=1_000, k_hashes=7)
    bf_big = BloomFilter(m_bits=10_000, k_hashes=7)

    n = 500
    assert bf_big.estimated_false_positive_rate(n) < bf_small.estimated_false_positive_rate(n)


def test_invalid_params():
    try:
        BloomFilter(m_bits=0, k_hashes=3)
        assert False, "should have raised"
    except ValueError:
        pass

    try:
        BloomFilter(m_bits=100, k_hashes=0)
        assert False, "should have raised"
    except ValueError:
        pass