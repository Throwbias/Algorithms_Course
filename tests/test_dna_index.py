from advds.applications.dna_index import DNAIndex


def test_dna_range_count():
    dna = DNAIndex("ACGTAGCTA")

    assert dna.range_count("A", 0, 8) == 3
    assert dna.range_count("C", 0, 8) == 2
    assert dna.range_count("G", 0, 8) == 2
    assert dna.range_count("T", 0, 8) == 2


def test_dna_subrange_count():
    dna = DNAIndex("ACGTAGCTA")

    assert dna.range_count("A", 0, 3) == 1
    assert dna.range_count("C", 0, 3) == 1
    assert dna.range_count("T", 4, 8) == 1


def test_dna_kth_smallest():
    dna = DNAIndex("ACGTAGCTA")

    assert dna.kth_smallest(0, 3, 1) == "A"
    assert dna.kth_smallest(0, 3, 2) == "C"
    assert dna.kth_smallest(0, 3, 3) == "G"
    assert dna.kth_smallest(0, 3, 4) == "T"


def test_dna_pattern_frequency():
    dna = DNAIndex("ACGTACGTAC")

    assert dna.pattern_frequency("AC") == 3
    assert dna.pattern_frequency("CG") == 2
    assert dna.pattern_frequency("GT") == 2
    assert dna.pattern_frequency("TT") == 0


def test_dna_empty_or_long_pattern():
    dna = DNAIndex("ACGT")

    assert dna.pattern_frequency("") == 0
    assert dna.pattern_frequency("ACGTA") == 0