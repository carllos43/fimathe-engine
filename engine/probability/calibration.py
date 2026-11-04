"""Placeholder for future probability calibration checks.

Real calibration needs out-of-sample buckets (predicted freq vs realized).
Not implemented until a labeled library exists.
"""
from __future__ import annotations

from typing import Dict


def calibration_status() -> Dict[str, str]:
    return {
        "status": "not_implemented",
        "reason": "Requires labeled historical library and out-of-sample evaluation.",
        "next_step": "Build PatternStore from OHLC + fixed outcomes, then bucket by similarity.",
    }
