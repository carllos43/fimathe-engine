"""
Pure geometric functions for Fimathe channels.
All formulas are explicit; no automatic target selection.
"""

from __future__ import annotations

from typing import List, Optional
from engine.core.models import (
    ReferenceChannel,
    NeutralChannel,
    TrendDirection,
    CalculationResult,
    RuleClarity,
)


def channel_amplitude(lower: float, upper: float) -> CalculationResult:
    """amplitude = H - L"""
    if upper < lower:
        return CalculationResult(
            value=None,
            parameters={"lower": lower, "upper": upper},
            rule_id="R_amplitude",
            rule_version="0.2",
            clarity=RuleClarity.HIGH,
            warnings=["upper < lower"],
        )
    amp = upper - lower
    return CalculationResult(
        value=amp,
        parameters={"lower": lower, "upper": upper},
        rule_id="R_amplitude",
        rule_version="0.2",
        clarity=RuleClarity.HIGH,
    )


def build_neutral_zone(
    reference: ReferenceChannel,
    direction_of_reference: TrendDirection = TrendDirection.DOWN,
) -> CalculationResult:
    """Zona neutra adjacente com a mesma amplitude."""
    amp = reference.amplitude
    if direction_of_reference == TrendDirection.DOWN:
        n_lower = reference.upper
        n_upper = reference.upper + amp
        formula = "neutral_lower = H; neutral_upper = H + amplitude"
    elif direction_of_reference == TrendDirection.UP:
        n_lower = reference.lower - amp
        n_upper = reference.lower
        formula = "PROVISIONAL symmetric: neutral_upper = L; neutral_lower = L - amplitude"
    else:
        return CalculationResult(
            value=None,
            parameters={"reference": (reference.lower, reference.upper)},
            rule_id="B_neutral_zone",
            rule_version="0.2",
            clarity=RuleClarity.PROVISIONAL,
            warnings=["direction must be UP or DOWN to build neutral zone"],
        )

    neutral = NeutralChannel(
        lower=n_lower,
        upper=n_upper,
        reference=reference,
        direction_of_reference=direction_of_reference,
    )
    warnings = []
    if direction_of_reference == TrendDirection.UP:
        warnings.append(
            "Construção da zona neutra para tendência de alta é provisional"
        )

    return CalculationResult(
        value=neutral,
        parameters={
            "reference_lower": reference.lower,
            "reference_upper": reference.upper,
            "amplitude": amp,
            "direction": direction_of_reference.value,
            "formula": formula,
        },
        rule_id="B_neutral_zone",
        rule_version="0.2",
        clarity=RuleClarity.MEDIUM if direction_of_reference == TrendDirection.DOWN else RuleClarity.PROVISIONAL,
        warnings=warnings,
        notes="Stop tipicamente além do limite externo da zona neutra",
    )


def level_50_of_channel(lower: float, upper: float) -> CalculationResult:
    """Nível de 50% de um único canal."""
    mid = (lower + upper) / 2.0
    return CalculationResult(
        value=mid,
        parameters={"lower": lower, "upper": upper, "formula": "(L + H) / 2"},
        rule_id="R_50_channel",
        rule_version="0.2",
        clarity=RuleClarity.HIGH,
    )


def level_50_of_two_channels(
    ref_lower: float,
    ref_upper: float,
    neutral_lower: float,
    neutral_upper: float,
) -> CalculationResult:
    """Nível de 50% da região formada pelos dois canais."""
    overall_lower = min(ref_lower, neutral_lower)
    overall_upper = max(ref_upper, neutral_upper)
    mid = (overall_lower + overall_upper) / 2.0
    return CalculationResult(
        value=mid,
        parameters={
            "ref_lower": ref_lower,
            "ref_upper": ref_upper,
            "neutral_lower": neutral_lower,
            "neutral_upper": neutral_upper,
            "overall_lower": overall_lower,
            "overall_upper": overall_upper,
            "formula": "(min(L) + max(H)) / 2",
        },
        rule_id="B_50_two_channels",
        rule_version="0.2",
        clarity=RuleClarity.MEDIUM,
        warnings=[
            "A transcrição não define qual nível de 50% prevalece em cada contexto."
        ],
    )


def project_levels(
    origin: float,
    amplitude: float,
    direction: str,
    multipliers: Optional[List[float]] = None,
) -> CalculationResult:
    """Projeções parametrizadas (1, 1.5, 2 ciclos etc.)."""
    if multipliers is None:
        multipliers = [1.0, 1.5, 2.0]
    if direction not in ("up", "down"):
        return CalculationResult(
            value=None,
            parameters={"origin": origin, "amplitude": amplitude, "direction": direction},
            rule_id="R_project",
            rule_version="0.2",
            clarity=RuleClarity.HIGH,
            warnings=["direction must be 'up' or 'down'"],
        )

    sign = 1.0 if direction == "up" else -1.0
    levels = []
    for m in multipliers:
        target = origin + sign * m * amplitude
        levels.append({
            "multiplier": m,
            "price": target,
            "formula": f"origin {'+' if sign > 0 else '-'} {m} * amplitude",
        })

    return CalculationResult(
        value=levels,
        parameters={
            "origin": origin,
            "amplitude": amplitude,
            "direction": direction,
            "multipliers": multipliers,
        },
        rule_id="R_project",
        rule_version="0.2",
        clarity=RuleClarity.MEDIUM,
        warnings=["Nenhum alvo é marcado como oficial automaticamente."],
        notes="Multiplicadores configuráveis; padrão 1 / 1.5 / 2",
    )


def create_reference_channel(
    lower: float,
    upper: float,
    timeframe: str = "M15",
    source: str = "user",
    label: str = "reference",
) -> ReferenceChannel:
    """Factory that always requires explicit limits (subjective construction)."""
    return ReferenceChannel(
        lower=lower,
        upper=upper,
        source=source,
        timeframe=timeframe,
        label=label,
    )
