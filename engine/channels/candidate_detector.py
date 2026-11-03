"""Heuristic channel candidates from OHLC candles (research aid, not official rule)."""
from __future__ import annotations
from math import isfinite
from typing import Any, Dict, List, Sequence


def _clean(candles: Sequence[Dict[str, Any]]) -> List[Dict[str, float]]:
    out=[]
    for i,c in enumerate(candles):
        try: o,h,l,cl=(float(c[k]) for k in ('open','high','low','close'))
        except (KeyError,TypeError,ValueError) as e: raise ValueError(f'Invalid OHLC at index {i}') from e
        if not all(map(isfinite,(o,h,l,cl))) or h<l or not l<=o<=h or not l<=cl<=h:
            raise ValueError(f'Invalid OHLC bounds at index {i}')
        out.append({'open':o,'high':h,'low':l,'close':cl})
    return out


def _pivots(values: Sequence[float], left: int, right: int, kind: str):
    result=[]
    for i in range(left,len(values)-right):
        w=values[i-left:i+right+1]
        if kind=='high' and values[i]==max(w) and values[i]>max(values[i-left:i]) and values[i]>=max(values[i+1:i+right+1]): result.append(i)
        if kind=='low' and values[i]==min(w) and values[i]<min(values[i-left:i]) and values[i]<=min(values[i+1:i+right+1]): result.append(i)
    return result


def detect_channel_candidates(candles: Sequence[Dict[str, Any]], *, left: int=2, right: int=2,
                             max_pivot_pairs: int=12, tolerance_ratio: float=.08) -> List[Dict[str, Any]]:
    """Pair confirmed pivot highs/lows and score parallel, repeatedly touched envelopes."""
    if left<1 or right<1: raise ValueError('left and right must be >= 1')
    if max_pivot_pairs<1: raise ValueError('max_pivot_pairs must be >= 1')
    if not 0<=tolerance_ratio<=.25: raise ValueError('tolerance_ratio must be in [0, .25]')
    cs=_clean(candles)
    if len(cs)<left+right+3: return []
    highs=[c['high'] for c in cs]; lows=[c['low'] for c in cs]
    ph=_pivots(highs,left,right,'high'); pl=_pivots(lows,left,right,'low')
    pivots=sorted([(i,highs[i],'H') for i in ph]+[(i,lows[i],'L') for i in pl])
    candidates=[]; seen=set()
    for start in range(max(0,len(pivots)-max_pivot_pairs),len(pivots)-2):
        subset=pivots[start:]
        if len(subset)<3: continue
        idx0=subset[0][0]; idx1=subset[-1][0]
        lower=min(p for _,p,k in subset if k=='L') if any(k=='L' for *_,k in subset) else min(c['low'] for c in cs[idx0:idx1+1])
        upper=max(p for _,p,k in subset if k=='H') if any(k=='H' for *_,k in subset) else max(c['high'] for c in cs[idx0:idx1+1])
        amp=upper-lower
        if amp<=0: continue
        key=(round(lower,8),round(upper,8),idx0,idx1)
        if key in seen: continue
        seen.add(key); tol=amp*tolerance_ratio
        span=cs[idx0:idx1+1]
        lowtouch=sum(c['low']<=lower+tol for c in span); hitouch=sum(c['high']>=upper-tol for c in span)
        inside=sum(lower-tol<=c['close']<=upper+tol for c in span)
        score=2*min(lowtouch,3)+2*min(hitouch,3)+inside/max(1,len(span))
        candidates.append({'candidate_id':f'pivot_channel_{len(candidates)+1}','lower':lower,'upper':upper,'amplitude':amp,
          'start_index':idx0,'end_index':idx1,'pivot_count':len(subset),'quality_score':round(score,4),
          'evidence':{'lower_touches':lowtouch,'upper_touches':hitouch,'contained_closes':inside,'bars':len(span),'tolerance':tol},
          'status':'experimental_candidate_not_official_channel','limitations':['Heuristic pivot envelope; not a confirmed official Fimathe channel.',
          'Quality score is a ranking aid, not probability or trade validation.','Visual review and Fimathe source-rule confirmation remain required.']})
    return sorted(candidates,key=lambda x:(x['quality_score'],x['pivot_count']),reverse=True)


def generate_channel_candidates(candles: List[Dict[str, Any]], *, window_sizes=(8,12,20), boundary_tolerance_ratio=.04):
    """Legacy trailing-range candidates retained for backward compatibility."""
    cs=_clean(candles)
    if len(cs)<3: return []
    if not 0<=boundary_tolerance_ratio<=.25: raise ValueError('boundary_tolerance_ratio must be between 0 and 0.25')
    out=[]; seen=set()
    for n in window_sizes:
        if not isinstance(n,int) or n<3: continue
        size=min(n,len(cs)); subset=cs[-size:]; lo=min(c['low'] for c in subset); hi=max(c['high'] for c in subset)
        if hi<=lo: continue
        key=(round(lo,10),round(hi,10),size)
        if key in seen: continue
        seen.add(key); tol=(hi-lo)*boundary_tolerance_ratio
        out.append({'candidate_id':f'range_{size}_{len(out)+1}','lower':lo,'upper':hi,'amplitude':hi-lo,'window_candles':size,
          'evidence':{'lower_boundary_near_touches':sum(c['low']<=lo+tol for c in subset),'upper_boundary_near_touches':sum(c['high']>=hi-tol for c in subset),'tolerance_price':tol},
          'status':'experimental_candidate_not_official_channel','limitations':['Trailing high/low envelope; not verified Fimathe A/B construction.']})
    return out
