from advds.succinct.bit_vector import BitVector
from advds.succinct.rank_select import RankSelect


def test_bit_vector_access_and_length():
    bv = BitVector([1, 0, 1, 1, 0])
    assert len(bv) == 5
    assert bv.access(0) == 1
    assert bv.access(1) == 0
    assert bv.access(4) == 0


def test_rank1():
    bv = BitVector([1, 0, 1, 1, 0])
    assert bv.rank1(0) == 1
    assert bv.rank1(1) == 1
    assert bv.rank1(2) == 2
    assert bv.rank1(4) == 3


def test_rank0():
    bv = BitVector([1, 0, 1, 1, 0])
    assert bv.rank0(0) == 0
    assert bv.rank0(1) == 1
    assert bv.rank0(2) == 1
    assert bv.rank0(4) == 2


def test_select1():
    bv = BitVector([1, 0, 1, 1, 0])
    assert bv.select1(1) == 0
    assert bv.select1(2) == 2
    assert bv.select1(3) == 3
    assert bv.select1(4) == -1


def test_select0():
    bv = BitVector([1, 0, 1, 1, 0])
    assert bv.select0(1) == 1
    assert bv.select0(2) == 4
    assert bv.select0(3) == -1


def test_rank_select_wrapper():
    rs = RankSelect([1, 0, 1, 1, 0])
    assert rs.rank1(4) == 3
    assert rs.rank0(4) == 2
    assert rs.select1(2) == 2
    assert rs.select0(2) == 4


def test_invalid_bit_vector():
    try:
        BitVector([1, 0, 2, 1])
        assert False, "Expected ValueError"
    except ValueError:
        assert True