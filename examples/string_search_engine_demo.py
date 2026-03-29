import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.strings.search_engine import StringSearchEngine


text = "banana bandana banana"
pattern = "ana"

engine = StringSearchEngine(text)

print("Search Engine Demo")
print("------------------")
print("Text:", text)
print("Pattern:", pattern)

for method in ["kmp", "rk", "sa"]:
    result = engine.find(pattern, method=method)
    print(f"\nMethod: {method}")
    print("Matches:", result["matches"])
    print("Match count:", result["match_count"])
    print("Search time:", result["search_time_sec"])
    print("Preprocessing time:", result["preprocessing_time_sec"])
    print("Recommendation:", result["recommendation"])