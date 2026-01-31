from typing import List, Optional, TypeVar, Generic

T = TypeVar("T")


class BinaryHeap(Generic[T]):
    """
    Array-based binary heap (min or max).

    Supports:
    - insert(value)
    - extract_min / extract_max
    - heapify (build_heap)
    - peek
    - is_empty

    Maintains O(log n) insert/extract operations.
    """

    def __init__(self, is_min_heap: bool = True, items: Optional[List[T]] = None):
        self.data: List[T] = []
        self.is_min_heap = is_min_heap
        if items:
            self.data = list(items)
            self.heapify()

    def is_empty(self) -> bool:
        """Check if heap is empty."""
        return len(self.data) == 0

    def peek(self) -> Optional[T]:
        """Return top element without removing it."""
        if self.is_empty():
            return None
        return self.data[0]

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _compare(self, a: T, b: T) -> bool:
        """Compare based on heap type."""
        return a < b if self.is_min_heap else a > b

    def _sift_up(self, i: int):
        """Move element at index i up to restore heap property."""
        parent = self._parent(i)
        if i > 0 and self._compare(self.data[i], self.data[parent]):
            self.data[i], self.data[parent] = self.data[parent], self.data[i]
            self._sift_up(parent)

    def _sift_down(self, i: int):
        """Move element at index i down to restore heap property."""
        left = self._left(i)
        right = self._right(i)
        smallest_or_largest = i

        if left < len(self.data) and self._compare(self.data[left], self.data[smallest_or_largest]):
            smallest_or_largest = left
        if right < len(self.data) and self._compare(self.data[right], self.data[smallest_or_largest]):
            smallest_or_largest = right

        if smallest_or_largest != i:
            self.data[i], self.data[smallest_or_largest] = self.data[smallest_or_largest], self.data[i]
            self._sift_down(smallest_or_largest)

    def insert(self, value: T):
        """Add value to heap (O(log n))."""
        self.data.append(value)
        self._sift_up(len(self.data) - 1)

    def extract(self) -> T:
        """
        Remove and return top element (min or max) in O(log n).
        Raises IndexError if heap is empty.
        """
        if self.is_empty():
            raise IndexError("Heap is empty")
        top = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._sift_down(0)
        return top

    # Convenience aliases
    def extract_min(self) -> T:
        if not self.is_min_heap:
            raise TypeError("This is a max-heap, cannot extract_min")
        return self.extract()

    def extract_max(self) -> T:
        if self.is_min_heap:
            raise TypeError("This is a min-heap, cannot extract_max")
        return self.extract()

    def heapify(self):
        """Convert current array into heap in-place (O(n))."""
        for i in range(len(self.data) // 2 - 1, -1, -1):
            self._sift_down(i)


class PriorityQueue(Generic[T]):
    """
    Priority Queue implemented using BinaryHeap.
    Min-heap by default.
    """

    def __init__(self, min_heap: bool = True):
        self.heap = BinaryHeap(is_min_heap=min_heap)

    def enqueue(self, value: T):
        """Add value to priority queue."""
        self.heap.insert(value)

    def dequeue(self) -> T:
        """Remove and return top-priority element."""
        return self.heap.extract()

    def peek(self) -> Optional[T]:
        """View top-priority element."""
        return self.heap.peek()

    def is_empty(self) -> bool:
        return self.heap.is_empty()
