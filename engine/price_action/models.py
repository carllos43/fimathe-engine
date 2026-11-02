"""Typed models for the Price Action layer (docs/PRICE_ACTION_ENGINE.md)."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class InputQuality(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class MarketRegime(str, Enum):
    UPTREND = "UPTREND"
    DOWNTREND = "DOWNTREND"
    RANGE = "RANGE"
    TRANSITION = "TRANSITION"
    UNKNOWN = "UNKNOWN"


class TrendBias(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"
    UNKNOWN = "UNKNOWN"


class StructureStatus(str, Enum):
    INTACT = "INTACT"
    WEAKENING = "WEAKENING"
    BROKEN = "BROKEN"
    UNCLEAR = "UNCLEAR"


class BreakoutStatus(str, Enum):
    NONE = "NONE"
    ATTEMPT = "ATTEMPT"
    CONFIRMED = "CONFIRMED"
    RETEST_PENDING = "RETEST_PENDING"
    RETEST_CONFIRMED = "RETEST_CONFIRMED"
    FAILED = "FAILED"


class TradeDecision(str, Enum):
    BUY_SETUP = "BUY_SETUP"
    SELL_SETUP = "SELL_SETUP"
    WAIT = "WAIT"


class ConfluenceStatus(str, Enum):
    ALIGNED = "ALIGNED"
    CONFLICTING = "CONFLICTING"
    NEUTRAL = "NEUTRAL"
    UNAVAILABLE = "UNAVAILABLE"


class SwingType(str, Enum):
    HIGH = "HIGH"
    LOW = "LOW"


class SwingLabel(str, Enum):
    HH = "HH"
    HL = "HL"
    LH = "LH"
    LL = "LL"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class SwingPoint:
    index: int
    price: float
    swing_type: SwingType
    label: SwingLabel = SwingLabel.UNKNOWN
    confirmed_at_index: Optional[int] = None


@dataclass
class MarketStructure:
    swings: List[SwingPoint] = field(default_factory=list)
    sequence: List[str] = field(default_factory=list)
    bos: Optional[str] = None
    choch: Optional[str] = None
    structure_status: StructureStatus = StructureStatus.UNCLEAR


@dataclass
class TradePlan:
    decision: TradeDecision = TradeDecision.WAIT
    entry_type: Optional[str] = None
    entry: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profits: List[Dict[str, Any]] = field(default_factory=list)
    risk_reward: Optional[float] = None
    invalidation: Optional[str] = None


@dataclass
class FimatheConfluence:
    variant: Optional[str] = None
    direction: str = "UNKNOWN"
    status: ConfluenceStatus = ConfluenceStatus.UNAVAILABLE
    references: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


@dataclass
class PriceActionReport:
    analysis_version: str = "1.0"
    input_quality: InputQuality = InputQuality.MEDIUM
    asset: Optional[str] = None
    timeframe: Optional[str] = None
    market_regime: MarketRegime = MarketRegime.UNKNOWN
    trend_bias: TrendBias = TrendBias.UNKNOWN
    higher_timeframe_status: str = "UNAVAILABLE"
    market_structure: MarketStructure = field(default_factory=MarketStructure)
    breakout_status: BreakoutStatus = BreakoutStatus.NONE
    fimathe_confluence: FimatheConfluence = field(default_factory=FimatheConfluence)
    trade_plan: TradePlan = field(default_factory=TradePlan)
    confidence_level: str = "LOW"
    confidence_reasons: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    summary: str = ""
