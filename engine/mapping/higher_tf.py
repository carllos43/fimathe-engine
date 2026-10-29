"""Higher-timeframe mapping and pure mathematical subdivision (fatiamento)."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from engine.core.models import CalculationResult, RuleClarity

@dataclass
class HigherTimeframeMap:
    timeframe_ref: str
    top: float
    bottom: float
    channel_lower: float
    channel_upper: float
    amplitude: float
    period_open: Optional[datetime] = None
    projected_levels: List[Dict[str, Any]] = field(default_factory=list)
    subdivisions: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    study_version: str = "0.2"
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timeframe_ref": self.timeframe_ref,
            "top": self.top, "bottom": self.bottom,
            "channel_lower": self.channel_lower, "channel_upper": self.channel_upper,
            "amplitude": self.amplitude,
            "period_open": self.period_open.isoformat() if self.period_open else None,
            "projected_levels": self.projected_levels,
            "subdivisions": self.subdivisions,
            "created_at": self.created_at.isoformat(),
            "study_version": self.study_version,
            "notes": self.notes,
        }

@dataclass
class SubdivisionResult:
    levels: List[float]
    details: List[Dict[str, Any]]
    depth: int
    origin_lower: float
    origin_upper: float
    nomenclature: str = "Fimathe 350"
    math_confirmation: str = "pending"


def subdivide_interval(lower: float, upper: float, depth: int = 1) -> CalculationResult:
    """Subdivisao sucessiva em metades. Nomenclatura: Fimathe 350 (math pending)."""
    if depth < 1 or upper <= lower:
        return CalculationResult(
            value=None, parameters={"lower": lower, "upper": upper, "depth": depth},
            rule_id="fatiamento", rule_version="0.2", clarity=RuleClarity.HIGH,
            warnings=["depth must be >= 1 and upper > lower"],
        )
    n_parts = 2 ** depth
    step = (upper - lower) / n_parts
    levels = [round(lower + i * step, 10) for i in range(n_parts + 1)]
    levels[0], levels[-1] = lower, upper
    details = [{"index": i, "price": p, "origin": "original_bound" if i in (0, len(levels)-1) else f"subdivision_depth_{depth}", "fraction": i / n_parts} for i, p in enumerate(levels)]
    result = SubdivisionResult(levels=levels, details=details, depth=depth, origin_lower=lower, origin_upper=upper)
    return CalculationResult(
        value=result,
        parameters={"lower": lower, "upper": upper, "depth": depth, "n_parts": n_parts, "nomenclature": "Fimathe 350"},
        rule_id="fatiamento", rule_version="0.2", clarity=RuleClarity.MEDIUM,
        warnings=["Nomenclatura 'Fimathe 350' registrada. Correspondencia matematica exata pendente."],
    )


def build_higher_tf_map(
    timeframe_ref: str, top: float, bottom: float,
    channel_lower: Optional[float] = None, channel_upper: Optional[float] = None,
    period_open: Optional[datetime] = None,
    project_multipliers: Optional[List[float]] = None,
    subdivision_depth: int = 0,
) -> HigherTimeframeMap:
    cl = channel_lower if channel_lower is not None else bottom
    cu = channel_upper if channel_upper is not None else top
    amp = cu - cl
    projected = []
    if project_multipliers:
        from engine.channels.geometry import project_levels
        for direction in ("up", "down"):
            res = project_levels(cl if direction == "up" else cu, amp, direction, project_multipliers)
            if res.value:
                for lv in res.value:
                    projected.append({**lv, "direction": direction})
    subs = []
    if subdivision_depth >= 1:
        sub_res = subdivide_interval(cl, cu, subdivision_depth)
        if sub_res.value:
            subs = sub_res.value.details
    return HigherTimeframeMap(
        timeframe_ref=timeframe_ref, top=top, bottom=bottom,
        channel_lower=cl, channel_upper=cu, amplitude=amp,
        period_open=period_open, projected_levels=projected, subdivisions=subs,
    )


def context_between_timeframes(higher_map, lower_candles, lower_channels=None):
    inherited = {
        "channel_lower": higher_map.channel_lower,
        "channel_upper": higher_map.channel_upper,
        "projected_levels": higher_map.projected_levels,
        "subdivisions": higher_map.subdivisions,
        "amplitude": higher_map.amplitude,
    }
    candle_info, incomplete = [], []
    for c in lower_candles:
        info = {"timestamp_close": getattr(c, "timestamp_close", None), "is_closed": getattr(c, "is_closed", False), "close": getattr(c, "close", None)}
        if not info["is_closed"]:
            incomplete.append(info)
        candle_info.append(info)
    return {
        "inherited_from_higher_tf": inherited,
        "lower_tf_channels": lower_channels or [],
        "higher_period_open": higher_map.period_open.isoformat() if higher_map.period_open else None,
        "candle_confirmation_times": candle_info,
        "incomplete_data": incomplete,
        "warning": "Nunca use candles futuros nem trate candles abertos como fechados em simulacoes historicas",
    }
