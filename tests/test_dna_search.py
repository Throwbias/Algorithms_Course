from src.strings.dna_search import DNASearchEngine, validate_dna_sequence


def test_validate_dna_sequence_accepts_valid_input():
    validate_dna_sequence("ACGTACGT")


def test_validate_dna_sequence_rejects_invalid_input():
    try:
        validate_dna_sequence("ACGTX")
        assert False, "Expected ValueError for invalid DNA sequence"
    except ValueError:
        assert True


def test_dna_search_engine_finds_pattern():
    engine = DNASearchEngine("ACGTACGTACGT")
    result = engine.find_gene("ACG", method="sa")

    assert result["matches"] == [0, 4, 8]
    assert result["match_count"] == 3


def test_dna_search_engine_batch_search():
    engine = DNASearchEngine("ACGTACGTACGT")
    results = engine.find_many(["ACG", "CGT"], method="kmp")

    assert results["ACG"]["matches"] == [0, 4, 8]
    assert results["CGT"]["matches"] == [1, 5, 9]