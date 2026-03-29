import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.strings.suffix_tree import CompressedSuffixTree

text = "banana"
pattern = "ana"

tree = CompressedSuffixTree(text)

print("Suffix Tree Demo")
print("----------------")
print("Text:", text)
print("Pattern:", pattern)
print("Matches:", tree.search(pattern))
print("Longest repeated substring:", tree.longest_repeated_substring())
print("Distinct substrings:", tree.count_distinct_substrings())
print("Edges:")
for edge in tree.edge_list():
    print(edge)