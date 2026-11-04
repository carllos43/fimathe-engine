"""Frequency estimator from labeled neighbor outcomes."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Sequence

from engine.probability.confidence import sample_quality, wilson_interval


@dataclass(frozen=True)
class FrequencyEstimate:
    counts: Dict[str, int]
    n: int
    frequencies: Dict[str, float]
    intervals: Dict[str, tuple]
    quality: Dict[str, object]
    disclaimer: str

    def to_dict(self) -> Dict:
        return {
            "counts": self.counts,
            "n": self.n,
            "frequencies": self.frequencies,
            "intervals": {k: {"low": v[0], "high": v[1]} for k, v in self.intervals.items()},
            "quality": self.quality,
            "disclaimer": self.disclaimer,
        }


def estimate_frequencies(outcomes: Sequence[str]) -> FrequencyEstimate:
    """Count outcome labels and attach Wilson intervals + sample quality."""
    if not outcomes:
        return FrequencyEstimate(
            counts={},
            n=0,
            frequencies={},
            intervals={},
            quality=sample_quality(0),
            disclaimer="No outcomes supplied. Cannot estimate frequencies.",
        )
    labels = [str(o) for o in outcomes]
    ctr = Counter(labels)
    n = len(labels)
    freqs = {k: ctr[k] / n for k in ctr}
    intervals = {k: wilson_interval(ctr[k], n) for k in ctr}
    return FrequencyEstimate(
        counts=dict(ctr),
        n=n,
        frequencies=freqs,
        intervals=intervals,
        quality=sample_quality(n),
        disclaimer=(
            "Descriptive historical frequencies only. "
            "Not a calibrated probability of future price. "
            "Not financial advice. Require OHLC history and fixed outcome rules."
        ),
    )


def empty_report_placeholder() -> Dict:
    """Safe payload when no historical library exists yet."""
    return {
        "status": "no_historical_library",
        "message": "Load OHLC and labeled patterns before reporting frequencies.",
        "example_only": True,
        "see": "docs/probability/REFERENCE_SOURCES.md",
    }
