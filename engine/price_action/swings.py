"""Pivot detection without look-ahead bias."""
from __future__ import annotations

from typing import List, Sequence

from engine.price_action.models import SwingPoint, SwingType


def detect_swings(
    highs: Sequence[float],
    lows: Sequence[float],
    *,
    left: int = 2,
    right: int = 2,
) -> List[SwingPoint]:
    """Return confirmed pivots only after `right` bars have closed to the right."""
    if left < 1 or right < 1:
        raise ValueError("left and right must be >= 1")
    n = len(highs)
    if n != len(lows) or n < left + right + 1:
        return []

    swings: List[SwingPoint] = []
    for i in range(left, n - right):
        window_h = highs[i - left : i + right + 1]
        window_l = lows[i - left : i + right + 1]
        if highs[i] == max(window_h) and all(highs[i] > highs[j] for j in range(i - left, i)):
            if all(highs[i] >= highs[j] for j in range(i + 1, i + right + 1)):
                if highs[i] > max(highs[i + 1 : i + right + 1]):
                    swings.append(
                        SwingPoint(
                            index=i,
                            price=float(highs[i]),
                            swing_type=SwingType.HIGH,
                            confirmed_at_index=i + right,
                        )
                    )
        if lows[i] == min(window_l) and all(lows[i] < lows[j] for j in range(i - left, i)):
            if lows[i] < min(lows[i + 1 : i + right + 1]):
                swings.append(
                    SwingPoint(
                        index=i,
                        price=float(lows[i]),
                        swing_type=SwingType.LOW,
                        confirmed_at_index=i + right,
                    )
                )
    swings.sort(key=lambda s: s.index)
    return swings
