"""Deterministic post-vision pipeline for Fimathe chart analysis.

This module does not infer candles from pixels. A vision layer must provide the
observed OHLC values and a visually assessed channel candidate. Values read from
pixels should be marked estimated by the caller.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from engine.channels.geometry import (
    build_neutral_zone,
    create_reference_channel,
    level_50_of_channel,
    project_levels,
)
from engine.core.models import TrendDirection, MarketCandle
from engine.breakouts.confirmation import is_breakout_by_close


@dataclass(frozen=True)
class CandleInput:
    open: float
    high: float
    low: float
    close: float
    is_closed: bool = True
    timestamp: Optional[str] = None

    def validate(self) -> None:
        if self.high < self.low:
            raise ValueError("Candle high cannot be below low")
        if not self.low <= self.open <= self.high:
            raise ValueError("Candle open must be between low and high")
        if not self.low <= self.close <= self.high:
            raise ValueError("Candle close must be between low and high")


def analyze_chart_data(
    candles: List[Dict[str, Any]],
    *,
    channel_lower: float,
    channel_upper: float,
    trend: str,
    symbol: str = "UNKNOWN",
    timeframe: str = "UNKNOWN",
    price_precision: str = "estimated",
    point_a_evidence: str = "",
    point_b_evidence: str = "",
    boundary_method: str = "uncertain",
) -> Dict[str, Any]:
    """Validate vision output and calculate levels without inventing an entry."""
    if not candles:
        raise ValueError("At least one candle is required")
    if trend not in {"up", "down"}:
        raise ValueError("trend must be 'up' or 'down'; do not guess sideways/unknown")
    if price_precision not in {"exact", "estimated", "unreadable"}:
        raise ValueError("price_precision must be exact, estimated, or unreadable")
    if boundary_method not in {"body", "wick", "mixed", "uncertain"}:
        raise ValueError("boundary_method must be body, wick, mixed, or uncertain")
    if channel_upper <= channel_lower:
        raise ValueError("channel_upper must be greater than channel_lower")

    parsed = [CandleInput(**c) for c in candles]
    for candle in parsed:
        candle.validate()

    ref = create_reference_channel(
        channel_lower, channel_upper, timeframe=timeframe,
        source="vision_candidate", label="candidate_visual",
    )
    direction = TrendDirection.DOWN if trend == "down" else TrendDirection.UP
    neutral_result = build_neutral_zone(ref, direction)
    neutral = neutral_result.value
    mid_result = level_50_of_channel(channel_lower, channel_upper)
    latest = parsed[-1]

    stamp = latest.timestamp
    try:
        dt = datetime.fromisoformat(stamp.replace("Z", "+00:00")) if stamp else datetime.now(timezone.utc)
    except (ValueError, AttributeError):
        dt = datetime.now(timezone.utc)
    market_candle = MarketCandle(
        timestamp_open=dt, timestamp_close=dt,
        open=latest.open, high=latest.high, low=latest.low, close=latest.close,
        timeframe=timeframe, is_closed=latest.is_closed,
    )
    breakout = is_breakout_by_close(market_candle, ref, trend)
    if latest.is_closed and breakout.value is True:
        breakout_status = "confirmed_close_outside_reference_channel"
    elif not latest.is_closed:
        breakout_status = "pending_candle_not_closed"
    else:
        breakout_status = "no_close_breakout"

    projection = project_levels(
        channel_lower if trend == "down" else channel_upper,
        ref.amplitude, trend, [1.0, 1.5, 2.0],
    )
    warnings = list(neutral_result.warnings) + list(breakout.warnings) + list(projection.warnings)
    if price_precision == "estimated":
        warnings.append("Prices estimated from image; not exact OHLC data.")
    elif price_precision == "unreadable":
        warnings.append("Price scale unreadable: numeric price levels must not be presented as reliable.")
    if not point_a_evidence or not point_b_evidence:
        warnings.append("Evidence for A/B is incomplete; channel remains a visual hypothesis.")
    warnings.append("Entry is not generated automatically: the repository does not define a universal entry trigger for every scenario.")

    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "trend": trend,
        "channel": {
            "lower": channel_lower, "upper": channel_upper,
            "amplitude": ref.amplitude,
            "price_precision": price_precision,
            "point_a_evidence": point_a_evidence,
            "point_b_evidence": point_b_evidence,
            "boundary_method": boundary_method,
            "status": "visual_candidate_not_official",
        },
        "neutral_zone": {"lower": neutral.lower, "upper": neutral.upper,
                         "clarity": neutral_result.clarity.value},
        "level_50_reference": mid_result.value,
        "latest_candle": asdict(latest),
        "breakout_status": breakout_status,
        "entry": {"status": "pending_strategy_specific_confirmation", "price": None},
        "stop": {"status": "needs_strategy_specific_buffer", "price": None,
                 "reason": "Documented rule says beyond the outer neutral-zone boundary; exact buffer is not specified."},
        "projections": [
            {"multiplier": item["multiplier"], "price": item["price"], "status": "geometric_projection_not_confirmed_target"}
            for item in (projection.value or [])
        ],
        "warnings": warnings,
        "limitations": [
            "This pipeline validates extracted data; it does not perform image/pixel candle extraction.",
            "A/B localization remains partly subjective in the source material.",
            "A closed-candle breakout is not, by itself, a complete entry strategy.",
        ],
    }
