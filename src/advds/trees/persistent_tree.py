class Node:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class PersistentSegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.versions = [self._build(arr, 0, self.n - 1)]

    def _build(self, arr, start, end):
        if start == end:
            return Node(arr[start])

        mid = (start + end) // 2
        left = self._build(arr, start, mid)
        right = self._build(arr, mid + 1, end)
        return Node(left.value + right.value, left, right)

    def _update(self, node, start, end, idx, value):
        if start == end:
            return Node(value)

        mid = (start + end) // 2

        if idx <= mid:
            new_left = self._update(node.left, start, mid, idx, value)
            new_right = node.right
        else:
            new_left = node.left
            new_right = self._update(node.right, mid + 1, end, idx, value)

        return Node(new_left.value + new_right.value, new_left, new_right)

    def update(self, version, idx, value):
        new_root = self._update(self.versions[version], 0, self.n - 1, idx, value)
        self.versions.append(new_root)
        return len(self.versions) - 1

    def _query(self, node, start, end, left, right):
        if right < start or end < left:
            return 0

        if left <= start and end <= right:
            return node.value

        mid = (start + end) // 2
        return (
            self._query(node.left, start, mid, left, right)
            + self._query(node.right, mid + 1, end, left, right)
        )

    def query(self, version, left, right):
        return self._query(self.versions[version], 0, self.n - 1, left, right)