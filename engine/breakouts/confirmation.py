"""
Breakout confirmation by candle close only.
Shadow / intrabar touch is never treated as confirmed breakout.
"""

from __future__ import annotations

from engine.core.models import MarketCandle, CalculationResult, RuleClarity, ReferenceChannel


def is_breakout_by_close(
    candle: MarketCandle,
    channel: ReferenceChannel,
    direction: str,
) -> CalculationResult:
    """
    direction='down' → close < channel.lower
    direction='up'   → close > channel.upper

    Only closed candles are considered.
    """
    if not candle.is_closed:
        return CalculationResult(
            value=False,
            parameters={
                "candle_close": candle.close,
                "channel_lower": channel.lower,
                "channel_upper": channel.upper,
                "is_closed": False,
            },
            rule_id="B03_breakout_close",
            rule_version="0.2",
            clarity=RuleClarity.HIGH,
            warnings=["Candle still open – cannot confirm breakout"],
        )

    if direction == "down":
        broken = candle.close < channel.lower
        formula = "close < reference.lower"
    elif direction == "up":
        broken = candle.close > channel.upper
        formula = "close > reference.upper"
    else:
        return CalculationResult(
            value=None,
            parameters={},
            rule_id="B03_breakout_close",
            rule_version="0.2",
            clarity=RuleClarity.HIGH,
            warnings=["direction must be 'up' or 'down'"],
        )

    return CalculationResult(
        value=broken,
        parameters={
            "candle_close": candle.close,
            "candle_high": candle.high,
            "candle_low": candle.low,
            "channel_lower": channel.lower,
            "channel_upper": channel.upper,
            "direction": direction,
            "formula": formula,
            "timestamp_close": candle.timestamp_close.isoformat(),
        },
        rule_id="B03_breakout_close",
        rule_version="0.2",
        clarity=RuleClarity.HIGH,
        notes="Sombra fora do canal sem fechamento NÃO conta como rompimento",
    )


def touch_or_cross_intrabar(
    candle: MarketCandle,
    level: float,
) -> bool:
    """Utility: did price touch/cross the level during the bar? (not a confirmation)"""
    return candle.low <= level <= candle.high
