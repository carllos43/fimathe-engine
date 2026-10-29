"""
Fimathe mathematical engine – educational simulation only.
No real order execution.
"""

from engine.core.models import (
    MarketCandle,
    TrendAssessment,
    SwingPoint,
    ReferenceChannel,
    NeutralChannel,
    ChannelCycle,
    SubcycleLevel,
    CalculationResult,
    RuleValidation,
)
from engine.channels.geometry import (
    channel_amplitude,
    build_neutral_zone,
    level_50_of_channel,
    level_50_of_two_channels,
    project_levels,
)
from engine.cycles.projections import create_expansion, CycleModel
from engine.mapping.higher_tf import HigherTimeframeMap, SubdivisionResult
from engine.breakouts.confirmation import is_breakout_by_close

__all__ = [
    "MarketCandle",
    "TrendAssessment",
    "SwingPoint",
    "ReferenceChannel",
    "NeutralChannel",
    "ChannelCycle",
    "SubcycleLevel",
    "CalculationResult",
    "RuleValidation",
    "channel_amplitude",
    "build_neutral_zone",
    "level_50_of_channel",
    "level_50_of_two_channels",
    "project_levels",
    "create_expansion",
    "CycleModel",
    "HigherTimeframeMap",
    "SubdivisionResult",
    "is_breakout_by_close",
]

__version__ = "0.2.0"
