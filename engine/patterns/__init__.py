"""Pattern features and similarity (research layer).

Does not claim official Fimathe probability. Requires OHLC series.
"""
from engine.patterns.features import ScenarioFeatures, extract_features
from engine.patterns.similarity import similarity_score, rank_neighbors

__all__ = [
    "ScenarioFeatures",
    "extract_features",
    "similarity_score",
    "rank_neighbors",
]
