"""Uncertainty helpers for small-sample frequencies."""
from __future__ import annotations

from math import sqrt
from typing import Dict, Tuple


def wilson_interval(successes: int, n: int, z: float = 1.96) -> Tuple[float, float]:
    """Wilson score interval for a binomial proportion. Returns (low, high)."""
    if n <= 0:
        return (0.0, 1.0)
    if successes < 0 or successes > n:
        raise ValueError("successes must be in [0, n]")
    p = successes / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    margin = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    low = max(0.0, (centre - margin) / denom)
    high = min(1.0, (centre + margin) / denom)
    return (low, high)


def sample_quality(n: int) -> Dict[str, object]:
    """Qualitative flag for sample size — not a statistical test of edge."""
    if n < 10:
        level = "very_low"
        note = "n<10: frequency is unstable; do not treat as probability"
    elif n < 30:
        level = "low"
        note = "n<30: wide uncertainty; report interval"
    elif n < 100:
        level = "moderate"
        note = "n<100: usable for research, still not a calibrated edge"
    else:
        level = "adequate_for_research"
        note = "Large sample for descriptive research; still not a guarantee"
    return {"n": n, "quality": level, "note": note}
