from advds.succinct.bit_vector import BitVector


class RankSelect:
    def __init__(self, bits):
        self.bit_vector = BitVector(bits)

    def rank1(self, i):
        return self.bit_vector.rank1(i)

    def rank0(self, i):
        return self.bit_vector.rank0(i)

    def select1(self, k):
        return self.bit_vector.select1(k)

    def select0(self, k):
        return self.bit_vector.select0(k)

    def access(self, i):
        return self.bit_vector.access(i)