from advds.succinct.wavelet_tree import WaveletTree


def test_wavelet_tree_frequency_numeric():
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    wt = WaveletTree(data)

    assert wt.frequency(1, 0, 8) == 2
    assert wt.frequency(5, 0, 8) == 2
    assert wt.frequency(4, 2, 4) == 1
    assert wt.frequency(7, 0, 8) == 0


def test_wavelet_tree_rank():
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    wt = WaveletTree(data)

    assert wt.rank(1, 0) == 0
    assert wt.rank(1, 1) == 1
    assert wt.rank(1, 3) == 2
    assert wt.rank(5, 8) == 2


def test_wavelet_tree_quantile():
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    wt = WaveletTree(data)

    assert wt.quantile(0, 4, 1) == 1
    assert wt.quantile(0, 4, 2) == 1
    assert wt.quantile(0, 4, 3) == 3
    assert wt.quantile(0, 4, 5) == 5


def test_wavelet_tree_dna_symbols():
    data = list("ACGTAGCTA")
    wt = WaveletTree(data)

    assert wt.frequency("A", 0, 8) == 3
    assert wt.frequency("C", 0, 8) == 2
    assert wt.frequency("G", 0, 8) == 2
    assert wt.frequency("T", 0, 8) == 2


def test_wavelet_tree_invalid_quantile():
    data = [1, 2, 3]
    wt = WaveletTree(data)

    try:
        wt.quantile(0, 2, 4)
        assert False, "Expected ValueError"
    except ValueError:
        assert True