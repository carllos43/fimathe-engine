"""Minimal tests for Price Action structure and confluence."""
from engine.price_action.models import (
    MarketRegime,
    SwingPoint,
    SwingType,
    TradeDecision,
    ConfluenceStatus,
)
from engine.price_action.swings import detect_swings
from engine.price_action.structure import classify_structure_sequence, label_swings
from engine.price_action.trend import classify_market_regime
from engine.price_action.confluence import evaluate_confluence
from engine.price_action.report import build_chat_report
from engine.price_action.models import PriceActionReport


def test_detect_swings_no_lookahead_high_low():
    highs = [10, 11, 12, 11, 10, 11, 13, 12, 11]
    lows  = [9, 10, 11, 10, 9, 10, 12, 11, 10]
    swings = detect_swings(highs, lows, left=1, right=1)
    assert all(s.confirmed_at_index is not None for s in swings)
    assert all(s.confirmed_at_index > s.index for s in swings)


def test_hh_hl_uptrend_sequence():
    swings = [
        SwingPoint(0, 100, SwingType.LOW),
        SwingPoint(1, 110, SwingType.HIGH),
        SwingPoint(2, 105, SwingType.LOW),
        SwingPoint(3, 120, SwingType.HIGH),
        SwingPoint(4, 112, SwingType.LOW),
    ]
    labeled = label_swings(swings)
    labels = [s.label.value for s in labeled if s.label.value != "UNKNOWN"]
    assert "HH" in labels
    assert "HL" in labels
    regime, bias = classify_market_regime(swings)
    assert regime == MarketRegime.UPTREND


def test_lh_ll_downtrend_sequence():
    swings = [
        SwingPoint(0, 120, SwingType.HIGH),
        SwingPoint(1, 100, SwingType.LOW),
        SwingPoint(2, 115, SwingType.HIGH),
        SwingPoint(3, 95, SwingType.LOW),
        SwingPoint(4, 110, SwingType.HIGH),
    ]
    regime, bias = classify_market_regime(swings)
    assert regime == MarketRegime.DOWNTREND


def test_confluence_aligned_still_wait_without_breakout():
    conf, plan = evaluate_confluence(
        MarketRegime.DOWNTREND,
        bias=__import__("engine.price_action.models", fromlist=["TrendBias"]).TrendBias.BEARISH,
        fimathe_direction="down",
        breakout_confirmed=False,
    )
    assert conf.status == ConfluenceStatus.ALIGNED
    assert plan.decision == TradeDecision.WAIT


def test_confluence_conflict():
    from engine.price_action.models import TrendBias
    conf, plan = evaluate_confluence(
        MarketRegime.UPTREND,
        bias=TrendBias.BULLISH,
        fimathe_direction="down",
        breakout_confirmed=True,
    )
    assert conf.status == ConfluenceStatus.CONFLICTING
    assert plan.decision == TradeDecision.WAIT


def test_confluence_aligned_with_breakout_gives_setup_without_prices():
    from engine.price_action.models import TrendBias
    conf, plan = evaluate_confluence(
        MarketRegime.DOWNTREND,
        bias=TrendBias.BEARISH,
        fimathe_direction="down",
        breakout_confirmed=True,
    )
    assert conf.status == ConfluenceStatus.ALIGNED
    assert plan.decision == TradeDecision.SELL_SETUP
    assert plan.entry is None
    assert plan.stop_loss is None


def test_report_has_seven_sections():
    text = build_chat_report(PriceActionReport(summary="Teste"))
    for i in range(1, 8):
        assert f"### {i}." in text
