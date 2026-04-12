from advds.trees.segment_tree import SegmentTree
from advds.trees.fenwick_tree import FenwickTree
from advds.trees.persistent_tree import PersistentSegmentTree


class RangeQueryEngine:
    def __init__(self, arr):
        self.arr = list(arr)
        self.segment_tree = SegmentTree(self.arr)
        self.fenwick_tree = FenwickTree(self.arr)
        self.persistent_tree = PersistentSegmentTree(self.arr)

    def range_sum_segment(self, left, right):
        return self.segment_tree.query(left, right)

    def range_sum_fenwick(self, left, right):
        return self.fenwick_tree.range_sum(left, right)

    def point_update(self, index, new_value):
        delta = new_value - self.arr[index]
        self.arr[index] = new_value

        # update segment tree
        try:
            self.segment_tree.update(index, new_value)
        except AttributeError:
            current_value = self.segment_tree.query(index, index)
            self.segment_tree.range_update(index, index, new_value - current_value)

        # update fenwick tree
        self.fenwick_tree.update(index, delta)

        # create new persistent version based on latest version
        latest_version = len(self.persistent_tree.versions) - 1
        return self.persistent_tree.update(latest_version, index, new_value)

    def time_travel_sum(self, version, left, right):
        return self.persistent_tree.query(version, left, right)

    def range_min(self, left, right):
        return min(self.arr[left:right + 1])

    def range_max(self, left, right):
        return max(self.arr[left:right + 1])