from src.strings.search_engine import StringSearchEngine


def test_search_engine_kmp():
    engine = StringSearchEngine("banana")
    result = engine.find("ana", method="kmp")
    assert result["matches"] == [1, 3]
    assert result["match_count"] == 2
    assert result["method"] == "kmp"


def test_search_engine_rk():
    engine = StringSearchEngine("banana")
    result = engine.find("ana", method="rk")
    assert result["matches"] == [1, 3]
    assert result["match_count"] == 2
    assert result["method"] == "rk"


def test_search_engine_sa():
    engine = StringSearchEngine("banana")
    result = engine.find("ana", method="sa")
    assert result["matches"] == [1, 3]
    assert result["match_count"] == 2
    assert result["method"] == "sa"
    assert engine.suffix_array is not None
    assert engine.lcp_array is not None


def test_search_engine_tree():
    engine = StringSearchEngine("banana")
    result = engine.find("ana", method="tree")
    assert result["matches"] == [1, 3]
    assert result["match_count"] == 2
    assert result["method"] == "tree"
    assert engine.suffix_tree is not None


def test_search_engine_invalid_method():
    engine = StringSearchEngine("banana")
    try:
        engine.find("ana", method="bad")
        assert False
    except ValueError:
        assert True


def test_search_engine_empty_pattern():
    engine = StringSearchEngine("abc")
    result = engine.find("", method="kmp")
    assert result["matches"] == [0, 1, 2, 3]
    assert result["match_count"] == 4


def test_search_engine_recommendation():
    engine = StringSearchEngine("banana")
    rec = engine.recommend("tree")
    assert "Suffix Trees" in rec