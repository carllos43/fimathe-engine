"""Search helper: rank historical windows by feature similarity.

Caller owns the library of past ScenarioFeatures + their recorded outcomes.
This module does not load CSV or invent history.
"""
from __future__ import annotations

from typing import Any, Dict, List, Sequence

from engine.patterns.features import ScenarioFeatures
from engine.patterns.similarity import rank_neighbors


def search_similar(
    query: ScenarioFeatures,
    library: Sequence[ScenarioFeatures],
    *,
    top_k: int = 20,
    min_score: float = 0.0,
) -> List[Dict[str, Any]]:
    """Return ranked matches with index and score; filter by min_score."""
    ranks = rank_neighbors(query, library, top_k=top_k)
    out = []
    for idx, score in ranks:
        if score < min_score:
            continue
        out.append(
            {
                "library_index": idx,
                "similarity": round(score, 6),
                "features": library[idx].to_dict(),
            }
        )
    return out
