from __future__ import annotations

import hashlib
import math
from typing import Iterable


class BloomFilter:
    """
    Bloom filter with:
      - bit array length m_bits
      - k hash functions via double hashing

    Membership check:
      - False => definitely not present
      - True  => possibly present (false positives possible)
    """

    def __init__(self, m_bits: int, k_hashes: int):
        if m_bits <= 0:
            raise ValueError("m_bits must be > 0")
        if k_hashes <= 0:
            raise ValueError("k_hashes must be > 0")

        self.m_bits = int(m_bits)
        self.k_hashes = int(k_hashes)

        self._bytes = bytearray((self.m_bits + 7) // 8)
        self.items_added = 0

    @staticmethod
    def _to_bytes(item) -> bytes:
        if isinstance(item, bytes):
            return item
        if isinstance(item, str):
            return item.encode("utf-8")
        return str(item).encode("utf-8")

    def _hashes(self, item) -> Iterable[int]:
        data = self._to_bytes(item)

        h1 = int.from_bytes(hashlib.sha256(b"bf1:" + data).digest(), "big")
        h2 = int.from_bytes(hashlib.sha256(b"bf2:" + data).digest(), "big")

        # Double hashing: (h1 + i*h2) mod m
        for i in range(self.k_hashes):
            yield (h1 + i * h2) % self.m_bits

    def _set_bit(self, bit_index: int) -> None:
        byte_index = bit_index // 8
        mask = 1 << (bit_index % 8)
        self._bytes[byte_index] |= mask

    def _get_bit(self, bit_index: int) -> int:
        byte_index = bit_index // 8
        mask = 1 << (bit_index % 8)
        return 1 if (self._bytes[byte_index] & mask) else 0

    def add(self, item) -> None:
        for idx in self._hashes(item):
            self._set_bit(idx)
        self.items_added += 1

    def check(self, item) -> bool:
        return all(self._get_bit(idx) for idx in self._hashes(item))

    def union_inplace(self, other: "BloomFilter") -> None:
        if self.m_bits != other.m_bits or self.k_hashes != other.k_hashes:
            raise ValueError("BloomFilters must have same size and k")
        for i in range(len(self._bytes)):
            self._bytes[i] |= other._bytes[i]

    def estimated_false_positive_rate(self, n_inserted: int | None = None) -> float:
        """
        Theoretical approximation:
          p ≈ (1 - e^{-k n / m})^k
        """
        n = self.items_added if n_inserted is None else n_inserted
        m = self.m_bits
        k = self.k_hashes
        return (1.0 - math.exp(-k * n / m)) ** k