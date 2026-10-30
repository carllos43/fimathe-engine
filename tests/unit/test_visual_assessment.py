from engine.channels.visual_assessment import (
    VisualChannelCandidate,
    assess_visual_channel,
)
from engine.core.models import TrendDirection


def candidate(**overrides):
    data = dict(
        lower=100.0,
        upper=120.0,
        direction=TrendDirection.DOWN,
        timeframe="M15",
        point_a_evidence="Resistance region around the visible prior swing high.",
        point_b_evidence="Support region around the visible consolidation low.",
        trend_evidence="Lower highs and lower lows are visible in the analyzed segment.",
        boundary_method="wick",
        width_assessment="appropriate",
        price_precision="estimated",
    )
    data.update(overrides)
    return VisualChannelCandidate(**data)


def test_assess_visual_channel_computes_existing_geometry():
    result = assess_visual_channel(candidate())
    assert result.status == "candidate_ready"
    assert result.amplitude == 20.0
    assert result.midpoint_50 == 110.0
    assert result.neutral_lower == 120.0
    assert result.neutral_upper == 140.0
    assert result.warnings == []


def test_no_fixed_touch_count_is_required():
    result = assess_visual_channel(candidate())
    assert result.status == "candidate_ready"


def test_narrow_channel_requires_review():
    result = assess_visual_channel(candidate(width_assessment="narrow"))
    assert result.status == "needs_review"
    assert any("width" in warning.lower() or "narrow" in warning.lower() for warning in result.warnings)


def test_missing_anchor_evidence_requires_review():
    result = assess_visual_channel(candidate(point_a_evidence=""))
    assert result.status == "needs_review"


def test_unreadable_scale_is_not_presented_as_exact():
    result = assess_visual_channel(candidate(price_precision="unreadable"))
    assert result.status == "needs_review"
    assert any("unreadable" in warning.lower() for warning in result.warnings)


def test_invalid_bounds_are_rejected():
    result = assess_visual_channel(candidate(lower=120.0, upper=100.0))
    assert result.status in ("invalid", "invalid_candidate")
    assert result.amplitude is None


def test_uptrend_neutral_zone_retains_provisional_warning():
    result = assess_visual_channel(candidate(direction=TrendDirection.UP))
    assert result.neutral_lower == 80.0
    assert result.neutral_upper == 100.0
    assert any("provisional" in warning.lower() for warning in result.warnings)
