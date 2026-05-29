from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class SignalType(str, Enum):
    TRADE = "trade"
    NEWS = "news"
    ALPHA = "alpha"


class Direction(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"


class Confidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class ScreenerSignal:
    source_channel: str
    signal_type: SignalType
    timestamp: str
    parsed_at: str
    raw_text: str
    pair: Optional[str] = None
    direction: Optional[Direction] = None
    price: Optional[float] = None
    sl: Optional[float] = None
    tp: Optional[float] = None
    size: Optional[str] = None
    category: Optional[str] = None
    confidence: Optional[Confidence] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "source_channel": self.source_channel,
            "signal_type": self.signal_type.value,
            "timestamp": self.timestamp,
            "parsed_at": self.parsed_at,
            "raw_text": self.raw_text,
            "normalized": {
                "pair": self.pair,
                "direction": self.direction.value if self.direction else None,
                "price": self.price,
                "sl": self.sl,
                "tp": self.tp,
                "size": self.size,
                "category": self.category,
                "confidence": self.confidence.value if self.confidence else None,
            },
        }
