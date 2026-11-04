"""Similarity between scenario feature vectors (research ranking only)."""
from __future__ import annotations

from math import sqrt
from typing import List, Sequence, Tuple

from engine.patterns.features import ScenarioFeatures


def _euclid(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise ValueError("feature vectors must have same length")
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def similarity_score(a: ScenarioFeatures, b: ScenarioFeatures) -> float:
    """Return score in (0, 1]: higher = more similar. Based on inverse distance."""
    d = _euclid(a.to_vector(), b.to_vector())
    return 1.0 / (1.0 + d)


def rank_neighbors(
    query: ScenarioFeatures,
    library: Sequence[ScenarioFeatures],
    *,
    top_k: int = 20,
) -> List[Tuple[int, float]]:
    """Return list of (index, score) sorted by descending similarity."""
    if top_k < 1:
        raise ValueError("top_k must be >= 1")
    scored = [(i, similarity_score(query, feat)) for i, feat in enumerate(library)]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]
