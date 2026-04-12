class FenwickTree:
    def __init__(self, size_or_arr):
        if isinstance(size_or_arr, int):
            self.n = size_or_arr
            self.tree = [0] * (self.n + 1)
        else:
            arr = size_or_arr
            self.n = len(arr)
            self.tree = [0] * (self.n + 1)
            for i, value in enumerate(arr):
                self.update(i, value)

    def update(self, index, delta):
        i = index + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix_sum(self, index):
        result = 0
        i = index + 1
        while i > 0:
            result += self.tree[i]
            i -= i & -i
        return result

    def range_sum(self, left, right):
        if left > right:
            return 0
        if left == 0:
            return self.prefix_sum(right)
        return self.prefix_sum(right) - self.prefix_sum(left - 1)