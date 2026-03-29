from src.strings.plagiarism import plagiarism_similarity, longest_common_substring


def test_longest_common_substring_basic():
    text1 = "the quick brown fox"
    text2 = "quick brown dog"

    result = longest_common_substring(text1, text2)
    assert "quick brown" in result


def test_plagiarism_similarity_identical_text():
    text = "this is a short sample document for testing plagiarism"
    result = plagiarism_similarity(text, text, shingle_size=3)

    assert result["similarity_score"] == 1.0
    assert result["shared_shingles"] == result["total_shingles_doc1"]


def test_plagiarism_similarity_partial_overlap():
    text1 = "machine learning models are useful for pattern recognition"
    text2 = "deep learning models are powerful for pattern recognition tasks"

    result = plagiarism_similarity(text1, text2, shingle_size=2)

    assert 0.0 < result["similarity_score"] < 1.0
    assert len(result["longest_common_substring"]) > 0