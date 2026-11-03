import pytest
from engine.analysis.complete_pipeline import analyze_complete


def candles(vals):
    return [{'open':v,'high':v+1,'low':v-1,'close':v,'is_closed':True} for v in vals]


def test_pipeline_returns_explicit_no_entry_and_mtf_missing():
    result=analyze_complete(candles([10,12,9,13,8,14,9,15,10,16,11,17]),timeframe='5m')
    assert result['entry']['status']=='not_generated'
    assert result['multi_timeframe']['alignment']=='unavailable'
    assert 'channel_candidates' in result


def test_pipeline_rejects_nonfinite_ohlc():
    with pytest.raises(ValueError):
        analyze_complete([{'open':1,'high':float('nan'),'low':0,'close':1}])


def test_pipeline_does_not_call_open_candle_breakout_confirmed():
    cs=candles([10,12,9,13,8,14,9,15,10,16,11,17])
    cs[-1]['is_closed']=False
    result=analyze_complete(cs)
    if result['selected_channel']:
        assert result['breakout_retest_state']=='pending_open_candle'
