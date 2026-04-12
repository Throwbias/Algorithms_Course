class BitVector:
    def __init__(self, bits):
        self.bits = list(bits)
        self.n = len(self.bits)

        if any(bit not in (0, 1) for bit in self.bits):
            raise ValueError("BitVector must contain only 0s and 1s")

        self.prefix_ones = [0] * (self.n + 1)
        for i in range(self.n):
            self.prefix_ones[i + 1] = self.prefix_ones[i] + self.bits[i]

    def __len__(self):
        return self.n

    def access(self, i):
        return self.bits[i]

    def rank1(self, i):
        """
        Number of 1s in bits[0..i], inclusive.
        """
        if i < 0:
            return 0
        if i >= self.n:
            i = self.n - 1
        return self.prefix_ones[i + 1]

    def rank0(self, i):
        """
        Number of 0s in bits[0..i], inclusive.
        """
        if i < 0:
            return 0
        if i >= self.n:
            i = self.n - 1
        return (i + 1) - self.rank1(i)

    def select1(self, k):
        """
        Return the index of the k-th 1, 1-based.
        Example: select1(1) = index of first 1
        """
        if k <= 0 or k > self.prefix_ones[-1]:
            return -1

        lo, hi = 0, self.n - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if self.rank1(mid) >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def select0(self, k):
        """
        Return the index of the k-th 0, 1-based.
        """
        total_zeros = self.n - self.prefix_ones[-1]
        if k <= 0 or k > total_zeros:
            return -1

        lo, hi = 0, self.n - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if self.rank0(mid) >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo