import pytest
from engine.channels.candidate_detector import detect_channel_candidates
from engine.price_action.breakouts import classify_breakout
from engine.mapping.higher_tf import align_timeframes


def candles(closes, highs=None, lows=None):
    highs=highs or [x+1 for x in closes]; lows=lows or [x-1 for x in closes]
    return [{'open':x,'high':h,'low':l,'close':x,'is_closed':True} for x,h,l in zip(closes,highs,lows)]


def test_detector_returns_explicit_experimental_candidates():
    cs=candles([5,7,9,7,5,7,9,7,5,7,9,7,5])
    result=detect_channel_candidates(cs,left=1,right=1)
    assert result and result[0]['status']=='experimental_candidate_not_official_channel'
    assert result[0]['quality_score']>=0


def test_detector_rejects_bad_candle():
    with pytest.raises(ValueError): detect_channel_candidates([{'open':2,'high':1,'low':0,'close':1}]*5)


def test_breakout_requires_closed_close_beyond_boundary():
    r=classify_breakout(candles([9,10,11],highs=[10,11,12],lows=[8,9,10]),0,10)
    assert r['confirmed'] is True and r['direction']=='UP' and r['decision']=='WAIT'


def test_open_candle_ignored():
    r=classify_breakout([{'open':10,'high':12,'low':9,'close':11,'is_closed':False}],0,10)
    assert r['state']=='UNAVAILABLE'


def test_mtf_conflict_never_creates_entry():
    r=align_timeframes('up','down','up')
    assert r['status']=='CONFLICTING' and r['decision']=='WAIT' and not r['entry_confirmed']
