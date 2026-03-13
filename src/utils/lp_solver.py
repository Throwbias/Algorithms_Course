"""
Utility helpers for LP-based approximation modules.
Currently minimal because set_cover_lpround.py uses PuLP directly.
"""

try:
    import pulp
except ImportError:
    pulp = None


def pulp_available():
    """Return True if PuLP is installed."""
    return pulp is not None