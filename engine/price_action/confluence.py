"""Confluence between Price Action regime and Fimathe direction."""
from __future__ import annotations

from typing import Optional

from engine.price_action.models import (
    ConfluenceStatus,
    FimatheConfluence,
    MarketRegime,
    TradeDecision,
    TradePlan,
    TrendBias,
)


def evaluate_confluence(
    regime: MarketRegime,
    bias: TrendBias,
    *,
    fimathe_direction: Optional[str] = None,
    fimathe_variant: Optional[str] = None,
    breakout_confirmed: bool = False,
) -> tuple[FimatheConfluence, TradePlan]:
    """Compare PA regime with Fimathe direction; never invent entry/stop prices."""
    fd = (fimathe_direction or "UNKNOWN").lower()
    notes = []

    if fimathe_direction is None:
        status = ConfluenceStatus.UNAVAILABLE
        notes.append("Fimathe direction not supplied.")
    elif regime == MarketRegime.UPTREND and fd in ("up", "high", "bullish"):
        status = ConfluenceStatus.ALIGNED
    elif regime == MarketRegime.DOWNTREND and fd in ("down", "low", "bearish"):
        status = ConfluenceStatus.ALIGNED
    elif regime in (MarketRegime.RANGE, MarketRegime.TRANSITION) and fd in ("sideways", "unknown"):
        status = ConfluenceStatus.NEUTRAL
    elif regime == MarketRegime.UNKNOWN or fd == "unknown":
        status = ConfluenceStatus.UNAVAILABLE
    elif (regime == MarketRegime.UPTREND and fd in ("down", "low", "bearish")) or (
        regime == MarketRegime.DOWNTREND and fd in ("up", "high", "bullish")
    ):
        status = ConfluenceStatus.CONFLICTING
        notes.append("Price Action regime conflicts with Fimathe direction.")
    else:
        status = ConfluenceStatus.NEUTRAL

    conf = FimatheConfluence(
        variant=fimathe_variant,
        direction=fd.upper() if fd else "UNKNOWN",
        status=status,
        references=["docs/PRICE_ACTION_ENGINE.md", "docs/REGRAS_OPERACIONAIS.md"],
        notes=notes,
    )

    if status == ConfluenceStatus.ALIGNED and breakout_confirmed:
        decision = (
            TradeDecision.BUY_SETUP
            if bias == TrendBias.BULLISH
            else TradeDecision.SELL_SETUP
            if bias == TrendBias.BEARISH
            else TradeDecision.WAIT
        )
        plan = TradePlan(
            decision=decision,
            entry_type="conditional_on_fimathe_and_close_confirmation",
            entry=None,
            stop_loss=None,
            invalidation="Structure break against bias or Fimathe channel invalidation",
        )
    else:
        plan = TradePlan(
            decision=TradeDecision.WAIT,
            entry_type=None,
            invalidation="Await structure confirmation and/or Fimathe close beyond channel",
        )
        if status == ConfluenceStatus.CONFLICTING:
            plan.invalidation = "Resolve PA vs Fimathe conflict before entry"
    return conf, plan
