import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.strings.suffix_array import build_suffix_array, build_lcp_array, suffix_array_search


text = "banana"
pattern = "ana"

sa = build_suffix_array(text)
lcp = build_lcp_array(text, sa)
matches = suffix_array_search(text, pattern, sa)

print("Suffix Array Demo")
print("-----------------")
print("Text:", text)
print("Pattern:", pattern)
print("Suffix Array:", sa)
print("LCP Array:", lcp)
print("Matches:", matches)