"""
Cycle models and expansions.
Formula of successive cycles (C2 = CA+C1 etc.) remains provisional.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
from engine.core.models import ChannelCycle, CalculationResult, RuleClarity, ReferenceChannel


@dataclass
class CycleModel:
    name: str
    description: str
    active: bool = False


LINEAR_CUMULATIVE = CycleModel(
    name="linear_cumulative",
    description="C1 = CA; C2 = CA + C1; C3 = CA + C1 + C2; ... (interpretação possível)",
    active=False,
)

DOUBLING = CycleModel(
    name="doubling",
    description="Cada ciclo dobra a amplitude do anterior (outra leitura possível)",
    active=False,
)


def create_expansion(
    origin_price: float,
    amplitude: float,
    direction: str,
    multiplier: float = 1.0,
    formula: str = "origin ± multiplier * amplitude",
    label: str = "",
) -> CalculationResult:
    if direction not in ("up", "down"):
        return CalculationResult(
            value=None,
            parameters={},
            rule_id="R_expansion",
            rule_version="0.2",
            clarity=RuleClarity.HIGH,
            warnings=["direction must be 'up' or 'down'"],
        )

    sign = 1.0 if direction == "up" else -1.0
    if direction == "up":
        lower = origin_price
        upper = origin_price + multiplier * amplitude
    else:
        upper = origin_price
        lower = origin_price - multiplier * amplitude

    cycle = ChannelCycle(
        origin_price=origin_price,
        direction=direction,
        multiplier=multiplier,
        amplitude=amplitude,
        formula=formula,
        lower=lower,
        upper=upper,
        label=label or f"expansion_{multiplier}x",
        confirmed_target=False,
    )

    return CalculationResult(
        value=cycle,
        parameters={
            "origin_price": origin_price,
            "amplitude": amplitude,
            "direction": direction,
            "multiplier": multiplier,
            "formula": formula,
        },
        rule_id="R_expansion",
        rule_version="0.2",
        clarity=RuleClarity.MEDIUM,
        warnings=["Expansão criada; não é alvo confirmado automaticamente"],
    )


def subcycle_from_entry(
    entry_price: float,
    amplitude: float,
    direction: str = "down",
) -> CalculationResult:
    if direction == "down":
        price = entry_price - amplitude
        formula = "entry - amplitude"
    else:
        price = entry_price + amplitude
        formula = "entry + amplitude (PROVISIONAL for uptrend)"

    from engine.core.models import SubcycleLevel
    level = SubcycleLevel(
        price=price,
        origin=f"entry={entry_price}",
        related_amplitude=amplitude,
    )
    warnings = []
    if direction == "up":
        warnings.append("Fórmula de subciclo em alta é provisional")

    return CalculationResult(
        value=level,
        parameters={
            "entry_price": entry_price,
            "amplitude": amplitude,
            "direction": direction,
            "formula": formula,
        },
        rule_id="B_subcycle",
        rule_version="0.2",
        clarity=RuleClarity.MEDIUM if direction == "down" else RuleClarity.PROVISIONAL,
        warnings=warnings,
    )
