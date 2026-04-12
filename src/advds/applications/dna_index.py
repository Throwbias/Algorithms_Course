from advds.succinct.wavelet_tree import WaveletTree


class DNAIndex:
    def __init__(self, sequence):
        self.sequence = list(sequence)
        self.wavelet_tree = WaveletTree(self.sequence)

    def range_count(self, nucleotide, left, right):
        return self.wavelet_tree.frequency(nucleotide, left, right)

    def kth_smallest(self, left, right, k):
        return self.wavelet_tree.quantile(left, right, k)

    def pattern_frequency(self, pattern):
        pattern = list(pattern)
        m = len(pattern)
        n = len(self.sequence)

        if m == 0 or m > n:
            return 0

        count = 0
        for i in range(n - m + 1):
            if self.sequence[i:i + m] == pattern:
                count += 1
        return count