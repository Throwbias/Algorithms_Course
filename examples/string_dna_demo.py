import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.strings.dna_search import DNASearchEngine

genome = "ACGTACGTGACGTTACGTACG"
patterns = ["ACG", "TAC", "GTT"]

engine = DNASearchEngine(genome)

print("DNA Search Demo")
print("---------------")
print("Genome:", genome)

for pattern in patterns:
    result = engine.find_gene(pattern, method="sa")
    print(f"\nPattern: {pattern}")
    print("Matches:", result["matches"])
    print("Count:", result["match_count"])