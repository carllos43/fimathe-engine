"""Structured hand-off from chart vision to the existing Fimathe geometry engine.

This module does not read pixels or detect channels autonomously. A vision model
or user supplies a visual candidate and its evidence; this module validates the
candidate's shape and computes only the geometric values already supported by
the engine. It deliberately does not confirm entries, stops, or targets.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from typing import List, Literal, Optional

from engine.channels.geometry import (
    build_neutral_zone,
    level_50_of_channel,
    create_reference_channel,
)
from engine.core.models import TrendDirection, RuleClarity


BoundaryMethod = Literal["body", "wick", "mixed", "uncertain"]
WidthAssessment = Literal["appropriate", "narrow", "wide", "uncertain"]
PricePrecision = Literal["exact", "estimated", "unreadable"]


@dataclass(frozen=True)
class VisualChannelCandidate:
    """A candidate channel identified from a chart image, with traceable evidence."""

    lower: float
    upper: float
    direction: TrendDirection
    timeframe: str
    point_a_evidence: str
    point_b_evidence: str
    trend_evidence: str
    boundary_method: BoundaryMethod
    width_assessment: WidthAssessment
    price_precision: PricePrecision = "estimated"
    alternative_channels: List[str] = field(default_factory=list)
    image_limitations: List[str] = field(default_factory=list)


@dataclass
class VisualChannelAssessment:
    """Assessment output; candidate_ready never means a trading signal is confirmed."""

    status: str
    candidate: Optional[object]
    amplitude: Optional[float]
    midpoint_50: Optional[float]
    neutral_lower: Optional[float]
    neutral_upper: Optional[float]
    clarity: RuleClarity
    warnings: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)


def assess_visual_channel(
    candidate: VisualChannelCandidate,
) -> VisualChannelAssessment:
    """Validate visual evidence and compute supported geometry without inventing rules.

    A visually narrow, wide, uncertain, or insufficiently explained candidate is
    returned for review rather than silently accepted. No fixed number of candle
    touches is imposed because the source PDF does not specify one.
    """
    warnings: List[str] = []
    evidence: List[str] = []

    if not (isfinite(candidate.lower) and isfinite(candidate.upper)):
        return VisualChannelAssessment(
            status="invalid",
            candidate=None,
            amplitude=None,
            midpoint_50=None,
            neutral_lower=None,
            neutral_upper=None,
            clarity=RuleClarity.HIGH,
            warnings=["lower/upper must be finite numbers"],
            evidence=evidence,
        )

    if candidate.upper <= candidate.lower:
        return VisualChannelAssessment(
            status="invalid",
            candidate=None,
            amplitude=None,
            midpoint_50=None,
            neutral_lower=None,
            neutral_upper=None,
            clarity=RuleClarity.HIGH,
            warnings=["upper must be greater than lower"],
            evidence=evidence,
        )

    if candidate.width_assessment == "narrow":
        warnings.append(
            "Visual width assessed as narrow; review for false early entries "
            "instead of accepting automatically."
        )
    if candidate.width_assessment == "wide":
        warnings.append(
            "Visual width assessed as wide; review for delayed entries "
            "instead of accepting automatically."
        )
    if candidate.price_precision == "unreadable":
        warnings.append("Price scale is unreadable; do not present numeric prices as exact.")
    warnings.extend(candidate.image_limitations)

    evidence.extend([
        f"Trend evidence: {candidate.trend_evidence or 'not supplied'}",
        f"Point A evidence: {candidate.point_a_evidence or 'not supplied'}",
        f"Point B evidence: {candidate.point_b_evidence or 'not supplied'}",
        f"Boundary method: {candidate.boundary_method}",
        f"Width assessment: {candidate.width_assessment}",
        f"Price precision: {candidate.price_precision}",
    ])
    if candidate.alternative_channels:
        evidence.append("Alternative channel candidates were supplied for comparison.")

    channel = create_reference_channel(
        candidate.lower,
        candidate.upper,
        timeframe=candidate.timeframe,
        source="visual_candidate",
        label="reference_candidate",
    )
    midpoint = level_50_of_channel(candidate.lower, candidate.upper).value
    amplitude = channel.amplitude
    neutral_lower = neutral_upper = None

    if candidate.direction in (TrendDirection.UP, TrendDirection.DOWN):
        neutral_result = build_neutral_zone(channel, candidate.direction)
        if neutral_result.value is not None:
            neutral_lower = neutral_result.value.lower
            neutral_upper = neutral_result.value.upper
        warnings.extend(neutral_result.warnings)

    required_evidence_missing = (
        not candidate.trend_evidence.strip()
        or not candidate.point_a_evidence.strip()
        or not candidate.point_b_evidence.strip()
    )
    has_uncertainty = (
        required_evidence_missing
        or candidate.width_assessment != "appropriate"
        or candidate.boundary_method == "uncertain"
        or candidate.price_precision == "unreadable"
        or candidate.direction not in (TrendDirection.UP, TrendDirection.DOWN)
        or bool(candidate.alternative_channels)
        or bool(candidate.image_limitations)
    )

    return VisualChannelAssessment(
        status="needs_review" if has_uncertainty else "candidate_ready",
        candidate=channel,
        amplitude=amplitude,
        midpoint_50=midpoint,
        neutral_lower=neutral_lower,
        neutral_upper=neutral_upper,
        clarity=RuleClarity.MEDIUM if not has_uncertainty else RuleClarity.LOW,
        warnings=warnings,
        evidence=evidence,
    )
