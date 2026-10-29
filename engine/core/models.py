"""
Typed models for the Fimathe mathematical engine.
Every CalculationResult carries the parameters and rule version used.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional, List, Dict


class TrendDirection(str, Enum):
    UP = "up"
    DOWN = "down"
    SIDEWAYS = "sideways"
    UNKNOWN = "unknown"


class ConfirmationStatus(str, Enum):
    CONFIRMED = "confirmed"
    PROBABLE = "probable"
    PENDING = "pending"
    INVALID = "invalid"


class RuleClarity(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    PROVISIONAL = "provisional"
    UNVERIFIED = "unverified"


@dataclass(frozen=True)
class MarketCandle:
    """OHLC candle with explicit open/close times to prevent future leak."""
    timestamp_open: datetime
    timestamp_close: datetime
    open: float
    high: float
    low: float
    close: float
    timeframe: str
    is_closed: bool = True

    def __post_init__(self):
        if self.high < self.low:
            raise ValueError("high < low")


@dataclass(frozen=True)
class SwingPoint:
    price: float
    kind: str
    candle_index: int
    availability_time: datetime
    confirmed: bool = False


@dataclass
class TrendAssessment:
    direction: TrendDirection
    status: ConfirmationStatus
    swings: List[SwingPoint] = field(default_factory=list)
    method: str = "manual"
    notes: str = ""
    rule_version: str = "0.2"


@dataclass(frozen=True)
class ReferenceChannel:
    lower: float
    upper: float
    source: str = "user"
    timeframe: str = "M15"
    label: str = "reference"
    created_at: Optional[datetime] = None
    study_version: str = "0.2"

    @property
    def amplitude(self) -> float:
        return self.upper - self.lower

    def validate(self) -> "RuleValidation":
        warnings = []
        if self.upper <= self.lower:
            warnings.append("upper <= lower")
        return RuleValidation(
            ok=len(warnings) == 0,
            warnings=warnings,
            rule_id="channel_geometry",
            clarity=RuleClarity.MEDIUM,
        )


@dataclass(frozen=True)
class NeutralChannel:
    lower: float
    upper: float
    reference: ReferenceChannel
    direction_of_reference: TrendDirection = TrendDirection.DOWN
    rule_version: str = "0.2"

    @property
    def amplitude(self) -> float:
        return self.upper - self.lower


@dataclass(frozen=True)
class ChannelCycle:
    origin_price: float
    direction: str
    multiplier: float
    amplitude: float
    formula: str
    lower: float
    upper: float
    label: str = ""
    rule_version: str = "0.2"
    confirmed_target: bool = False


@dataclass(frozen=True)
class SubcycleLevel:
    price: float
    origin: str
    related_amplitude: float
    rule_version: str = "0.2"


@dataclass
class CalculationResult:
    value: Any
    parameters: Dict[str, Any]
    rule_id: str
    rule_version: str
    clarity: RuleClarity = RuleClarity.MEDIUM
    warnings: List[str] = field(default_factory=list)
    notes: str = ""

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)


@dataclass
class RuleValidation:
    ok: bool
    warnings: List[str]
    rule_id: str
    clarity: RuleClarity
    details: Dict[str, Any] = field(default_factory=dict)
