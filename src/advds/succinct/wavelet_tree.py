from advds.succinct.bit_vector import BitVector


class WaveletTree:
    def __init__(self, data, alphabet=None):
        self.data = list(data)
        if not self.data:
            self.low = None
            self.high = None
            self.mid = None
            self.bitvector = BitVector([])
            self.left = None
            self.right = None
            self.leaf_value = None
            return

        if alphabet is None:
            alphabet = sorted(set(self.data))

        self.alphabet = alphabet
        self.low = alphabet[0]
        self.high = alphabet[-1]

        if len(alphabet) == 1:
            self.mid = None
            self.bitvector = BitVector([0] * len(self.data))
            self.left = None
            self.right = None
            self.leaf_value = alphabet[0]
            return

        mid_idx = len(alphabet) // 2
        left_alphabet = alphabet[:mid_idx]
        right_alphabet = alphabet[mid_idx:]

        self.mid = left_alphabet[-1]
        bits = []
        left_data = []
        right_data = []

        left_set = set(left_alphabet)

        for x in self.data:
            if x in left_set:
                bits.append(0)
                left_data.append(x)
            else:
                bits.append(1)
                right_data.append(x)

        self.bitvector = BitVector(bits)
        self.left = WaveletTree(left_data, left_alphabet) if left_data else None
        self.right = WaveletTree(right_data, right_alphabet) if right_data else None
        self.leaf_value = None

    def rank(self, char, index):
        """
        Count occurrences of char in positions [0..index], inclusive.
        """
        if not self.data or index < 0:
            return 0

        if index >= len(self.data):
            index = len(self.data) - 1

        if self.leaf_value is not None:
            return index + 1 if char == self.leaf_value else 0

        if char <= self.mid:
            next_index = self.bitvector.rank0(index) - 1
            if self.left is None:
                return 0
            return self.left.rank(char, next_index)
        else:
            next_index = self.bitvector.rank1(index) - 1
            if self.right is None:
                return 0
            return self.right.rank(char, next_index)

    def frequency(self, char, left, right):
        if left > right or not self.data:
            return 0
        return self.rank(char, right) - self.rank(char, left - 1)

    def quantile(self, left, right, k):
        """
        Return the k-th smallest element in data[left:right+1], 1-based.
        """
        if left > right or k <= 0 or k > (right - left + 1):
            raise ValueError("Invalid range or k")

        return self._quantile(left, right, k)

    def _quantile(self, left, right, k):
        if self.leaf_value is not None:
            return self.leaf_value

        left_before = self.bitvector.rank0(left - 1)
        left_total = self.bitvector.rank0(right) - left_before

        if k <= left_total:
            new_left = left_before
            new_right = self.bitvector.rank0(right) - 1
            return self.left._quantile(new_left, new_right, k)
        else:
            right_before = self.bitvector.rank1(left - 1)
            new_left = right_before
            new_right = self.bitvector.rank1(right) - 1
            return self.right._quantile(new_left, new_right, k - left_total)