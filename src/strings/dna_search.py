"""
DNA sequence search application.

Uses the unified string search engine for exact pattern matching over DNA strings.
Supports:
- validation of DNA alphabet
- exact gene / motif search
- batch query search
"""

from typing import Dict, List, Any

from src.strings.search_engine import StringSearchEngine


VALID_DNA_CHARS = {"A", "C", "G", "T"}


def validate_dna_sequence(sequence: str) -> None:
    """
    Validate that a sequence contains only A, C, G, T.
    """
    invalid = set(sequence.upper()) - VALID_DNA_CHARS
    if invalid:
        raise ValueError(f"Invalid DNA characters found: {sorted(invalid)}")


class DNASearchEngine:
    """
    DNA-specific wrapper around StringSearchEngine.
    """

    def __init__(self, genome: str):
        genome = genome.upper()
        validate_dna_sequence(genome)
        self.genome = genome
        self.engine = StringSearchEngine(genome)

    def find_gene(self, pattern: str, method: str = "sa") -> Dict[str, Any]:
        """
        Find all exact occurrences of a DNA pattern.

        Args:
            pattern: DNA substring
            method: kmp, rk, sa, or tree

        Returns:
            search result dictionary
        """
        pattern = pattern.upper()
        validate_dna_sequence(pattern)
        return self.engine.find(pattern, method=method)

    def find_many(self, patterns: List[str], method: str = "sa") -> Dict[str, Dict[str, Any]]:
        """
        Search for multiple DNA patterns.
        """
        results = {}
        for pattern in patterns:
            results[pattern] = self.find_gene(pattern, method=method)
        return results