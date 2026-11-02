"""Market regime classification from structure sequence."""
from __future__ import annotations

from typing import Sequence

from engine.price_action.models import MarketRegime, SwingLabel, SwingPoint, TrendBias
from engine.price_action.structure import label_swings


def classify_market_regime(swings: Sequence[SwingPoint]) -> tuple[MarketRegime, TrendBias]:
    labeled = label_swings(swings)
    labels = [s.label for s in labeled if s.label != SwingLabel.UNKNOWN]
    if len(labels) < 2:
        return MarketRegime.UNKNOWN, TrendBias.UNKNOWN

    recent = labels[-4:] if len(labels) >= 4 else labels
    bull = sum(1 for x in recent if x in (SwingLabel.HH, SwingLabel.HL))
    bear = sum(1 for x in recent if x in (SwingLabel.LH, SwingLabel.LL))

    if bull >= 2 and bear == 0:
        return MarketRegime.UPTREND, TrendBias.BULLISH
    if bear >= 2 and bull == 0:
        return MarketRegime.DOWNTREND, TrendBias.BEARISH
    if bull > 0 and bear > 0:
        return MarketRegime.TRANSITION, TrendBias.NEUTRAL
    if bull == 0 and bear == 0:
        return MarketRegime.RANGE, TrendBias.NEUTRAL
    return MarketRegime.UNKNOWN, TrendBias.UNKNOWN
