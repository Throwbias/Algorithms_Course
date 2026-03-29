import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.strings.kmp import compute_lps, kmp_search, kmp_search_all
from src.strings.rabin_karp import rabin_karp_search, rabin_karp_search_all


text = "abxabcabcaby"
pattern = "abcaby"

print("KMP Demo")
print("--------")
print("Text:", text)
print("Pattern:", pattern)
print("LPS:", compute_lps(pattern))
print("First match:", kmp_search(text, pattern))
print("All matches:", kmp_search_all(text, pattern))

print("\nRabin-Karp Demo")
print("----------------")
print("Text:", text)
print("Pattern:", pattern)
print("First match:", rabin_karp_search(text, pattern))
print("All matches:", rabin_karp_search_all(text, pattern))