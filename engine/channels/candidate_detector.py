"""Experimental channel candidate generator from extracted OHLC candles.

This proposes alternatives; it is not an official Fimathe A/B rule.
"""
from __future__ import annotations
from typing import Any, Dict, Iterable, List


def generate_channel_candidates(candles: List[Dict[str, Any]], *,
        window_sizes: Iterable[int] = (8, 12, 20),
        boundary_tolerance_ratio: float = 0.04) -> List[Dict[str, Any]]:
    """Generate trailing-range hypotheses with transparent heuristic evidence.

    Candles must be chronological. The caller is responsible for excluding future
    data. Touch counts are descriptive heuristics, not a validated ranking score.
    """
    if len(candles) < 3:
        return []
    if not 0 <= boundary_tolerance_ratio <= 0.25:
        raise ValueError("boundary_tolerance_ratio must be between 0 and 0.25")
    cleaned = []
    for i, c in enumerate(candles):
        try:
            o, h, low, close = (float(c[k]) for k in ("open", "high", "low", "close"))
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Invalid OHLC data at candle index {i}") from exc
        if h < low or not low <= o <= h or not low <= close <= h:
            raise ValueError(f"Invalid OHLC bounds at candle index {i}")
        cleaned.append({"open": o, "high": h, "low": low, "close": close})

    candidates, seen = [], set()
    for requested_window in window_sizes:
        if not isinstance(requested_window, int) or requested_window < 3:
            continue
        size = min(requested_window, len(cleaned))
        subset = cleaned[-size:]
        lower = min(c["low"] for c in subset)
        upper = max(c["high"] for c in subset)
        if upper <= lower:
            continue
        key = (round(lower, 10), round(upper, 10), size)
        if key in seen:
            continue
        seen.add(key)
        tolerance = (upper - lower) * boundary_tolerance_ratio
        lower_touches = sum(c["low"] <= lower + tolerance for c in subset)
        upper_touches = sum(c["high"] >= upper - tolerance for c in subset)
        candidates.append({
            "candidate_id": f"range_{size}_{len(candidates)+1}",
            "lower": lower, "upper": upper, "amplitude": upper - lower,
            "window_candles": size,
            "evidence": {"lower_boundary_near_touches": lower_touches,
                         "upper_boundary_near_touches": upper_touches,
                         "tolerance_price": tolerance},
            "status": "experimental_candidate_not_official_channel",
            "limitations": [
                "Trailing high/low envelope; not verified Fimathe A/B construction.",
                "Touch counts do not imply channel validity or trading probability.",
                "Review trend, swings, body-versus-wick choice and source examples visually.",
            ],
        })
    return sorted(candidates, key=lambda x: (
        x["evidence"]["lower_boundary_near_touches"] + x["evidence"]["upper_boundary_near_touches"],
        -x["amplitude"]), reverse=True)
