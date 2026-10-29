"""
Tests for higher-TF mapping and pure mathematical subdivision (fatiamento).
"""

import pytest
from datetime import datetime, timezone
from engine.mapping.higher_tf import (
    subdivide_interval,
    build_higher_tf_map,
    context_between_timeframes,
    HigherTimeframeMap,
)
from engine.core.models import MarketCandle


def test_subdivide_depth_1():
    res = subdivide_interval(100.0, 200.0, depth=1)
    assert res.value is not None
    levels = res.value.levels
    assert levels == [100.0, 150.0, 200.0]
    assert res.value.nomenclature == "Fimathe 350"
    assert res.value.math_confirmation == "pending"
    assert any("pendente" in w.lower() for w in res.warnings)


def test_subdivide_depth_2():
    res = subdivide_interval(0.0, 100.0, depth=2)
    levels = res.value.levels
    assert len(levels) == 5
    assert levels[0] == 0.0
    assert levels[-1] == 100.0
    assert levels[2] == 50.0


def test_subdivide_depth_3():
    res = subdivide_interval(0.0, 80.0, depth=3)
    levels = res.value.levels
    assert len(levels) == 9
    assert levels[0] == 0.0
    assert levels[-1] == 80.0
    assert levels[1] == 10.0
    assert levels[4] == 40.0


def test_subdivide_invalid():
    res = subdivide_interval(100.0, 50.0, depth=1)
    assert res.value is None
    res2 = subdivide_interval(0.0, 100.0, depth=0)
    assert res2.value is None


def test_higher_tf_map_basic():
    m = build_higher_tf_map(
        timeframe_ref="W1",
        top=1500.0,
        bottom=1400.0,
        project_multipliers=[1.0, 2.0],
        subdivision_depth=1,
    )
    assert m.amplitude == 100.0
    assert m.channel_lower == 1400.0
    assert m.channel_upper == 1500.0
    assert len(m.projected_levels) > 0
    assert len(m.subdivisions) == 3
    d = m.to_dict()
    assert d["timeframe_ref"] == "W1"
    assert d["study_version"] == "0.2"


def test_context_no_future_leak():
    higher = build_higher_tf_map("D1", top=120.0, bottom=100.0)
    ts = datetime(2026, 10, 27, 10, 0, tzinfo=timezone.utc)
    candles = [
        MarketCandle(ts, ts, 110, 112, 109, 111, "M15", is_closed=True),
        MarketCandle(ts, ts, 111, 113, 110, 112, "M15", is_closed=False),
    ]
    ctx = context_between_timeframes(higher, candles)
    assert "inherited_from_higher_tf" in ctx
    assert len(ctx["incomplete_data"]) == 1
    assert ctx["incomplete_data"][0]["is_closed"] is False
    assert "Nunca use candles futuros" in ctx["warning"]
