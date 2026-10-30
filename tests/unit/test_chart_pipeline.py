from engine.analysis.chart_pipeline import analyze_chart_data
from engine.analysis.svg_renderer import render_candles_svg


def sample_candles():
    return [
        {"open": 110, "high": 114, "low": 108, "close": 112, "is_closed": True},
        {"open": 112, "high": 113, "low": 104, "close": 106, "is_closed": True},
        {"open": 106, "high": 109, "low": 99, "close": 101, "is_closed": False},
    ]


def test_pipeline_does_not_invent_entry_or_exact_stop():
    result = analyze_chart_data(sample_candles(), channel_lower=100, channel_upper=120,
        trend="down", price_precision="estimated", point_a_evidence="swing high near candle 1",
        point_b_evidence="swing low near candle 2", boundary_method="wick")
    assert result["channel"]["amplitude"] == 20
    assert result["level_50_reference"] == 110
    assert result["breakout_status"] == "pending_candle_not_closed"
    assert result["entry"]["price"] is None
    assert result["stop"]["price"] is None
    assert any("estimated" in warning.lower() for warning in result["warnings"])


def test_closed_close_outside_is_detected():
    candles = [{"open": 105, "high": 108, "low": 96, "close": 98, "is_closed": True}]
    result = analyze_chart_data(candles, channel_lower=100, channel_upper=120, trend="down")
    assert result["breakout_status"] == "confirmed_close_outside_reference_channel"


def test_svg_contains_candles_and_separate_levels():
    candles = sample_candles()
    svg = render_candles_svg(candles, channel_lower=100, channel_upper=120,
        neutral_lower=120, neutral_upper=140, level_50=110, symbol="TEST", timeframe="M15")
    assert svg.startswith('<svg')
    assert "CANAL H" in svg and "ZONA NEUTRA H" in svg and "50% CANAL" in svg
    assert svg.count("<rect") >= len(candles)


def test_candidate_generator_returns_multiple_labeled_hypotheses():
    from engine.channels.candidate_detector import generate_channel_candidates
    candles = [
        {"open": 10+i, "high": 13+i, "low": 8+i, "close": 11+i}
        for i in range(24)
    ]
    candidates = generate_channel_candidates(candles, window_sizes=(5, 10, 20))
    assert len(candidates) == 3
    assert all(c["status"] == "experimental_candidate_not_official_channel" for c in candidates)
    assert all("lower_boundary_near_touches" in c["evidence"] for c in candidates)
