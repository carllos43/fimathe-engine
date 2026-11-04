import pytest
from engine.patterns.features import extract_features
from engine.patterns.similarity import rank_neighbors, similarity_score
from engine.patterns.pattern_store import PatternStore, StoredPattern
from engine.probability.outcomes import OutcomeLabel, classify_outcome
from engine.probability.estimator import estimate_frequencies
from engine.probability.confidence import wilson_interval, sample_quality
from engine.analysis.probability_report import build_probability_report


def _c(closes):
    return [{"open": x, "high": x + 0.5, "low": x - 0.5, "close": x, "is_closed": True} for x in closes]


def test_extract_features_position_r():
    cs = _c([10, 11, 10, 12, 11, 10, 11, 12, 11, 10.5])
    feat = extract_features(cs, lower=10.0, upper=12.0)
    assert feat.amplitude == 2.0
    assert abs(feat.price_position_r - 0.25) < 1e-9
    assert feat.last_close_beyond == "inside"


def test_similarity_identical_is_one():
    cs = _c([10, 11, 10, 12, 11, 10, 11, 12, 11, 10.5])
    a = extract_features(cs, lower=10.0, upper=12.0)
    assert similarity_score(a, a) == 1.0


def test_rank_neighbors_orders():
    base = extract_features(_c([10, 11, 10, 12, 11, 10, 11, 12, 11, 10.5]), lower=10.0, upper=12.0)
    near = extract_features(_c([10, 11, 10, 12, 11, 10, 11, 12, 11, 10.6]), lower=10.0, upper=12.0)
    far_cs = []
    for x in [8, 9, 10, 11, 12, 13, 14, 15, 16, 17]:
        far_cs.append({"open": x - 0.2, "high": x + 0.3, "low": x - 0.4, "close": x, "is_closed": True})
    far = extract_features(far_cs, lower=8.0, upper=12.0)
    ranks = rank_neighbors(base, [far, near], top_k=2)
    assert ranks[0][0] == 1
    assert ranks[0][1] > ranks[1][1]


def test_classify_outcome_up_first():
    future = [
        {"high": 10.5, "low": 9.5},
        {"high": 11.2, "low": 10.0},
    ]
    assert classify_outcome(future, up_target=11.0, down_target=9.0) == OutcomeLabel.UP_FIRST


def test_classify_outcome_lateral():
    future = [{"high": 10.2, "low": 9.8} for _ in range(5)]
    assert classify_outcome(future, up_target=12.0, down_target=8.0) == OutcomeLabel.LATERAL


def test_estimate_frequencies_and_wilson():
    est = estimate_frequencies(["up_first", "up_first", "down_first", "lateral"])
    assert est.n == 4
    assert abs(est.frequencies["up_first"] - 0.5) < 1e-9
    low, high = wilson_interval(2, 4)
    assert 0 <= low <= 0.5 <= high <= 1
    assert sample_quality(4)["quality"] == "very_low"


def test_report_without_store():
    cs = _c([10, 11, 10, 12, 11, 10, 11, 12, 11, 10.5])
    rep = build_probability_report(cs, lower=10.0, upper=12.0, store=None)
    assert rep["historical"]["status"] == "no_historical_library"
    assert rep["entry"]["status"] == "not_generated"


def test_report_with_store():
    cs = _c([10, 11, 10, 12, 11, 10, 11, 12, 11, 10.5])
    feat = extract_features(cs, lower=10.0, upper=12.0)
    store = PatternStore()
    store.add(StoredPattern(features=feat, outcome="up_first", timeframe="M15"))
    store.add(
        StoredPattern(
            features=extract_features(_c([10, 11, 10, 12, 11, 10, 11, 12, 11, 10.4]), lower=10.0, upper=12.0),
            outcome="down_first",
            timeframe="M15",
        )
    )
    rep = build_probability_report(cs, lower=10.0, upper=12.0, store=store, top_k=2)
    assert rep["historical"]["library_size"] == 2
    assert rep["historical"]["estimate"]["n"] == 2
