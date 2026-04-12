class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self._build(arr, 0, 0, self.n - 1)

    def _build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            left = 2 * node + 1
            right = 2 * node + 2

            self._build(arr, left, start, mid)
            self._build(arr, right, mid + 1, end)

            self.tree[node] = self.tree[left] + self.tree[right]

    def _push(self, node, start, end):
        if self.lazy[node] != 0:
            # apply pending update
            self.tree[node] += (end - start + 1) * self.lazy[node]

            if start != end:
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]

            self.lazy[node] = 0

    def range_update(self, l, r, val):
        self._range_update(0, 0, self.n - 1, l, r, val)

    def _range_update(self, node, start, end, l, r, val):
        self._push(node, start, end)

        if r < start or end < l:
            return

        if l <= start and end <= r:
            self.lazy[node] += val
            self._push(node, start, end)
            return

        mid = (start + end) // 2
        self._range_update(2 * node + 1, start, mid, l, r, val)
        self._range_update(2 * node + 2, mid + 1, end, l, r, val)

        self.tree[node] = (
            self.tree[2 * node + 1] +
            self.tree[2 * node + 2]
        )

    def query(self, l, r):
        return self._query(0, 0, self.n - 1, l, r)

    def _query(self, node, start, end, l, r):
        self._push(node, start, end)

        if r < start or end < l:
            return 0

        if l <= start and end <= r:
            return self.tree[node]

        mid = (start + end) // 2
        left = self._query(2 * node + 1, start, mid, l, r)
        right = self._query(2 * node + 2, mid + 1, end, l, r)

        return left + right