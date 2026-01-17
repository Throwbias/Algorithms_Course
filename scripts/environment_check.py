import sys
import importlib
from pathlib import Path

REQUIRED_PACKAGES = ["numpy", "matplotlib", "pandas", "pytest"]

def check_python():
    print(f"Python version: {sys.version}")
    assert sys.version_info >= (3, 10), "Python 3.10+ is required"

def check_packages():
    for pkg in REQUIRED_PACKAGES:
        importlib.import_module(pkg)
    print("All required packages installed")

def check_structure():
    required_dirs = [
        "src/sorting",
        "benchmarks/results",
        "tests",
        "reports",
    ]
    for d in required_dirs:
        assert Path(d).exists(), f"Missing directory: {d}"
    print("Project structure verified")

def check_tests():
    print("Test framework available")

if __name__ == "__main__":
    check_python()
    check_packages()
    check_structure()
    check_tests()
    print("✅ Environment check PASSED")
