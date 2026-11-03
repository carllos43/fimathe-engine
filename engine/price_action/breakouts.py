"""Closed-candle channel break and retest classification (research aid).

Does not generate entries. Decision remains WAIT until strategy rules validate.
"""
from __future__ import annotations
from math import isfinite
from typing import Any, Dict, Sequence


def classify_breakout(candles: Sequence[Dict[str, Any]], lower: float, upper: float, *,
                    tolerance: float=0.0, retest_tolerance: float|None=None,
                    structure_bias: str='unknown') -> Dict[str, Any]:
    if not all(isfinite(float(x)) for x in (lower,upper,tolerance)) or upper<=lower or tolerance<0:
        raise ValueError('Require finite channel bounds, upper > lower, and tolerance >= 0')
    rt=tolerance if retest_tolerance is None else float(retest_tolerance)
    if not isfinite(rt) or rt<0: raise ValueError('retest_tolerance must be finite and >= 0')
    closed=[]
    for i,c in enumerate(candles):
        if not c.get('is_closed',True): continue
        try: o,h,l,cl=(float(c[k]) for k in ('open','high','low','close'))
        except (KeyError,TypeError,ValueError) as e: raise ValueError(f'Invalid OHLC at {i}') from e
        if not all(isfinite(x) for x in (o,h,l,cl)) or h<l or not l<=o<=h or not l<=cl<=h: raise ValueError(f'Invalid OHLC at {i}')
        closed.append({'open':o,'high':h,'low':l,'close':cl})
    if not closed: return {'state':'UNAVAILABLE','direction':'NONE','confirmed':False,'retest':False,'decision':'WAIT','reason':'No closed candles'}
    prev=closed[-2] if len(closed)>1 else None; last=closed[-1]
    direction='UP' if last['close']>upper+tolerance else 'DOWN' if last['close']<lower-tolerance else 'NONE'
    attempt=(last['high']>upper+tolerance or last['low']<lower-tolerance) and direction=='NONE'
    if direction=='NONE': state='ATTEMPT' if attempt else 'NONE'; retest=False
    else:
        boundary=upper if direction=='UP' else lower
        retest=bool(prev and ((prev['low']<=boundary+rt and last['close']>boundary) if direction=='UP' else (prev['high']>=boundary-rt and last['close']<boundary)))
        state='RETEST_CONFIRMED' if retest else 'CONFIRMED'
    aligned=(structure_bias.lower() in ('bullish','up','uptrend') if direction=='UP' else structure_bias.lower() in ('bearish','down','downtrend') if direction=='DOWN' else False)
    return {'state':state,'direction':direction,'confirmed':direction!='NONE','retest':retest,
      'structure_bias':structure_bias,'structure_aligned':aligned,'decision':'WAIT',
      'reason':'Closed-candle channel break only; no entry trigger validated. Retest and structure are separate evidence.' if direction!='NONE' else 'No close beyond channel boundary.',
      'last_closed_candle':last}
