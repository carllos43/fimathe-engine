"""Deterministic unit tests for channel geometry, neutral zone, 50% levels."""
import pytest
from datetime import datetime, timezone
from engine.core.models import ReferenceChannel, TrendDirection, MarketCandle
from engine.channels.geometry import (
    channel_amplitude, build_neutral_zone, level_50_of_channel,
    level_50_of_two_channels, project_levels, create_reference_channel,
)
from engine.cycles.projections import create_expansion, subcycle_from_entry
from engine.breakouts.confirmation import is_breakout_by_close, touch_or_cross_intrabar

def test_amplitude_basic():
    res = channel_amplitude(100.0, 120.0)
    assert res.value == 20.0
    assert res.rule_id == "R_amplitude"

def test_amplitude_invalid():
    res = channel_amplitude(120.0, 100.0)
    assert res.value is None

def test_neutral_zone_downtrend():
    ref = create_reference_channel(100.0, 120.0)
    res = build_neutral_zone(ref, TrendDirection.DOWN)
    assert res.value is not None
    assert res.value.lower == 120.0 and res.value.upper == 140.0

def test_neutral_zone_uptrend_provisional():
    ref = create_reference_channel(100.0, 120.0)
    res = build_neutral_zone(ref, TrendDirection.UP)
    assert res.value is not None
    assert any("provisional" in w.lower() for w in res.warnings)

def test_50_of_channel():
    assert level_50_of_channel(100.0, 120.0).value == 110.0

def test_50_of_two_channels_separate():
    r50 = level_50_of_channel(100.0, 120.0)
    n50 = level_50_of_channel(120.0, 140.0)
    union50 = level_50_of_two_channels(100.0, 120.0, 120.0, 140.0)
    assert r50.value == 110.0 and n50.value == 130.0 and union50.value == 120.0

def test_project_levels():
    res = project_levels(120.0, 20.0, "up", [1.0, 2.0])
    assert res.value[0]["price"] == 140.0 and res.value[1]["price"] == 160.0

def test_expansion_not_auto_confirmed():
    res = create_expansion(120.0, 20.0, "up", 1.0)
    assert res.value.confirmed_target is False

def test_subcycle_down():
    assert subcycle_from_entry(115.0, 20.0, "down").value.price == 95.0

def test_breakout_by_close_only():
    ref = create_reference_channel(100.0, 120.0)
    ts = datetime(2026, 10, 27, 12, 0, tzinfo=timezone.utc)
    c_break = MarketCandle(ts, ts, 110.0, 112.0, 98.0, 99.0, "M15", is_closed=True)
    assert is_breakout_by_close(c_break, ref, "down").value is True
    c_wick = MarketCandle(ts, ts, 110.0, 112.0, 98.0, 101.0, "M15", is_closed=True)
    assert is_breakout_by_close(c_wick, ref, "down").value is False
    assert touch_or_cross_intrabar(c_wick, 100.0) is True
    c_open = MarketCandle(ts, ts, 110.0, 112.0, 98.0, 99.0, "M15", is_closed=False)
    assert is_breakout_by_close(c_open, ref, "down").value is False

def test_known_example_manual_check():
    ref = create_reference_channel(100.0, 120.0)
    assert ref.amplitude == 20.0
    neut = build_neutral_zone(ref, TrendDirection.DOWN).value
    assert (neut.lower, neut.upper) == (120.0, 140.0)
    assert level_50_of_channel(100.0, 120.0).value == 110.0
    assert project_levels(100.0, 20.0, "down", [1.0]).value[0]["price"] == 80.0
    assert subcycle_from_entry(115.0, 20.0, "down").value.price == 95.0
