"""End-to-end OHLC analysis orchestration (experimental, deterministic).

This consumes extracted candles. It does not OCR chart screenshots or create trade
orders. All channel selection and breakout/retest labels are heuristic research.
"""
from __future__ import annotations
from math import isfinite
from typing import Any, Dict, Sequence
from engine.channels.candidate_detector import detect_channel_candidates


def _validate(candles: Sequence[Dict[str, Any]]) -> list[dict[str, float | bool]]:
    if not candles: raise ValueError('candles cannot be empty')
    result=[]
    for i,c in enumerate(candles):
        try: o,h,l,cl=[float(c[k]) for k in ('open','high','low','close')]
        except (KeyError,TypeError,ValueError) as e: raise ValueError(f'invalid OHLC at index {i}') from e
        if not all(isfinite(x) for x in (o,h,l,cl)) or h<l or not l<=o<=h or not l<=cl<=h:
            raise ValueError(f'invalid OHLC bounds at index {i}')
        result.append({'open':o,'high':h,'low':l,'close':cl,'is_closed':bool(c.get('is_closed',True))})
    return result


def _state(candles, channel, tolerance_ratio=.08):
    lower,upper=channel['lower'],channel['upper']; amp=upper-lower; tol=amp*tolerance_ratio
    latest=candles[-1]
    if not latest['is_closed']: return 'pending_open_candle'
    if latest['close']>upper: return 'confirmed_close_above_candidate'
    if latest['close']<lower: return 'confirmed_close_below_candidate'
    prior_break=None
    for c in candles[:-1]:
        if c['is_closed'] and c['close']>upper: prior_break='up'
        elif c['is_closed'] and c['close']<lower: prior_break='down'
    if prior_break=='up' and latest['low']<=upper+tol and latest['close']>upper:
        return 'possible_retest_up_closed_not_entry'
    if prior_break=='down' and latest['high']>=lower-tol and latest['close']<lower:
        return 'possible_retest_down_closed_not_entry'
    return 'inside_candidate_channel_or_no_retest'


def _structure(candles, left=2, right=2):
    highs=[c['high'] for c in candles]; lows=[c['low'] for c in candles]
    ph=[]; pl=[]
    for i in range(left,len(candles)-right):
        if highs[i]>max(highs[i-left:i]) and highs[i]>=max(highs[i+1:i+right+1]): ph.append((i,highs[i]))
        if lows[i]<min(lows[i-left:i]) and lows[i]<=min(lows[i+1:i+right+1]): pl.append((i,lows[i]))
    labels=[]; prevh=prevl=None
    for kind,idx,price in sorted([( 'H',i,p) for i,p in ph]+[( 'L',i,p) for i,p in pl], key=lambda x:x[1]):
        if kind=='H':
            labels.append('HH' if prevh is not None and price>prevh else 'LH' if prevh is not None else 'H?'); prevh=price
        else:
            labels.append('HL' if prevl is not None and price>prevl else 'LL' if prevl is not None else 'L?'); prevl=price
    recent=labels[-6:]; bull=('HH' in recent and 'HL' in recent); bear=('LH' in recent and 'LL' in recent)
    return {'swing_labels':labels,'bias':'bullish' if bull and not bear else 'bearish' if bear and not bull else 'mixed_or_unclear',
            'status':'heuristic_swing_structure'}


def analyze_complete(candles: Sequence[Dict[str, Any]], *, timeframe='unknown',
                   higher_timeframe: Sequence[Dict[str, Any]]|None=None,
                   middle_timeframe: Sequence[Dict[str, Any]]|None=None,
                   pivot_left=2, pivot_right=2) -> Dict[str, Any]:
    """Analyze candle data and optional higher/middle timeframe OHLC sequences."""
    cs=_validate(candles)
    candidates=detect_channel_candidates(cs,left=pivot_left,right=pivot_right)
    selected=candidates[0] if candidates else None
    lower=_structure(_validate(higher_timeframe)) if higher_timeframe else {'bias':'not_supplied','status':'missing'}
    middle=_structure(_validate(middle_timeframe)) if middle_timeframe else {'bias':'not_supplied','status':'missing'}
    lower_bias=lower.get('bias'); middle_bias=middle.get('bias'); local=_structure(cs)
    alignment='unavailable'
    if lower_bias!='not_supplied' and middle_bias!='not_supplied':
        alignment='aligned' if lower_bias==middle_bias==local['bias'] and local['bias'] in ('bullish','bearish') else 'conflict_or_unclear'
    scenario=_state(cs,selected) if selected else 'no_channel_candidate'
    return {'timeframe':timeframe,'candles_count':len(cs),'channel_candidates':candidates,
      'selected_channel':selected,'selection_status':'top_heuristic_candidate_requires_visual_and_rule_review' if selected else 'no_candidate',
      'breakout_retest_state':scenario,'structure':local,
      'multi_timeframe':{'higher':lower,'middle':middle,'lower':local,'alignment':alignment,
        'status':'heuristic_structure_not_official_fimathe_rule'},
      'entry':{'status':'not_generated','price':None,'reason':'A candidate channel or breakout/retest is not an entry trigger.'},
      'stop':{'status':'not_generated','price':None,'reason':'No validated strategy-specific invalidation/buffer supplied.'},
      'warnings':['Channel candidate detector and structure labels are heuristic; validate against annotated Fimathe examples.',
       'OHLC must be extracted by a vision/OCR layer; this function does not read pixels.',
       'Retest label is descriptive, not a confirmed trade setup or recommendation.']}
