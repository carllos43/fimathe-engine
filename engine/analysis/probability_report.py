"""Compose a research report: current features + neighbor frequencies.

Does not generate trade entries. Entry remains not_generated / WAIT.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from engine.patterns.features import extract_features
from engine.patterns.historical_search import search_similar
from engine.patterns.pattern_store import PatternStore
from engine.probability.estimator import empty_report_placeholder, estimate_frequencies


def build_probability_report(
    candles: Sequence[Dict[str, Any]],
    *,
    lower: float,
    upper: float,
    store: Optional[PatternStore] = None,
    top_k: int = 20,
    min_score: float = 0.0,
) -> Dict[str, Any]:
    features = extract_features(candles, lower=lower, upper=upper)
    base = {
        "scenario_features": features.to_dict(),
        "entry": {
            "status": "not_generated",
            "reason": "Probability layer does not create entries; Fimathe confirmation still required.",
        },
        "warnings": [
            "Historical frequency is not a trading signal.",
            "Without a labeled PatternStore, only features are returned.",
        ],
    }
    if store is None or store.size() == 0:
        base["historical"] = empty_report_placeholder()
        return base

    matches = search_similar(features, store.features_list(), top_k=top_k, min_score=min_score)
    neighbor_outcomes: List[str] = []
    for m in matches:
        neighbor_outcomes.append(store.items[m["library_index"]].outcome)
    est = estimate_frequencies(neighbor_outcomes)
    base["historical"] = {
        "matches": matches,
        "estimate": est.to_dict(),
        "library_size": store.size(),
    }
    return base
