import pytest
from src.structures.heap import BinaryHeap, PriorityQueue


# -------------------- MIN HEAP TESTS --------------------
def test_min_heap_insert_and_extract():
    heap = BinaryHeap(is_min_heap=True)
    values = [5, 3, 8, 1, 2]
    
    for v in values:
        heap.insert(v)
    
    sorted_values = []
    while not heap.is_empty():
        sorted_values.append(heap.extract_min())
    
    assert sorted_values == sorted(values), "Min-Heap extraction should be sorted ascending"


def test_min_heap_peek():
    heap = BinaryHeap(is_min_heap=True)
    heap.insert(10)
    heap.insert(5)
    assert heap.peek() == 5, "Peek should return min element"
    heap.extract_min()
    assert heap.peek() == 10, "Peek should update after extraction"


# -------------------- MAX HEAP TESTS --------------------
def test_max_heap_insert_and_extract():
    heap = BinaryHeap(is_min_heap=False)
    values = [5, 3, 8, 1, 2]
    
    for v in values:
        heap.insert(v)
    
    sorted_values = []
    while not heap.is_empty():
        sorted_values.append(heap.extract_max())
    
    assert sorted_values == sorted(values, reverse=True), "Max-Heap extraction should be sorted descending"


def test_max_heap_peek():
    heap = BinaryHeap(is_min_heap=False)
    heap.insert(10)
    heap.insert(20)
    assert heap.peek() == 20, "Peek should return max element"
    heap.extract_max()
    assert heap.peek() == 10, "Peek should update after extraction"


# -------------------- PRIORITY QUEUE TESTS --------------------
def test_priority_queue_min():
    pq = PriorityQueue(min_heap=True)
    for v in [7, 2, 9, 1]:
        pq.enqueue(v)

    results = []
    while not pq.is_empty():
        results.append(pq.dequeue())
    
    assert results == [1, 2, 7, 9], "PriorityQueue (min) should dequeue in ascending order"


def test_priority_queue_max():
    pq = PriorityQueue(min_heap=False)
    for v in [7, 2, 9, 1]:
        pq.enqueue(v)

    results = []
    while not pq.is_empty():
        results.append(pq.dequeue())
    
    assert results == [9, 7, 2, 1], "PriorityQueue (max) should dequeue in descending order"


# -------------------- EDGE CASE TESTS --------------------
def test_empty_heap_peek_and_extract():
    heap = BinaryHeap()
    assert heap.peek() is None
    with pytest.raises(IndexError):
        heap.extract_min()
