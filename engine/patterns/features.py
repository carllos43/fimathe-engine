"""Extract normalized scenario features from OHLC + channel bounds.

All geometry is relative so channels of different absolute size can be compared.
Does not detect official Fimathe A/B points — caller supplies L/H or uses a candidate.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isfinite
from typing import Any, Dict, List, Sequence


@dataclass(frozen=True)
class ScenarioFeatures:
    """Normalized fingerprint of a market window."""

    amplitude: float
    price_position_r: float
    bars_in_window: int
    bull_fraction: float
    mean_body_ratio: float
    mean_range_over_amp: float
    dist_to_upper: float
    dist_to_lower: float
    last_close_beyond: str
    pivot_highs: int
    pivot_lows: int
    meta: Dict[str, Any]

    def to_vector(self) -> List[float]:
        beyond = {"above": 1.0, "below": -1.0, "inside": 0.0}.get(self.last_close_beyond, 0.0)
        return [
            self.amplitude,
            self.price_position_r,
            float(self.bars_in_window),
            self.bull_fraction,
            self.mean_body_ratio,
            self.mean_range_over_amp,
            self.dist_to_upper,
            self.dist_to_lower,
            beyond,
            float(self.pivot_highs),
            float(self.pivot_lows),
        ]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["vector"] = self.to_vector()
        return d


def _clean(candles: Sequence[Dict[str, Any]]) -> List[Dict[str, float]]:
    out: List[Dict[str, float]] = []
    for i, c in enumerate(candles):
        try:
            o, h, l, cl = (float(c[k]) for k in ("open", "high", "low", "close"))
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f"invalid OHLC at index {i}") from e
        if not all(map(isfinite, (o, h, l, cl))) or h < l or not (l <= o <= h and l <= cl <= h):
            raise ValueError(f"invalid OHLC bounds at index {i}")
        out.append({"open": o, "high": h, "low": l, "close": cl})
    if not out:
        raise ValueError("candles cannot be empty")
    return out


def _count_pivots(values: Sequence[float], left: int, right: int, kind: str) -> int:
    count = 0
    for i in range(left, len(values) - right):
        window = values[i - left : i + right + 1]
        if kind == "high":
            if values[i] == max(window) and values[i] > max(values[i - left : i]) and values[i] >= max(
                values[i + 1 : i + right + 1]
            ):
                count += 1
        else:
            if values[i] == min(window) and values[i] < min(values[i - left : i]) and values[i] <= min(
                values[i + 1 : i + right + 1]
            ):
                count += 1
    return count


def extract_features(
    candles: Sequence[Dict[str, Any]],
    *,
    lower: float,
    upper: float,
    pivot_left: int = 2,
    pivot_right: int = 2,
) -> ScenarioFeatures:
    """Build ScenarioFeatures from OHLC and channel bounds [lower, upper]."""
    if not isfinite(lower) or not isfinite(upper) or upper <= lower:
        raise ValueError("require finite upper > lower")
    if pivot_left < 1 or pivot_right < 1:
        raise ValueError("pivot_left and pivot_right must be >= 1")
    cs = _clean(candles)
    amp = upper - lower
    last = cs[-1]
    r = (last["close"] - lower) / amp
    if last["close"] > upper:
        beyond = "above"
    elif last["close"] < lower:
        beyond = "below"
    else:
        beyond = "inside"

    bodies = []
    ranges = []
    bulls = 0
    for c in cs:
        bodies.append(abs(c["close"] - c["open"]) / amp)
        ranges.append((c["high"] - c["low"]) / amp)
        if c["close"] > c["open"]:
            bulls += 1

    highs = [c["high"] for c in cs]
    lows = [c["low"] for c in cs]
    ph = _count_pivots(highs, pivot_left, pivot_right, "high") if len(cs) > pivot_left + pivot_right else 0
    pl = _count_pivots(lows, pivot_left, pivot_right, "low") if len(cs) > pivot_left + pivot_right else 0

    return ScenarioFeatures(
        amplitude=amp,
        price_position_r=r,
        bars_in_window=len(cs),
        bull_fraction=bulls / len(cs),
        mean_body_ratio=sum(bodies) / len(bodies),
        mean_range_over_amp=sum(ranges) / len(ranges),
        dist_to_upper=(upper - last["close"]) / amp,
        dist_to_lower=(last["close"] - lower) / amp,
        last_close_beyond=beyond,
        pivot_highs=ph,
        pivot_lows=pl,
        meta={
            "lower": lower,
            "upper": upper,
            "last_close": last["close"],
            "status": "experimental_features_not_official_fimathe",
        },
    )
