"""HH/HL/LH/LL labeling and structure sequence."""
from __future__ import annotations

from typing import List, Sequence

from engine.price_action.models import (
    MarketStructure,
    StructureStatus,
    SwingLabel,
    SwingPoint,
    SwingType,
)


def label_swings(swings: Sequence[SwingPoint]) -> List[SwingPoint]:
    """Label each swing relative to the previous swing of the same type."""
    last_high = None
    last_low = None
    labeled: List[SwingPoint] = []
    for s in swings:
        if s.swing_type == SwingType.HIGH:
            if last_high is None:
                label = SwingLabel.UNKNOWN
            elif s.price > last_high:
                label = SwingLabel.HH
            elif s.price < last_high:
                label = SwingLabel.LH
            else:
                label = SwingLabel.UNKNOWN
            last_high = s.price
        else:
            if last_low is None:
                label = SwingLabel.UNKNOWN
            elif s.price > last_low:
                label = SwingLabel.HL
            elif s.price < last_low:
                label = SwingLabel.LL
            else:
                label = SwingLabel.UNKNOWN
            last_low = s.price
        labeled.append(
            SwingPoint(
                index=s.index,
                price=s.price,
                swing_type=s.swing_type,
                label=label,
                confirmed_at_index=s.confirmed_at_index,
            )
        )
    return labeled


def classify_structure_sequence(swings: Sequence[SwingPoint]) -> MarketStructure:
    """Classify structure from labeled swings."""
    labeled = label_swings(swings)
    seq = [s.label.value for s in labeled if s.label != SwingLabel.UNKNOWN]
    status = StructureStatus.UNCLEAR
    if not seq:
        return MarketStructure(swings=list(labeled), sequence=seq, structure_status=status)

    recent = seq[-4:] if len(seq) >= 4 else seq
    has_hh = "HH" in recent
    has_hl = "HL" in recent
    has_lh = "LH" in recent
    has_ll = "LL" in recent

    if has_hh and has_hl and not (has_lh or has_ll):
        status = StructureStatus.INTACT
    elif has_lh and has_ll and not (has_hh or has_hl):
        status = StructureStatus.INTACT
    elif (has_hh and has_hl) and (has_lh or has_ll):
        status = StructureStatus.WEAKENING
    elif (has_lh and has_ll) and (has_hh or has_hl):
        status = StructureStatus.WEAKENING
    else:
        status = StructureStatus.UNCLEAR

    return MarketStructure(swings=list(labeled), sequence=seq, structure_status=status)
