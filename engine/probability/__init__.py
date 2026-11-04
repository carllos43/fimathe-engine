"""Historical frequency estimation (research layer).

Frequencies are descriptive counts, not calibrated trading probabilities.
Small samples must expose uncertainty. Never invent outcomes without OHLC history.
"""
from engine.probability.outcomes import OutcomeLabel, classify_outcome
from engine.probability.estimator import FrequencyEstimate, estimate_frequencies
from engine.probability.confidence import wilson_interval, sample_quality

__all__ = [
    "OutcomeLabel",
    "classify_outcome",
    "FrequencyEstimate",
    "estimate_frequencies",
    "wilson_interval",
    "sample_quality",
]
