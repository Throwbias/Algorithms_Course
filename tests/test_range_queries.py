from advds.applications.range_queries import RangeQueryEngine


def test_range_query_engine_sum_agreement():
    arr = [1, 3, 5, 7, 9]
    engine = RangeQueryEngine(arr)

    assert engine.range_sum_segment(1, 3) == 15
    assert engine.range_sum_fenwick(1, 3) == 15


def test_range_query_engine_point_update():
    arr = [1, 3, 5, 7, 9]
    engine = RangeQueryEngine(arr)

    version = engine.point_update(2, 10)

    assert engine.range_sum_segment(0, 4) == 30
    assert engine.range_sum_fenwick(0, 4) == 30
    assert version == 1


def test_range_query_engine_time_travel():
    arr = [1, 3, 5, 7, 9]
    engine = RangeQueryEngine(arr)

    v1 = engine.point_update(2, 10)  # [1,3,10,7,9]
    v2 = engine.point_update(0, 4)   # [4,3,10,7,9]

    assert engine.time_travel_sum(0, 0, 4) == 25
    assert engine.time_travel_sum(v1, 0, 4) == 30
    assert engine.time_travel_sum(v2, 0, 4) == 33


def test_range_query_engine_min_max():
    arr = [8, 2, 6, 1, 10]
    engine = RangeQueryEngine(arr)

    assert engine.range_min(1, 4) == 1
    assert engine.range_max(1, 4) == 10