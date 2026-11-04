"""In-memory store for labeled historical scenarios (prototype).

Not a database. For production use CSV/SQLite outside this module.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from engine.patterns.features import ScenarioFeatures


@dataclass
class StoredPattern:
    features: ScenarioFeatures
    outcome: str
    timeframe: str = "unknown"
    notes: str = ""
    source: str = ""


@dataclass
class PatternStore:
    items: List[StoredPattern] = field(default_factory=list)

    def add(self, pattern: StoredPattern) -> None:
        self.items.append(pattern)

    def features_list(self) -> List[ScenarioFeatures]:
        return [p.features for p in self.items]

    def outcomes_list(self) -> List[str]:
        return [p.outcome for p in self.items]

    def size(self) -> int:
        return len(self.items)

    def to_dicts(self) -> List[Dict[str, Any]]:
        return [
            {
                "features": p.features.to_dict(),
                "outcome": p.outcome,
                "timeframe": p.timeframe,
                "notes": p.notes,
                "source": p.source,
            }
            for p in self.items
        ]
