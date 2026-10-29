"""Comando padrao para grafico puro: build_overlay(L, H) retorna pacote completo."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from engine.channels.geometry import (
    create_reference_channel, build_neutral_zone,
    level_50_of_channel, level_50_of_two_channels, project_levels,
)
from engine.cycles.projections import create_expansion, subcycle_from_entry
from engine.mapping.higher_tf import subdivide_interval
from engine.core.models import TrendDirection

@dataclass
class OverlayResult:
    symbol: str
    timeframe: str
    reference_lower: float
    reference_upper: float
    amplitude: float
    direction_bias: str
    neutral_lower: float
    neutral_upper: float
    level_50_reference: float
    level_50_neutral: float
    level_50_union: float
    stop: float
    expansions_down: List[Dict[str, float]]
    expansions_up: List[Dict[str, float]]
    subcycle: Optional[float]
    entry_hypothesis: Optional[float]
    fatiamento_depth2: List[float]
    current_price: Optional[float]
    position_vs_reference: str
    position_vs_neutral: str
    warnings: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def summary_text(self) -> str:
        lines = [
            f"=== Fimathe Overlay – {self.symbol} {self.timeframe} ===",
            f"Canal: {self.reference_lower:.5f} – {self.reference_upper:.5f}  amp={self.amplitude:.5f}",
            f"Zona Neutra: {self.neutral_lower:.5f} – {self.neutral_upper:.5f}",
            f"50% Ref/ZN/Uniao: {self.level_50_reference:.5f} / {self.level_50_neutral:.5f} / {self.level_50_union:.5f}",
            f"Stop: {self.stop:.5f}",
        ]
        for e in self.expansions_down:
            lines.append(f"  EXP {e['mult']}x down: {e['lower']:.5f}")
        if self.entry_hypothesis is not None:
            lines.append(f"Entrada: {self.entry_hypothesis:.5f}  Subciclo: {self.subcycle:.5f}")
        if self.current_price is not None:
            lines.append(f"Preco atual: {self.current_price:.5f} → {self.position_vs_reference} | {self.position_vs_neutral}")
        return "\n".join(lines)


def build_overlay(
    lower: float, upper: float, *,
    symbol: str = "UNKNOWN", timeframe: str = "M15",
    direction_bias: str = "down", current_price: Optional[float] = None,
    entry_offset: float = 0.00020,
) -> OverlayResult:
    warnings: List[str] = []
    notes = [
        "Canal de referencia informado explicitamente (construcao subjetiva).",
        "Nenhuma expansao e marcada como alvo oficial automaticamente.",
    ]
    if upper <= lower:
        raise ValueError("upper must be > lower")
    ref = create_reference_channel(lower, upper, timeframe=timeframe, source="user_or_visual")
    amp = ref.amplitude
    dir_enum = TrendDirection.DOWN if direction_bias == "down" else TrendDirection.UP
    neut_res = build_neutral_zone(ref, dir_enum)
    neut = neut_res.value
    warnings.extend(neut_res.warnings)
    r50 = level_50_of_channel(lower, upper).value
    n50 = level_50_of_channel(neut.lower, neut.upper).value
    u50 = level_50_of_two_channels(lower, upper, neut.lower, neut.upper).value
    stop = neut.upper if direction_bias == "down" else neut.lower
    expansions_down = []
    for m in [1.0, 1.5, 2.0]:
        exp = create_expansion(origin_price=lower, amplitude=amp, direction="down", multiplier=m)
        c = exp.value
        expansions_down.append({"mult": m, "lower": c.lower, "upper": c.upper})
    expansions_up = []
    proj = project_levels(upper, amp, "up", [1.0, 1.5, 2.0])
    for lv in proj.value:
        expansions_up.append({"mult": lv["multiplier"], "price": lv["price"]})
    entry_hyp = subcycle = None
    if direction_bias == "down":
        entry_hyp = round(lower - entry_offset, 5)
        sub = subcycle_from_entry(entry_hyp, amp, "down")
        subcycle = sub.value.price
    fat = subdivide_interval(lower, upper, depth=2)
    fat_levels = fat.value.levels if fat.value else []
    pos_ref = pos_neut = "desconhecido"
    if current_price is not None:
        if current_price > upper: pos_ref = "ACIMA do canal"
        elif current_price < lower: pos_ref = "ABAIXO do canal (rompimento)"
        else: pos_ref = "DENTRO do canal"
        if current_price > neut.upper: pos_neut = "ACIMA da zona neutra"
        elif current_price < neut.lower: pos_neut = "ABAIXO da zona neutra"
        else: pos_neut = "DENTRO da zona neutra"
    return OverlayResult(
        symbol=symbol, timeframe=timeframe,
        reference_lower=lower, reference_upper=upper, amplitude=amp,
        direction_bias=direction_bias,
        neutral_lower=neut.lower, neutral_upper=neut.upper,
        level_50_reference=r50, level_50_neutral=n50, level_50_union=u50,
        stop=stop, expansions_down=expansions_down, expansions_up=expansions_up,
        subcycle=subcycle, entry_hypothesis=entry_hyp,
        fatiamento_depth2=fat_levels, current_price=current_price,
        position_vs_reference=pos_ref, position_vs_neutral=pos_neut,
        warnings=warnings, notes=notes,
    )
