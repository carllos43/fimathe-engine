"""Outcome definitions for comparable historical cases.

Same definition must be applied to every historical window.
"""
from __future__ import annotations

from enum import Enum
from math import isfinite
from typing import Any, Dict, Sequence


class OutcomeLabel(str, Enum):
    UP_FIRST = "up_first"
    DOWN_FIRST = "down_first"
    LATERAL = "lateral"
    UNKNOWN = "unknown"


def classify_outcome(
    future_candles: Sequence[Dict[str, Any]],
    *,
    up_target: float,
    down_target: float,
) -> OutcomeLabel:
    """Scan closed path: first touch of up_target or down_target wins."""
    if not future_candles:
        return OutcomeLabel.UNKNOWN
    if not all(map(isfinite, (up_target, down_target))):
        raise ValueError("targets must be finite")
    if up_target <= down_target:
        raise ValueError("up_target must be > down_target")

    for i, c in enumerate(future_candles):
        try:
            h, l = float(c["high"]), float(c["low"])
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f"invalid future candle at {i}") from e
        if not isfinite(h) or not isfinite(l) or h < l:
            raise ValueError(f"invalid future bounds at {i}")
        hit_up = h >= up_target
        hit_down = l <= down_target
        if hit_up and hit_down:
            return OutcomeLabel.UNKNOWN
        if hit_up:
            return OutcomeLabel.UP_FIRST
        if hit_down:
            return OutcomeLabel.DOWN_FIRST
    return OutcomeLabel.LATERAL
