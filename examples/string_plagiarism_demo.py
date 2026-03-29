import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.strings.plagiarism import plagiarism_similarity

doc1 = """
Machine learning models are widely used in modern data analysis and pattern recognition systems.
These methods help identify structure in large datasets.
"""

doc2 = """
Deep learning and machine learning models are widely used in modern pattern recognition systems.
These approaches help identify structure in very large datasets.
"""

result = plagiarism_similarity(doc1, doc2, shingle_size=3)

print("Plagiarism Demo")
print("----------------")
print("Similarity score:", result["similarity_score"])
print("Longest common substring:", result["longest_common_substring"])
print("Shared shingles:", result["shared_shingles"])
print("Doc1 shingles:", result["total_shingles_doc1"])
print("Doc2 shingles:", result["total_shingles_doc2"])